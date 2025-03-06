import pandas as pd
import numpy as np
import xarray as xr

def create_set(times, entry, name):
    
    dt = len(times)

    if name == "meteorology":
        #special case
        for item in entry:
            components = {item['name']: ("time", np.full(dt, np.nan), {"unit":item["unit"]}) for item in entry}
        ds = xr.Dataset(data_vars=components,
                    coords={'time': times}
        )
        return ds

    if 'components' in entry:
        components = {comp['component']: np.full(dt, np.nan) for comp in entry['components']}
    else:
        components = {}

    if 'regional' in entry:
        components['regional'] = np.full(dt, np.nan)

    components[entry['name']] = np.full(dt, np.nan)

    components = {name:('time', comp) for name,comp in components.items()}

    ds = xr.Dataset(data_vars=components,
                    coords={'time': times}
    )

    if entry['unit'] != "":
        ds.attrs['unit'] = entry['unit']

    ds.attrs['name'] = entry['name']

    return ds

def transform_to_xarray(data):
    times = []
    latitude = data["latitude"]
    longitudes = data["longitude"]

    datapoints = len(data["data"])

    times = pd.to_datetime([record["date"] for record in data["data"]])

    datasets = {}

    #Create all datasets based on the first value
    i = 0
    for key, dd in data["data"][0]["values"].items():
        if key == "meteorology":
            datasets[key] = create_set(times, dd, key)
        else:
            for entry in dd:
                datasets[entry['name']] = create_set(times, entry, '')
        i=i+1

    for i in range(datapoints):
        for key, dd in data["data"][i]["values"].items():
            if key == "meteorology":
                for entry in dd:
                    datasets[key][entry['name']][i] = entry['value']
            else:
                for entry in dd:
                    datasets[entry['name']][entry["name"]][i] = entry['value']
                    if 'components' in entry:
                        for comp in entry['components']:
                            try:
                                datasets[entry['name']][comp["component"]][i] = comp['value']
                            except KeyError as e:
                                #Create the component if it wasn't in the first response
                                datasets[entry['name']][comp["component"]] = xr.DataArray(np.full(datapoints, np.nan), coords=[times], dims=["time"])
                                datasets[entry['name']][comp["component"]][i] = comp['value']
                    if 'regional' in entry:
                        datasets[entry["name"]]['regional'][i] = entry['regional']

    return datasets