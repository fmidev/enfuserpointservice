import json
import requests
from time import sleep
from datetime import datetime, timedelta
from pathlib import Path
from . import parsing

import pandas as pd
from datetime import datetime

import traceback

default_credential_store = Path("./credentials.json")

class EnfuserAPI:
    def __init__(self, username=None, password=None, 
                 token_endpoint="https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token",
                api_base="https://point-service-enfuser-portal.2.rahtiapp.fi"):
        
        if username is None or password is None:
            if not default_credential_store.exists():
                raise Exception("No credentials provided and no default credential store found.")
            with default_credential_store.open("r") as f:
                credentials = json.load(f)
                self.username = credentials["username"]
                self.password = credentials["password"]
        else:
            self.username = username
            self.password = password
        
        self.token = None
        self.token_acquired_time = None
        self.api_base = api_base
        self.api_endpoint = api_base + "/enfuser/point-data"
        self.regions_areas_endpoint = api_base + "/enfuser/regions-areas"
        self.geotiff_endpoint = api_base + "/enfuser/geotiff"
        self.netcdf_endpoint = api_base + "/enfuser/netcdf"
        self.point_statistics_endpoint = api_base + "/enfuser/point-statistics"
        self.token_endpoint = token_endpoint
        self.get_token()

    def get_token(self):
        response = requests.post(self.token_endpoint, data={
            "client_id": "point-service",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        })
        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.status_code}, {response.text}")
        
        self.token = response.json()["access_token"]
        self.token_acquired_time = datetime.now()

    def get_headers(self):
        if self.token is None or datetime.now() - self.token_acquired_time > timedelta(minutes=30):
            self.get_token()
        return {"Authorization": f"Bearer {self.token}"}
    
    def turn_time_to_string(self, t):

        if isinstance(t, str):
            return t

        if isinstance(t, datetime):
            x = pd.Timestamp(t)
        else:
            x = t.copy()
        
        if x.tzinfo is None:
            x = x.tz_localize("UTC")
        else:
            x = x.tz_convert("UTC")

        return x.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    

    def get_modelling_areas(self):

        """
        Get the available areas for the point service.
        """
        response = requests.get(self.regions_areas_endpoint, headers=self.get_headers())
        if response.status_code != 200:
            raise Exception(f"Failed to get areas: {response.status_code}, {response.text}")
        
        return response.json()
    
    def get_area(self, format="netcdf", variables=None, north=None, south=None, west=None, east=None, dateTime=None):
        """
        Query the geotiff or netcdf endpoint with the given parameters.

        Args:
            endpoint (str): "geotiff" or "netcdf"
            variables (list): List of variable names (strings)
            north, south, west, east (float): Bounding box coordinates
            dateTime (str): ISO formatted datetime string

        Returns:
            Response: Response object from the request.
        """
        if format not in ["geotiff", "netcdf"]:
            raise ValueError("format must be 'geotiff' or 'netcdf'")

        url = self.geotiff_endpoint if format == "geotiff" else self.netcdf_endpoint

        params = {}

        params["variables"] = variables
        params["north"] = north
        params["south"] = south
        params["west"] = west
        params["east"] = east
        params["dateTime"] = dateTime

        response = requests.get(url, params=params, headers=self.get_headers())
        if response.status_code != 200:
            print((f"Failed to get {format}: {response.status_code}, {response.text}"))
            raise Exception(f"Failed to get {format}: {response.status_code}, {response.text}")
        return response
    

    def get_statistics(self, lat, lon, starttime, endtime, parse=True):
        """
        Query the point-statistics endpoint with the given parameters.

        Args:
            lat (float): Latitude.
            lon (float): Longitude.
            starttime (str or datetime): Start time (ISO string or datetime).
            endtime (str or datetime): End time (ISO string or datetime).

        Returns:
            Response JSON if parse is False or xarray if parse is True.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "startTime": self.turn_time_to_string(starttime),
            "endTime": self.turn_time_to_string(endtime)
        }

        response = requests.get(self.point_statistics_endpoint, params=params, headers=self.get_headers())
        if response.status_code != 200:
            print(f"Failed to get statistics: {response.status_code}, {response.text}")
            return response
        
        if parse:
            try:
                return parsing.parse_statistics_endpoint(response.json())
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print(f"Can't parse the statistics data. Message from server {response.text} \n")
                return response

        return response.json()
    
    def acquire(self, lat, lon, starttime, endtime=None, parse=False, values=None, retries=3, retry_interval=2):
            
            str_start = self.turn_time_to_string(starttime)
            if endtime is not None:
                str_end = self.turn_time_to_string(endtime)
            else:
                str_end = None

            print(f"Getting data at {lat}, {lon} from {str_start} to {str_end}")
            params = {
                "lat": lat,
                "lon": lon,
                "startTime": str_start,
                "endTime": str_end,
            }
            if values is not None:
                params["values"] = values
    
            for attempt in range(retries):
                result = requests.get(self.api_endpoint, params=params, headers=self.get_headers())
                if result.status_code == 403:
                    print("Retrying")
                    #wait for few seconds and try again
                    sleep(retry_interval)
                else:
                    if result.status_code != 200:
                        raise Exception(f"Failed to get data: {result.status_code}, {result.text}")
                    break
            else:
                raise Exception("Failed to get data after multiple retries. Please make sure you have been granted permission to pointservice & check your credentials.")
            
            if not parse:
                return result.json()

            try:
                return parsing.transform_to_xarray(result.json())
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print(f"Can't parse the data. Check it is not inside a building, or outside the modelling areas. Message from server {result.text} \n")
                return result.text