# Python example

The library requires: numpy, pandas, xarray and requests

How to install: Copy the folder enfuserpointservice to where you want to use the code.

# Usage

The library assumes that you have a credentials.json (with two elements "username" and "password") in the same folder as you are using it. Alternatively you can just give username and password as arguments.

```python
from enfuserpointservice.get_data import EnfuserAPI

# If you have credentials.json file in the same directory as this file, you can use the default constructor
a = EnfuserAPI()

# otherwise you can provide the username and password
#a = EnfuserAPI(username="yourusername", password="yourpassword")

# Some example values
lat = 60.2
lon = 25.0
starttime = "2025-01-01T00:00:00Z"
endtime = "2025-01-01T01:00:00Z"

#Parsed to a dictionary of xarrays
result = a.acquire(lat, lon, starttime, endtime, parse=True)

# Json response
result_json = a.acquire(lat, lon, starttime, endtime)

#Get modelling area information as json parsed into a python list+dictionary
area_info = a.get_modelling_areas()
```
