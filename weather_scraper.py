#!/usr/bin/env python

import json
import pandas as pd
import requests
from sqlalchemy import create_engine
import traceback
import os
import datetime
from bs4 import BeautifulSoup

# API weather URI for city ID "Dublin, IE"
api_url_base_weather = ***REMOVED***
api_token_weather = ***REMOVED***

# Database access details
URI = ***REMOVED***
DB = ***REMOVED***
PORT = ***REMOVED***
USER = ***REMOVED***
PASSWORD = ***REMOVED***

# Use sqlalchemy to log into the database
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)


# Function to connect to Amazon RDS and upload dataframe to database
def weather_to_db(df):
    try:
        df.to_sql('current_weather', con=engine, if_exists='append', index=False)
    except:
        f= open("logTracebackError.log", "a+")
        print(traceback.format_exc())
        f.write(traceback.format_exc())
        f.close()
        print("operation complete")
    return

try:
    # Pull json data with api token provided above
    r = requests.get(api_url_base_weather, params={"APPID": api_token_weather})

    # Decode json to a text format
    data_weather = json.JSONDecoder().decode(r.text)

    # JSON data is nested, normalize it
    df = pd.io.json.json_normalize(data_weather)

    # take a date-time stamp to add to the dataframe
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add the time stamp to the dataframe
    df['last_update'] = str(currentDT)

    # Split out the weather data array into individual new columns
    df['description'] = df['weather'][0][0]['description']
    df['main_weather'] = df['weather'][0][0]['main']
    df['icon'] = df['weather'][0][0]['icon']
    df['weather_id'] = df['weather'][0][0]['id']

    # Dropped internal system and static data https://openweathermap.org/weather-data
    df = df.drop(['weather', 'base', 'coord.lat', 'coord.lon', 'sys.country', 'sys.message', 'sys.id', 'sys.type',
                  'name'], axis=1)

    # List of openweathermap optional api parameters
    optional_list = ['rain.1h', 'rain.3h', 'snow.1h', 'snow.3h', 'wind.gust']

    #If optional api item is in the list, drop it
    for api_item in optional_list:
        if api_item in df:
            df = df.drop([api_item], axis=1)

    # Access met weather (for rainfall in mm) data html table and convert into data frame
    df_rainfall = pd.read_html('https://www.met.ie/latest-reports/observations', header=1)[0]

    df_rainfall.columns = ['Location',
                           'Dir',
                           'Speed Kts(Km/h)',
                           'Gust Kts(Km/h)',
                           'Weather',
                           'oC',
                           '(%)',
                           '(mm)',
                           '(hPa)']

    # Drop columns that will not be used
    df_rainfall = df_rainfall.drop(['Dir', 'Speed Kts(Km/h)',
                                       'Gust Kts(Km/h)', 'oC', '(%)', '(hPa)'], axis=1)
    # Filter location to Dublin for new df
    df_rainfall = df_rainfall.loc[df_rainfall['Location'] == 'Dublin']

    # Add rainfall column to existing core dataframe
    df['rainfall_mm'] = df_rainfall['(mm)'].values

    # Send the data frame to the RDS database table "current_weather"
    weather_to_db(df)

    # Check if csv exists, if not, create one
    csv_exists = os.path.isfile('data_backup_weather.csv')
    if not csv_exists:
        print("csv doesn't exist")
        df.to_csv('data_backup_weather.csv', index=False)
    else:
        # Append data to csv file
        print("csv does exist")
        with open('data_backup_weather.csv', 'a') as f:
            df.to_csv(f, header=False, index=False)

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

# Error logging should data pull fail for any reason
except:
    f = open("logTracebackError.log", "a+")
    print(traceback.format_exc())
    f.write(traceback.format_exc())
    f.close()


