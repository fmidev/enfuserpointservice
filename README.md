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

<details>

<summary> Example output json (the values are for example only). The amount of pollutant species can be different for different modelling areas. </summary>

```javascript
{'longitude': 24.93263,
 'latitude': 60.17501,
 'units': {'BC': 'µg/m^3',
  'NO': 'µg/m^3',
  'ABLH': 'm',
  'O3': 'µg/m^3',
  'PNC': '1/cm^3',
  'wind_E': 'degrees',
  'coarsePM': 'µg/m^3',
  'skyCondition': '',
  'NO2': 'µg/m^3',
  'SO2': 'µg/m^3',
  'temperature': '°C',
  'AQI': '',
  'humidity': '%',
  'swRad': 'W/m^2',
  'windDirection': 'degrees',
  'windSpeed': 'm/s',
  'wind_N': 'm/s',
  'rain': 'precipitation_mm_per_hour',
  'lwRad': 'W/m^2',
  'NMVOC': 'µg/m^3',
  'LDSA': 'µm^2/cm^3',
  'PM25': 'µg/m^3',
  'pressure': 'hPa',
  'CO': 'µg/m^3',
  'roadSurfaceWater': 'µm',
  'PM10': 'µg/m^3',
  'InvMOlength': '1/m'},
 'data': [{'date': '2025-02-24T01:00:00Z',
   'values': {'meteorology': [{'name': 'ABLH', 'value': 235.865},
     {'name': 'InvMOlength', 'value': 0.001},
     {'name': 'humidity', 'value': 90.356},
     {'name': 'lwRad', 'value': 293.449},
     {'name': 'pressure', 'value': 1020.981},
     {'name': 'rain', 'value': 0.01},
     {'name': 'roadSurfaceWater', 'value': 0.05},
     {'name': 'skyCondition', 'value': 1.0},
     {'name': 'swRad', 'value': 0.0},
     {'name': 'temperature', 'value': 1.967},
     {'name': 'windDirection', 'value': 207.479},
     {'name': 'windSpeed', 'value': 6.106},
     {'name': 'wind_E', 'value': 2.813},
     {'name': 'wind_N', 'value': 5.432}],
    'pollutants': [{'name': 'AQI', 'value': 3.009},
     {'name': 'BC',
      'value': 1.467,
      'components': [{'component': 'bg', 'value': 1.423},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.0},
       {'component': 'ship', 'value': 0.001},
       {'component': 'traffic', 'value': 0.036}],
      'regional': 0.863},
     {'name': 'CO',
      'value': 180.648,
      'components': [{'component': 'bg', 'value': 170.303},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.013},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 7.806}],
      'regional': 239.031},
     {'name': 'LDSA',
      'value': 18.322,
      'components': [{'component': 'bg', 'value': 16.428},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.008},
       {'component': 'traffic', 'value': 1.407}],
      'regional': 14.622},
     {'name': 'NO',
      'value': 2.896,
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.009},
       {'component': 'ship', 'value': 0.064},
       {'component': 'traffic', 'value': 2.198}],
      'regional': 0.014},
     {'name': 'NO2',
      'value': 8.313,
      'components': [{'component': 'bg', 'value': 5.949},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.004},
       {'component': 'ship', 'value': 0.095},
       {'component': 'traffic', 'value': 1.728}],
      'regional': 10.832},
     {'name': 'O3',
      'value': 57.334,
      'components': [{'component': 'bg', 'value': 58.937},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': -0.016},
       {'component': 'ship', 'value': -0.056},
       {'component': 'traffic', 'value': -1.61}],
      'regional': 37.493},
     {'name': 'PM10', 'value': 32.301, 'regional': 15.052},
     {'name': 'PM25',
      'value': 25.616,
      'components': [{'component': 'bg', 'value': 25.136},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.003},
       {'component': 'traffic', 'value': 0.375}],
      'regional': 14.622},
     {'name': 'PNC',
      'value': 12401.994,
      'components': [{'component': 'bg', 'value': 7622.396},
       {'component': 'household', 'value': 0.002},
       {'component': 'power', 'value': 1.944},
       {'component': 'ship', 'value': 2.637},
       {'component': 'traffic', 'value': 3312.948}],
      'regional': 7311.122},
     {'name': 'coarsePM',
      'value': 6.428,
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'misc', 'value': 2.031},
       {'component': 'resusp', 'value': 2.832},
       {'component': 'traffic', 'value': 0.233}],
      'regional': 0.56}]}},
  {'date': '2025-02-24T02:00:00Z',
   'values': {'meteorology': [{'name': 'ABLH', 'value': 224.745},
     {'name': 'InvMOlength', 'value': 0.001},
     {'name': 'humidity', 'value': 90.086},
     {'name': 'lwRad', 'value': 299.594},
     {'name': 'pressure', 'value': 1020.507},
     {'name': 'rain', 'value': 0.0},
     {'name': 'roadSurfaceWater', 'value': 0.059},
     {'name': 'skyCondition', 'value': 1.0},
     {'name': 'swRad', 'value': 0.0},
     {'name': 'temperature', 'value': 2.057},
     {'name': 'windDirection', 'value': 217.061},
     {'name': 'windSpeed', 'value': 5.487},
     {'name': 'wind_E', 'value': 3.28},
     {'name': 'wind_N', 'value': 4.413}],
    'pollutants': [{'name': 'AQI', 'value': 3.111},
     {'name': 'BC',
      'value': 1.424,
      'components': [{'component': 'bg', 'value': 1.37},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.002},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 0.051}],
      'regional': 0.886},
     {'name': 'CO',
      'value': 184.682,
      'components': [{'component': 'bg', 'value': 173.536},
       {'component': 'household', 'value': 0.017},
       {'component': 'power', 'value': 0.071},
       {'component': 'ship', 'value': 0.0},
       {'component': 'traffic', 'value': 8.402}],
      'regional': 240.04},
     {'name': 'LDSA',
      'value': 18.858,
      'components': [{'component': 'bg', 'value': 17.011},
       {'component': 'household', 'value': 0.001},
       {'component': 'power', 'value': 0.01},
       {'component': 'ship', 'value': 0.004},
       {'component': 'traffic', 'value': 1.444}],
      'regional': 15.295},
     {'name': 'NO',
      'value': 2.837,
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.051},
       {'component': 'ship', 'value': 0.028},
       {'component': 'traffic', 'value': 2.164}],
      'regional': 0.015},
     {'name': 'NO2',
      'value': 7.991,
      'components': [{'component': 'bg', 'value': 5.633},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.025},
       {'component': 'ship', 'value': 0.042},
       {'component': 'traffic', 'value': 1.835}],
      'regional': 10.77},
     {'name': 'O3',
      'value': 58.571,
      'components': [{'component': 'bg', 'value': 59.839},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': -0.052},
       {'component': 'ship', 'value': -0.025},
       {'component': 'traffic', 'value': -1.35}],
      'regional': 37.081},
     {'name': 'PM10', 'value': 33.4, 'regional': 15.789},
     {'name': 'PM25',
      'value': 27.273,
      'components': [{'component': 'bg', 'value': 26.882},
       {'component': 'household', 'value': 0.0},
       {'component': 'power', 'value': 0.01},
       {'component': 'ship', 'value': 0.001},
       {'component': 'traffic', 'value': 0.379}],
      'regional': 15.295},
     {'name': 'PNC',
      'value': 12651.571,
      'components': [{'component': 'bg', 'value': 7652.822},
       {'component': 'household', 'value': 0.504},
       {'component': 'power', 'value': 9.779},
       {'component': 'ship', 'value': 1.317},
       {'component': 'traffic', 'value': 2976.331}],
      'regional': 7643.334},
     {'name': 'coarsePM',
      'value': 5.88,
      'components': [{'component': 'bg', 'value': 0.0},
       {'component': 'misc', 'value': 2.039},
       {'component': 'resusp', 'value': 2.789},
       {'component': 'traffic', 'value': 0.233}],
      'regional': 0.543}]}}]}
```

</details>


<details>

<Summary> Inside buildings the API returns an explanation and no data </Summary>

In these cases pick a point outside the building.

Example building call
```
https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data?lat=60.19823873736357&lon=24.930557907247696&startTime=2025-03-10T13%3A09%3A58Z
```

Example json output
```javascript
{"longitude":24.930557907247696,"latitude":60.19823873736357,"unavailable":"Location is inside a building.","data":[]}
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
