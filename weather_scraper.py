#!/usr/bin/env python

import json
import pandas as pd
import requests
from sqlalchemy import create_engine
import traceback
import os
import datetime

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

    # Access met weather (for rainfall in mm) data html table and convert into data frame
    df_rainfall = pd.read_html('https://www.met.ie/latest-reports/observations', header=1)[0]

    # Rename the columns from the Met Eireann HTML table as EC2 not accept otherwise
    df_rainfall.columns = ['Location',
                           'Dir',
                           'Speed Kts(Km/h)',
                           'Gust Kts(Km/h)',
                           'Weather',
                           'oC',
                           '(%)',
                           '(mm)',
                           '(hPa)']

    # Filter location to Dublin for new df
    df_rainfall = df_rainfall.loc[df_rainfall['Location'] == 'Dublin']

    # Add rainfall column to existing core dataframe
    df['rainfall_mm'] = df_rainfall['(mm)'].values

    # Create a new dataframe to be pushed to the database
    df_to_database = pd.DataFrame()

    # List of existing dataframe columns
    database_columns = ['last_update', 'clouds.all', 'cod', 'id', 'description', 'main_weather', 'main.temp',
                        'rainfall_mm', 'main.humidity', 'main.pressure', 'visibility', 'wind.speed', 'wind.deg',
                        'main.temp_max', 'main.temp_min', 'sys.sunrise', 'sys.sunset', 'dt', 'icon', 'weather_id']

    # Create a new database using only the column names that exist in the database
    for names in database_columns:
        if names in df.columns:
            df_to_database[names] = df[names]
        else:
            df_to_database[names] = None

    # Send the data frame to the RDS database table "current_weather"
    weather_to_db(df_to_database)

    # Rebase database for backup purposes
    df = df_to_database

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