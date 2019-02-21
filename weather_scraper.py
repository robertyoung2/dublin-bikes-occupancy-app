
import json
import pandas as pd
import numpy as numpy
import requests
import os

api_url_base_weather = ***REMOVED***
api_token_weather = ***REMOVED***
r = requests.get(api_url_base_weather, params={"APPID": api_token_weather})

data_weather = json.JSONDecoder().decode(r.text)

df = pd.io.json.json_normalize(data_weather)

# Split out the weather data array into individual new columns
df['description'] = df['weather'][0][0]['description']
df['main_weather'] = df['weather'][0][0]['main']
df['icon'] = df['weather'][0][0]['icon']
df['weather_id'] = df['weather'][0][0]['id']

# Drop the weather column and base column
df = df.drop(['weather','base'], axis=1)

# Check if csv exists, if not, create one
csv_exists = os.path.isfile('data_backup_weather.csv')
if not csv_exists:
    print("csv doesn't exist")
    df.to_csv('data_backup_weather.csv',index=False)
else:
    # Append data to csv file
    print("csv does exist")
    with open('data_backup_weather.csv', 'a') as f:
        df.to_csv(f, header=False,index=False)
    
# Check if text file exists, if not, create one
text_exists = os.path.isfile('data_weather.txt')
if not text_exists:
    print("txt doesn't exist")
    with open('data_weather.txt', 'w') as outfile:  
        json.dump(data_weather, outfile)
else:
    # Append data to txt
    print("txt does exist")
    with open('data_weather.txt', 'a') as outfile:
        json.dump(data_weather, outfile)

