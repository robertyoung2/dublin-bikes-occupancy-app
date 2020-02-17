#!/usr/bin/env python

# Import required libraries
import pandas as pd
import requests
import json
from sqlalchemy import create_engine
import traceback
import os
import datetime

NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
API_KEY = ***REMOVED***

URI = ***REMOVED***
DB = ***REMOVED***
PORT = ***REMOVED***
USER = ***REMOVED***
PASSWORD = ***REMOVED***

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

def stations_to_db(df):
    """Connect to RDS database"""
    try:
        df.to_sql('station_status', con=engine, if_exists='append', index=False)
    except:
        f= open("logTracebackError.log", "a+")
        print(traceback.format_exc())
        f.write(traceback.format_exc())
        f.close()
        print("operation complete")
    return

try:
    r = requests.get(STATIONS, params={"apiKey": API_KEY, "contract": NAME})
    data = json.JSONDecoder().decode(r.text)
    df = pd.DataFrame(data)
    df = df.drop(columns=['bonus', 'address', 'contract_name', 'position', 'name'], axis=1)
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df['last_update'] = str(currentDT)
    stations_to_db(df)

    # Check if csv exists, if not, create one
    csv_exists = os.path.isfile('data_backup.csv')
    if not csv_exists:
        print("csv doesn't exist")
        df.to_csv('data_backup.csv', index=False)
    else:
        # Append data to csv file
        print("csv does exist")
        with open('data_backup.csv', 'a') as f:
            df.to_csv(f, header=False, index=False)

    # Check if text file exists, if not, create one
    text_exists = os.path.isfile('data.txt')
    if not text_exists:
        print("txt doesn't exist")
        with open('data.txt', 'w') as outfile:  
            json.dump(data, outfile)
    else:
        # Append data to txt
        print("txt does exist")
        with open('data.txt', 'a') as outfile:
            json.dump(data, outfile)
except:
    f = open("logTracebackError.log", "a+")
    print(traceback.format_exc())
    f.write(traceback.format_exc())
    f.close()
