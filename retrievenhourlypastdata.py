import requests
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

"""
    vegtype_1:35-m broadleaf-evergreen trees (70% coverage)
    vegtype_2:20-m broadleaf-deciduous trees (75% coverage)
    vegtype_3:20-m broadleaf and needleleaf trees (75% coverage)
    vegtype_4:17-m needleleaf-evergreen trees (75% coverage)
    vegtype_5:14-m needleleaf-deciduous trees (50% coverage)
    vegtype_6:Savanna 18-m broadleaf trees (30%) & groundcover
    vegtype_7:0.6-m perennial groundcover (100%)
    vegtype_8:0.5-m broadleaf shrubs (variable %) & groundcover
    vegtype_9:0.5-m broadleaf shrubs (10%) with bare soil
    vegtype_10:Tundra: 0.6-m trees/shrubs (variable %) & groundcover
    vegtype_11:Rough bare soil
    vegtype_12:20-m broadleaf-deciduous trees (10%) & wheat
    vegtype_20:Rough glacial snow/ice
    seaice:Smooth sea ice
    openwater:Open water
    airportice:Airport: flat ice/snow
    airportgrass:Airport: flat rough grass
    "accept": "application/json"
"""

def quick_convert(json_data,name):
    params = json_data['properties']['parameter']
    all_dates = set()
    for param_data in params.values():
        all_dates.update(param_data.keys())
    dates = sorted(list(all_dates))
    
    df = pd.DataFrame([{
        'datetime': datetime.strptime(d, '%Y%m%d%H').strftime('%Y-%m-%d %H:%M:%S'),
        'date': datetime.strptime(d, '%Y%m%d%H').strftime('%Y-%m-%d'),
        'hour': int(d[8:10]),    
        **{var: params[var][d] for var in params.keys()}
    } for d in dates])
    
    df.to_csv(f'{name}.csv', index=False)
    return df

def quick_convert_coordinate(json_data,name):
    coords = json_data['geometry']['coordinates']
    params = json_data['properties']['parameter']
    all_dates = set()
    for param_data in params.values():
        all_dates.update(param_data.keys())
    dates = sorted(list(all_dates))
    
    df = pd.DataFrame([{
        'datetime': datetime.strptime(d, '%Y%m%d%H').strftime('%Y-%m-%d %H:%M:%S'),
        'date': datetime.strptime(d, '%Y%m%d%H').strftime('%Y-%m-%d'),
        'hour': int(d[8:10]),
        'latitude': coords[1],
        'longitude': coords[0],
        'elevation': coords[2] if len(coords) > 2 else None,
        #'wkt_geometry': f"POINT ({coords[0]} {coords[1]})",
        **{var: params[var].get(d, None) for var in params.keys()}  # Use .get() for missing dates
    } for d in dates])
    
    df.to_csv(f'{name}.csv', index=False)
    return df

start="20250101"
end="20250120"
lan=43.47589488154674
lon=-80.5321299441535

url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
params = {
    "start": start,
    "end": end,
    "latitude": lan,
    "longitude": lon,
    "community": "ag",
    "parameters": "T2M",
    "format": "json",
    "units": "metric",
    "user": "T123",
    "header": "true",
    #required for IMERG_PRECLIQUID_PROB
    #"site-elevation": "0",
    #"wind-elevation": "10",
    #"wind-surface": "openwater"
    #wind-surface parameters:
}
headers = {
    "accept": "application/json"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
#print(quick_convert(data,"nasahpdataadvpara"))
print(quick_convert_coordinate(data,"nasahpdatacoordinateadvpara"))
