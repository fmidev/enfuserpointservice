import pandas as pd
import numpy as np
import xarray as xr

from functools import reduce
import operator


def convert_units_to_dict(units):

    return {item['name']: item['unit'] for item in units}

def convert_components_to_dict(components):

    if type(components) != list:
        return components

    #component naming has changed in api v2
    if 'name' in components[0]:
        var = 'name'
    elif 'component' in components[0]:
        var = 'component'
    else:
        #It's a list of dictionaries with no name or component key, so we assume it's a list of values
        return reduce(operator.ior, components, {})

    return {item[var]: item['value'] for item in components}

def create_set(times, entry, name, units=None):
    
    # units description has changed for api v2
    if type(units) == list:
        units = convert_units_to_dict(units)

    dt = len(times)

    if name == "meteorology":
        #special case
        components = {item['name']: ("time", np.full(dt, np.nan), {"unit":units[item["name"]]}) for item in entry}
        ds = xr.Dataset(data_vars=components,
                    coords={'time': times}
        )
        return ds

    if 'components' in entry:
        if type(entry['components']) == list:
            cc = convert_components_to_dict(entry['components'])
        else:
            cc = entry['components'] 
        components = {key: np.full(dt, np.nan) for key in cc.keys()}
    else:
        components = {}

    if 'regional' in entry:
        components['regional'] = np.full(dt, np.nan)

    components[entry['name']] = np.full(dt, np.nan)

    components = {name:('time', comp) for name,comp in components.items()}

    ds = xr.Dataset(data_vars=components,
                    coords={'time': times}
    )

    if type(units) == list:
        units_v = {i["name"]:i["unit"] for i in units}
    else:
        units_v = units.copy()

    ds.attrs['unit'] = units_v[entry["name"]]

    ds.attrs['name'] = entry['name']

    return ds

def transform_to_xarray(data):
    times = []
    latitude = data["latitude"]
    longitudes = data["longitude"]

    units = data["units"]

    datapoints = len(data["data"])

    times = pd.to_datetime([record["date"] for record in data["data"]]).values

    datasets = {}

    #Create all datasets based on the first value
    for key, dd in data["data"][0]["values"].items():
        if key == "meteorology":
            datasets[key] = create_set(times, dd, key, units)
        else:
            for entry in dd:
                datasets[entry['name']] = create_set(times, entry, '', units)

    for i in range(datapoints):
        for key, dd in data["data"][i]["values"].items():
            if key == "meteorology":
                for entry in dd:
                    datasets[key][entry['name']][i] = entry['value']
            else:
                for entry in dd:
                    datasets[entry['name']][entry["name"]][i] = entry['value']
                    if 'components' in entry:
                        cc = convert_components_to_dict(entry['components'])
                        for key,comp in cc.items():
                            try:
                                datasets[entry['name']][key][i] = comp
                            except KeyError as e:
                                #Create the component if it wasn't in the first response
                                datasets[entry['name']][key] = xr.DataArray(np.full(datapoints, np.nan), coords=[times], dims=["time"])
                                datasets[entry['name']][key][i] = comp
                    if 'regional' in entry:
                        datasets[entry["name"]]['regional'][i] = entry['regional']

    return datasets

def pad_hour(s: pd.Series) -> pd.Series:
    return s.str.replace(r'(\d+)$', lambda m: f"{int(m.group(1)):02}", regex=True)

def parse_statistics_endpoint(response):
    """
    Parse the response from the statistics endpoint.

    Args:
        response (dict): The response from the statistics endpoint (.json())

    Returns:
        dict: Parsed statistics data.
    """
    if not isinstance(response, dict):
        raise ValueError("Response must be a dictionary")

    if "values" not in response:
        raise ValueError("Response does not contain 'values' key")

    results = {}
    for item in response["values"]:
        results[item["name"]] = pd.DataFrame(item["statistics"]).sort_values(by="group", key=pad_hour).set_index("group")

    result = xr.Dataset({k: xr.DataArray(v, dims=['Time', 'Metric'])
             for k, v in results.items()})
    
    result.attrs["Timezone"] = response["zoneId"]

    return result