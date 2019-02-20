#!/usr/bin/env python


# Import required libraries
import pandas as pd
import numpy as np
import requests
import json
import time
import os
import traceback

NAME="Dublin"
STATIONS="https://api.jcdecaux.com/vls/v1/stations"
APIKEY='insert_key_here'

try:
    r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
    data = json.JSONDecoder().decode(r.text)
    df = pd.DataFrame(data)

    # Check if csv exists, if not, create one
    csv_exists = os.path.isfile('data_backup.csv')
    if not csv_exists:
        df.to_csv('data_backup.csv',index=False)

    # Check if text file exists, if not, create one
    text_exists = os.path.isfile('data.txt')
    if not text_exists:
        with open('data.txt', 'w') as outfile:  
            json.dump(data, outfile)

    # Append data to csv
    with open('data_backup.csv', 'a') as f:
        df.to_csv(f, header=False,index=False)

    # Append data to text file
    with open('data.txt', 'a') as outfile:
        json.dump(data, outfile)
except:
    f= open("logTracebackError.log","a+")
    print(traceback.format_exc())
    f.write(traceback.format_exc())
    f.close() 