import requests
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

def quick_convert(json_data,name):
    params = json_data['properties']['parameter']
    dates = list(params['T2M'].keys())
    
    df = pd.DataFrame([{
        'date': datetime.strptime(d, '%Y%m%d').strftime('%Y-%m-%d'),
        **{var: params[var][d] for var in params.keys()}
    } for d in dates])
    
    df.to_csv(f'{name}.csv', index=False)
    return df

def quick_convert_coordinate(json_data,name):
    coords = json_data['geometry']['coordinates']
    params = json_data['properties']['parameter']
    dates = list(params['T2M'].keys())
    
    df = pd.DataFrame([{
        'date': datetime.strptime(d, '%Y%m%d').strftime('%Y-%m-%d'),
        'latitude': coords[1],
        'longitude': coords[0],
        'elevation': coords[2] if len(coords) > 2 else None,
        #'wkt_geometry': f"POINT ({coords[0]} {coords[1]})",
        **{var: params[var][d] for var in params.keys()}
    } for d in dates])
    
    df.to_csv(f'{name}.csv', index=False)
    return df

start="20251101"
end="20251120"
lan=43.47589488154674
lon=-80.5321299441535

url = "https://power.larc.nasa.gov/api/projection/daily/point"
params = {
    "start": start,
    "end": end,
    "latitude": lan,
    "longitude": lon,
    "community": "ag",
    "parameters": "T2M,T2M_MIN,T2M_MAX,T2MDEW,PRECTOTCORR,RH2M,QV2M,WS10M,ALLSKY_SFC_SW_DWN,ALLSKY_SFC_LW_DWN",
    "format": "json",
    "user": "T123",
    "header": "true",
    "time-standard": "utc",
    "model": "ensemble",
    "scenario": "ssp126"
}
headers = {
    "accept": "application/json"
}
    

response = requests.get(url, params=params)
data = response.json()
print(quick_convert(data,"nasadata"))
print(quick_convert_coordinate(data,"nasadatacoordinate"))
