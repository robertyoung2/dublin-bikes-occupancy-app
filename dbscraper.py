#!/usr/bin/env python


# Import required libraries
import pandas as pd
import numpy as np
import requests

import json
import time
import os
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import time
from IPython.display import display

NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
APIKEY = ***REMOVED***

URI = ***REMOVED***
DB = ***REMOVED***
PORT=***REMOVED***
USER=***REMOVED***
PASSWORD=***REMOVED***


engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

try:
    r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
    data = json.JSONDecoder().decode(r.text)
    df = pd.DataFrame(data)

    # Check if csv exists, if not, create one
    csv_exists = os.path.isfile('data_backup.csv')
    if not csv_exists:
        print("csv doesn't exist")
        df.to_csv('data_backup.csv',index=False)
    else:
        # Append data to csv file
        print("csv does exist")
        with open('data_backup.csv', 'a') as f:
            df.to_csv(f, header=False,index=False)
        

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
    f= open("logTracebackError.log","a+")
    print(traceback.format_exc())
    f.write(traceback.format_exc())
    f.close() 
    
def stations_to_db(text):
    stations = json.loads(text)
    print(type(stations), len(stations))
    for station in stations:
        print(station)
        vals = (station.get('number'), station.get('last_update'), station.get('bike_stands'), 
                station.get('available_bike_stands'), station.get('available_bikes'), station.get('status'), station.get('banking'))
        try:
            engine.execute("insert into station_status values(%s,%s,%s,%s,%s,%s,%s)", vals)
        except:
            f= open("logTracebackError.log","a+")
            print(traceback.format_exc())
            f.write(traceback.format_exc())
            f.close()
    print("operation complete")
    return

stations_to_db(r.text)