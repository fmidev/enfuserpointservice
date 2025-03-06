# enfuserpointservice
Documentation and example codes to access data from the Enfuser model point service API. 

Access is only granted within projects currently for testing purposes and the interfaces as well as data availability are subject to change.

# Registration

To get an user account first register at 

https://epk.2.rahtiapp.fi/realms/enfuser-portal/account

After registering, you’ll be sent a message to confirm your e-mail.

The e-mail adress will be used only to facilitate communication about the service to you and the service is only meant for project partners in currently active projects - not for members of the general public. You are explicitly not allowed to register or use the services if you are not representing a project partner.

Once you’ve created an account, send an e-mail to Matti Jokinen explaining your intended usage and once it has been approved, you can then use your e-mail (i.e. your username) and password to access the service.

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
- startTime (optional, default now): Time you want the data to start from in format: 2025-02-27T12:00:00Z (The Z is not optional, all times must be given in UTC)
- endTime (optional, default startTime) same format as starttime

This endpoint gives json that has all the modeled pollutants and meteorological data for times that fall between startTime and endTime. The data is only available at full hours (i.e. 12:00, 13:00 etc), so the interval should contain at least one of them.

These endpoints should be called with a https GET query, you must include the access_token that you acquired in the previous step via a header:
> Authorization: Bearer access_token

Where you need to replace “access_token” with the actual access token (Which will be a very long string)

## Example query to the endpoint

For a call (with proper headers as described above):
```
https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data?lat=60.17501&lon=24.93263&startTime=2025-02-24T01%3A00%3A00Z&endTime=2025-02-24T02%3A00%3A00Z
```

