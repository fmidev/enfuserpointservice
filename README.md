# enfuserpointservice
Documentation and example codes to access data from the Enfuser model point service API. 

Access is only granted within projects currently for testing purposes and the interfaces as well as data availability are subject to change.

# Registration

To get an user account first register at 

https://epk.2.rahtiapp.fi/realms/enfuser-portal/account

After registering, you’ll be sent a message to confirm your e-mail.

The e-mail adress will be used only to facilitate communication about the service to you and the service is only meant for project partners in currently active projects - not for members of the general public. You are explicitly not allowed to register or use the services if you are not representing a project partner.

Once you’ve created an account and your usage has been approved, you will be notified by e-mail. Then you can use your user name (i.e. your email address) and password to access the service.

# Accessing the data

The service works with a bearer authentication mechanism. You first acquire a token from one endpoint using your username/password , which is valid for ~1 hour to get data from the other endpoints.

We have provided a python library to do these queries and handle the token for you as well as an example in java. These can be found in the code_examples directory. If you need to use other languages and are having difficulties please ask and we’ll see what can be done.

Below we explain the technical details of the endpoints:

The endpoint for acquiring the token is:

 https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token

You will need to do a https POST query with the payload of

```
data={      
     "client_id": "point-service",
     "username": your_username,
     "password": your_password,
     "grant_type": "password",
     }
```

The response json contains a field “access_token” which is your bearer token as well as some other info.

Example using curl
```bash
curl -X 'POST' 'https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token' -H 'accept: application/json' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=password&username=<your-user-name>&password=<your-password>&client_id=point-service'
```

# Access data using the token

The main endpoint is

https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data

The endpoint takes the following arguments

- lat: latitude
- lon: longitude
- startTime (optional, default now): Time you want the data to start from in format: 2025-02-27T12:00:00Z (The Z is not optional, all times must be given with proper timezones)
- endTime (optional, default startTime) same format as starttime

This endpoint gives json that has all the modeled pollutants and meteorological data for times that fall between startTime and endTime. The data is only available at full hours (i.e. 12:00, 13:00 etc), so the interval should contain at least one of them.

These endpoints should be called with a https GET query, you must include the access_token that you acquired in the previous step via a header:
> Authorization: Bearer access_token

Where you need to replace “access_token” with the actual access token (Which will be a very long string)

There are other endpoints that will be documented as they are considered ready for general use.

## Example query to the endpoint

For a call (with proper headers as described above):
```
https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data?lat=60.263296126396405&lon=24.912241001988615&startTime=2025-08-26T00%3A00Z&endTime=2025-08-26T01%3A00Z
```

<details>

<summary> Example output json (the values are for example only). The amount of pollutant species can be different for different modelling areas. </summary>

