import json
import requests
from time import sleep
from datetime import datetime, timedelta
from pathlib import Path
from . import parsing

import pandas as pd
from datetime import datetime

default_credential_store = Path("./credentials.json")

class EnfuserAPI:
    def __init__(self, username=None, password=None, 
                 token_endpoint="https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token",
                   api_endpoint="https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data"):
        
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
        self.token_endpoint = token_endpoint
        self.api_endpoint = api_endpoint
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
    
    def acquire(self, lat, lon, starttime, endtime, parse=False, retries=3, retry_interval=2):
            
            str_start = self.turn_time_to_string(starttime)
            str_end = self.turn_time_to_string(endtime)

            print(f"Getting data at {lat}, {lon} from {str_start} to {str_end}")
            params = {
                "lat": lat,
                "lon": lon,
                "startTime": str_start,
                "endTime": str_end,
            }
    
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
                print(f"Can't parse the data. Check it is not inside a building, or outside the modelling areas. Message from server {result.text} \n")
                return result.text