Example output json (the values are for example only). The amount of pollutant species can be different for different modelling areas.
```json
{'longitude': 24.93263,
 'latitude': 60.17501,
 'data': [{'date': '2025-02-24T01:00:00Z',
   'values': {'meteorology': [{'name': 'ABLH', 'value': 235.865, 'unit': 'm'},
     {'name': 'InvMOlength', 'value': 0.001, 'unit': '1/m'},
     {'name': 'humidity', 'value': 90.356, 'unit': '%'},
     {'name': 'lwRad', 'value': 293.449, 'unit': 'W/m^2'},
     {'name': 'pressure', 'value': 1020.981, 'unit': 'hPa'},
     {'name': 'rain', 'value': 0.01, 'unit': 'precipitation_mm_per_hour'},
     {'name': 'roadSurfaceWater', 'value': 0.05, 'unit': 'µm'},
     {'name': 'skyCondition', 'value': 1.0, 'unit': ''},
     {'name': 'swRad', 'value': 0.0, 'unit': 'W/m^2'},
     {'name': 'temperature', 'value': 1.967, 'unit': '°C'},
     {'name': 'windDirection', 'value': 207.479, 'unit': 'degrees'},
     {'name': 'windSpeed', 'value': 6.106, 'unit': 'm/s'},
     {'name': 'wind_E', 'value': 2.813, 'unit': 'degrees'},
     {'name': 'wind_N', 'value': 5.432, 'unit': 'm/s'}],
    'pollutants': [{'name': 'AQI', 'value': 3.009, 'unit': ''},
     {'name': 'BC',
      'value': 1.467,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 1.423},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.0},
       {'component': 'ship', 'value': 0.001},
       {'component': 'traffic', 'value': 0.036}],
      'regional': 0.863},
     {'name': 'CO',
      'value': 180.648,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 170.303},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.013},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 7.806}],
      'regional': 239.031},
     {'name': 'LDSA',
      'value': 18.322,
      'unit': 'µm^2/cm^3',
      'components': [{'component': 'bg', 'value': 16.428},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.008},
       {'component': 'traffic', 'value': 1.407}],
      'regional': 14.622},
     {'name': 'NO',
      'value': 2.896,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.009},
       {'component': 'ship', 'value': 0.064},
       {'component': 'traffic', 'value': 2.198}],
      'regional': 0.014},
     {'name': 'NO2',
      'value': 8.313,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 5.949},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.004},
       {'component': 'ship', 'value': 0.095},
       {'component': 'traffic', 'value': 1.728}],
      'regional': 10.832},
     {'name': 'O3',
      'value': 57.334,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 58.937},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': -0.016},
       {'component': 'ship', 'value': -0.056},
       {'component': 'traffic', 'value': -1.61}],
      'regional': 37.493},
     {'name': 'PM10', 'value': 32.301, 'unit': 'µg/m^3', 'regional': 15.052},
     {'name': 'PM25',
      'value': 25.616,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 25.136},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.003},
       {'component': 'traffic', 'value': 0.375}],
      'regional': 14.622},
     {'name': 'PNC',
      'value': 12401.994,
      'unit': '1/cm^3',
      'components': [{'component': 'bg', 'value': 7622.396},
       {'component': 'household', 'value': 0.002},
       {'component': 'power', 'value': 1.944},
       {'component': 'ship', 'value': 2.637},
       {'component': 'traffic', 'value': 3312.948}],
      'regional': 7311.122},
     {'name': 'coarsePM',
      'value': 6.428,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'misc', 'value': 2.031},
       {'component': 'resusp', 'value': 2.832},
       {'component': 'traffic', 'value': 0.233}],
      'regional': 0.56}]}},
  {'date': '2025-02-24T02:00:00Z',
   'values': {'meteorology': [{'name': 'ABLH', 'value': 224.745, 'unit': 'm'},
     {'name': 'InvMOlength', 'value': 0.001, 'unit': '1/m'},
     {'name': 'humidity', 'value': 90.086, 'unit': '%'},
     {'name': 'lwRad', 'value': 299.594, 'unit': 'W/m^2'},
     {'name': 'pressure', 'value': 1020.507, 'unit': 'hPa'},
     {'name': 'rain', 'value': 0.0, 'unit': 'precipitation_mm_per_hour'},
     {'name': 'roadSurfaceWater', 'value': 0.059, 'unit': 'µm'},
     {'name': 'skyCondition', 'value': 1.0, 'unit': ''},
     {'name': 'swRad', 'value': 0.0, 'unit': 'W/m^2'},
     {'name': 'temperature', 'value': 2.057, 'unit': '°C'},
     {'name': 'windDirection', 'value': 217.061, 'unit': 'degrees'},
     {'name': 'windSpeed', 'value': 5.487, 'unit': 'm/s'},
     {'name': 'wind_E', 'value': 3.28, 'unit': 'degrees'},
     {'name': 'wind_N', 'value': 4.413, 'unit': 'm/s'}],
    'pollutants': [{'name': 'AQI', 'value': 3.111, 'unit': ''},
     {'name': 'BC',
      'value': 1.424,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 1.37},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 0.051}],
      'regional': 0.886},
     {'name': 'CO',
      'value': 184.682,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 173.536},
       {'component': 'household', 'value': 0.017},
       {'component': 'power', 'value': 0.071},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 8.402}],
      'regional': 240.04},
     {'name': 'LDSA',
      'value': 18.858,
      'unit': 'µm^2/cm^3',
      'components': [{'component': 'bg', 'value': 17.011},
       {'component': 'household', 'value': 0.001},
       {'component': 'power', 'value': 0.01},
       {'component': 'ship', 'value': 0.004},
       {'component': 'traffic', 'value': 1.444}],
      'regional': 15.295},
     {'name': 'NO',
      'value': 2.837,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.051},
       {'component': 'ship', 'value': 0.028},
       {'component': 'traffic', 'value': 2.164}],
      'regional': 0.015},
     {'name': 'NO2',
      'value': 7.991,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 5.633},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.025},
       {'component': 'ship', 'value': 0.042},
       {'component': 'traffic', 'value': 1.835}],
      'regional': 10.77},
     {'name': 'O3',
      'value': 58.571,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 59.839},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': -0.052},
       {'component': 'ship', 'value': -0.025},
       {'component': 'traffic', 'value': -1.35}],
      'regional': 37.081},
     {'name': 'PM10', 'value': 33.4, 'unit': 'µg/m^3', 'regional': 15.789},
     {'name': 'PM25',
      'value': 27.273,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 26.882},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.01},
       {'component': 'ship', 'value': 0.001},
       {'component': 'traffic', 'value': 0.379}],
      'regional': 15.295},
     {'name': 'PNC',
      'value': 12651.571,
      'unit': '1/cm^3',
      'components': [{'component': 'bg', 'value': 7652.822},
       {'component': 'household', 'value': 0.504},
       {'component': 'power', 'value': 9.779},
       {'component': 'ship', 'value': 1.317},
       {'component': 'traffic', 'value': 2976.331}],
      'regional': 7643.334},
     {'name': 'coarsePM',
      'value': 5.88,
      'unit': 'µg/m^3',
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'misc', 'value': 2.039},
       {'component': 'resusp', 'value': 2.789},
       {'component': 'traffic', 'value': 0.233}],
      'regional': 0.543}]}}]}
```

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