```javascript
{
  "data": [
    {
      "date": "2025-08-26T00:00:00Z",
      "values": {
        "meteorology": [
          {
            "name": "InvMOlength",
            "value": -0.0076
          },
          {
            "name": "pressure",
            "value": 998.6602
          },
          {
            "name": "ABLH",
            "value": 312.3657
          },
          {
            "name": "dewPoint",
            "value": 8.4669
          },
          {
            "name": "wind_E",
            "value": 2.013
          },
          {
            "name": "lwRad",
            "value": 285.1766
          },
          {
            "name": "wind_N",
            "value": -2.4294
          },
          {
            "name": "rain",
            "value": 0.0
          },
          {
            "name": "humidity",
            "value": 89.4313
          },
          {
            "name": "roadSurfaceWater",
            "value": 0.0
          },
          {
            "name": "sensHflux",
            "value": -1.867
          },
          {
            "name": "swRad",
            "value": 0.0
          },
          {
            "name": "temperature",
            "value": 10.0449
          },
          {
            "name": "skyCondition",
            "value": 0.0127
          },
          {
            "name": "windDirection",
            "value": 319.3647
          },
          {
            "name": "windSpeed",
            "value": 3.1365
          }
        ],
        "pollutants": [
          {
            "name": "AQI",
            "altitude100m": 1.055,
            "value": 1.0538
          },
          {
            "name": "LDSA",
            "regional": 0.7636,
            "altitude100m": 2.8049,
            "components": {
              "bg": 2.5656,
              "household": 0.0,
              "ship": 0.0,
              "power": 0.0124,
              "misc": 0.0008,
              "traffic": 0.24760000000000026
            },
            "value": 2.8264
          },
          {
            "name": "BC",
            "regional": 0.0468,
            "altitude100m": 0.0571,
            "components": {
              "bg": 0.0468,
              "ship": 0.0,
              "household": 0.0,
              "power": 0.0005,
              "misc": 0.0,
              "traffic": 0.010999999999999996
            },
            "value": 0.0583
          },
          {
            "name": "CO",
            "regional": 146.24,
            "altitude100m": 65.2636,
            "components": {
              "bg": 63.2687,
              "ship": 0.004,
              "household": 0.0,
              "power": 0.0182,
              "misc": 0.0,
              "traffic": 2.092000000000006
            },
            "value": 65.3829
          },
          {
            "name": "NO2",
            "regional": 3.4279,
            "altitude100m": 0.7732,
            "components": {
              "bg": 0.0,
              "ship": 0.0,
              "household": 0.0,
              "power": 0.0195,
              "misc": 0.0,
              "traffic": 0.8153
            },
            "value": 0.8348
          },
          {
            "name": "NO",
            "regional": 0.0196,
            "altitude100m": 0.7439,
            "components": {
              "bg": 0.0,
              "ship": 0.0,
              "household": 0.0,
              "power": 0.0131,
              "misc": 0.0,
              "traffic": 0.8019
            },
            "value": 0.815
          },
          {
            "name": "O3",
            "regional": 34.5136,
            "altitude100m": 34.7122,
            "components": {
              "bg": 35.0728,
              "household": 0.0,
              "ship": 0.0,
              "power": -0.0225,
              "misc": 0.0,
              "traffic": -0.3575999999999979
            },
            "value": 34.6927
          },
          {
            "name": "PM10",
            "regional": 1.1695,
            "altitude100m": 3.1776,
            "value": 3.2163
          },
          {
            "name": "PM25",
            "regional": 0.7636,
            "altitude100m": 1.0254,
            "components": {
              "bg": 0.9537,
              "household": 0.0,
              "ship": 0.0,
              "power": 0.0037,
              "misc": 0.0,
              "traffic": 0.07279999999999998
            },
            "value": 1.0302
          },
          {
            "name": "coarsePM",
            "regional": 0.4023,
            "altitude100m": 2.1528,
            "components": {
              "bg": 2.1425,
              "misc": 0.0254,
              "resusp": 0.0309,
              "traffic": -0.004999999999999893
            },
            "value": 2.1938
          },
          {
            "name": "PNC",
            "regional": 381.952,
            "altitude100m": 1249.3025,
            "components": {
              "bg": 927.7849,
              "ship": 1.1026,
              "household": 0.0,
              "power": 3.8002,
              "misc": 0.0,
              "traffic": 346.2912000000001
            },
            "value": 1278.9789
          }
        ]
      },
      "localDate": "2025-08-26T03:00:00+03:00"
    },
    {
      "date": "2025-08-26T01:00:00Z",
      "values": {
        "meteorology": [
          {
            "name": "InvMOlength",
            "value": -0.0107
          },
          {
            "name": "pressure",
            "value": 998.7787
          },
          {
            "name": "ABLH",
            "value": 303.7438
          },
          {
            "name": "dewPoint",
            "value": 8.1684
          },
          {
            "name": "wind_E",
            "value": 2.41
          },
          {
            "name": "lwRad",
            "value": 275.7146
          },
          {
            "name": "wind_N",
            "value": -2.4197
          },
          {
            "name": "rain",
            "value": 0.0
          },
          {
            "name": "humidity",
            "value": 91.0245
          },
          {
            "name": "roadSurfaceWater",
            "value": 0.0
          },
          {
            "name": "sensHflux",
            "value": -0.1805
          },
          {
            "name": "swRad",
            "value": 0.0
          },
          {
            "name": "temperature",
            "value": 9.4676
          },
          {
            "name": "skyCondition",
            "value": 0.0643
          },
          {
            "name": "windDirection",
            "value": 314.8381
          },
          {
            "name": "windSpeed",
            "value": 3.3908
          }
        ],
        "pollutants": [
          {
            "name": "AQI",
            "altitude100m": 1.0556,
            "value": 1.0554
          },
          {
            "name": "LDSA",
            "regional": 0.8112,
            "altitude100m": 2.8259,
            "components": {
              "bg": 2.5758,
              "household": 0.004,
              "ship": 0.0,
              "power": 0.0074,
              "misc": 0.0,
              "traffic": 0.2674999999999996
            },
            "value": 2.8547
          },
          {
            "name": "BC",
            "regional": 0.0499,
            "altitude100m": 0.0524,
            "components": {
              "bg": 0.0423,
              "household": 0.0004,
              "ship": 0.0,
              "power": 0.0005,
              "misc": 0.0,
              "traffic": 0.009500000000000001
            },
            "value": 0.0527
          },
          {
            "name": "CO",
            "regional": 145.8492,
            "altitude100m": 66.2318,
            "components": {
              "bg": 64.2421,
              "household": 0.0537,
              "ship": 0.0,
              "power": 0.0151,
              "misc": 0.0,
              "traffic": 2.027300000000011
            },
            "value": 66.3382
          },
          {
            "name": "NO2",
            "regional": 3.6517,
            "altitude100m": 0.7263,
            "components": {
              "bg": 0.0,
              "household": 0.0002,
              "ship": 0.0,
              "power": 0.016,
              "misc": 0.0,
              "traffic": 0.7658
            },
            "value": 0.782
          },
          {
            "name": "NO",
            "regional": 0.0251,
            "altitude100m": 0.7245,
            "components": {
              "bg": 0.0,
              "ship": 0.0,
              "household": 0.0,
              "power": 0.0109,
              "misc": 0.0,
              "traffic": 0.7715
            },
            "value": 0.7824
          },
          {
            "name": "O3",
            "regional": 32.1404,
            "altitude100m": 32.3489,
            "components": {
              "bg": 32.6699,
              "ship": 0.0,
              "household": 0.0,
              "power": -0.0186,
              "misc": -0.0014,
              "traffic": -0.37189999999999657
            },
            "value": 32.278
          },
          {
            "name": "PM10",
            "regional": 1.2223,
            "altitude100m": 3.0497,
            "value": 3.099
          },
          {
            "name": "PM25",
            "regional": 0.8112,
            "altitude100m": 1.0613,
            "components": {
              "bg": 0.9877,
              "ship": 0.0,
              "household": 0.0013,
              "power": 0.0026,
              "misc": 0.0,
              "traffic": 0.07329999999999992
            },
            "value": 1.0649
          },
          {
            "name": "coarsePM",
            "regional": 0.4139,
            "altitude100m": 1.9845,
            "components": {
              "bg": 1.9724,
              "misc": 0.0334,
              "resusp": 0.0182,
              "traffic": 0.010499999999999954
            },
            "value": 2.0345
          },
          {
            "name": "PNC",
            "regional": 405.6044,
            "altitude100m": 1140.5321,
            "components": {
              "bg": 825.6502,
              "ship": 0.0,
              "household": 1.2903,
              "power": 2.5586,
              "misc": 1.0117,
              "traffic": 342.8056999999999
            },
            "value": 1173.3165
          }
        ]
      },
      "localDate": "2025-08-26T04:00:00+03:00"
    }
  ],
  "longitude": 24.912241001988615,
  "latitude": 60.263296126396405,
  "units": {
    "NO": "μg/m^3",
    "BC": "μg/m^3",
    "ABLH": "m",
    "O3": "μg/m^3",
    "PNC": "1/cm^3",
    "wind_E": "degrees",
    "coarsePM": "μg/m^3",
    "skyCondition": "",
    "NO2": "μg/m^3",
    "SO2": "μg/m^3",
    "temperature": "°C",
    "AQI": "",
    "humidity": "%",
    "swRad": "W/m^2",
    "windDirection": "degrees",
    "wind_N": "m/s",
    "windSpeed": "m/s",
    "sensHflux": "W/m^2",
    "rain": "precipitation_mm_per_hour",
    "lwRad": "W/m^2",
    "NMVOC": "μg/m^3",
    "LDSA": "um2 1/cm^3",
    "PM25": "μg/m^3",
    "pressure": "hPa",
    "dewPoint": "°C",
    "CO": "μg/m^3",
    "roadSurfaceWater": "µm",
    "PM10": "μg/m^3",
    "InvMOlength": "1/m"
  }
}
```

</details>


<details>

<Summary> Inside buildings the API returns an explanation and no data </Summary>

In these cases pick a point outside the building.

Example building call
```
https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data?lat=60.19823873736357&lon=24.930557907247696&startTime=2025-08-26T00%3A00Z&endTime=2025-08-26T01%3A00Z
```

Example json output
```javascript
[{"parameter":null,"error":"Location is inside a building."}]
```

</details>

## Known issues
* The server can return 403 even with correct credentials when there is high load. Simply retry after a few seconds.

## Regions endpoint

https://enfuser-portal.2.rahtiapp.fi/enfuser/regions-areas

An endpoint that gives the boundaries of currently valid modelling areas.
The endpoint takes no arguments but requires the same authorization. Querying outside these bounds will result in empty results "[]".

### Examples of regions endpoint

With curl:
```bash
curl 'https://enfuser-portal.2.rahtiapp.fi/enfuser/regions-areas' -H 'Authorization: Bearer <your-access-token>'
```

Both steps with jq:
```bash
export ACCESS_TOKEN=”$(curl -X 'POST' 'https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token' -H 'accept: application/json' -H 'Content-Type: application/x-www-form-urlencoded' -d grant_type=password&username=<your-user-name>&password=<your-password>&client_id=point-service| jq -r ‘.access_token’)”
curl 'https://enfuser-portal.2.rahtiapp.fi/enfuser/regions-areas' -H "Authorization: Bearer ${ACCESS_TOKEN}"
```
