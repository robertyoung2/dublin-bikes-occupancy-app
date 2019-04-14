from sqlalchemy import create_engine
from sqlalchemy.sql import column, text
from functools import lru_cache
import pandas as pd
from datetime import timedelta, datetime, time
import math
from flask import jsonify
import pickle


USER=***REMOVED***
PASSWORD=***REMOVED***
URI = ***REMOVED***
PORT=***REMOVED***
DB = ***REMOVED***

#The engine stores the log in details used to connect to RDS instance
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

@lru_cache(maxsize=128)
def staticQuery():
    connection = engine.connect() #connects the engine to the database

    """
    SQL query to get data from RDS db stations table
    To populate more details on the InfoWindow, add them to query here
    """
    result = connection.execute("""SELECT DISTINCT address, position_lat, position_lng, station_status.number, available_bikes, available_bike_stands
                                    FROM stations, station_status
                                    WHERE station_status.number = stations.number 
                                        AND `last_update` BETWEEN DATE_SUB(NOW() , INTERVAL 6 MINUTE) AND NOW()
                                    ORDER BY last_update DESC;""")

    connection.close() # Close engine connection to tidy up resources

    myTuple = result
    myList = []
    result = Convert(myTuple, myList)

    return result

def Convert(myTuple, myList):
    for add, lat, lng, number, available_bikes, available_bike_stands in myTuple:
        myList.append([add, lat, lng, number, available_bikes, available_bike_stands])
    # print()
    # print(myList)
    # print()
    return myList

    
def todayWeather():
    connection = engine.connect()

    sql = text("SELECT last_update, description, icon , `main.temp`"
               "FROM current_weather "
               "ORDER BY last_update DESC LIMIT 1")

    sql = sql.columns(
            column('last_update'),
            column('description'),
            column('icon'),
            column('main.temp')
        )

    # print("Before Query")
    result = connection.execute(sql)
    # print("After Query")

    d=dict()
    for row in result:
        d["last_update"]=row["last_update"]
        d["description"]=row["description"]
        d["icon"]=row["icon"]
        d["temp"]=row["main.temp"]

    connection.close()
    
    return d 




# result = convert_ResultProxy_to_Array(result)


# JSON_result = json.dumps(result) #convert list into JSON format (removed atm as having issues with formatting)





def dynamicQuery(stationID):

    connection = engine.connect()  # connects the engine to the database

    """
    SQL query to get data from RDS db stations table
    To populate more details on the InfoWindow, add them to query here
    """
    sql = text("SELECT last_update, available_bike_stands, available_bikes, name "
                                "FROM station_status, stations "
                                "WHERE station_status.number = "+ stationID + " and station_status.number = stations.number "
                                "ORDER BY last_update DESC LIMIT 1")

    sql = sql.columns(
            column('last_update'),
            column('available_bike_stands'),
            column('available_bikes'),
            column('name')
        )
    try:
        result = connection.execute(sql)

        d=dict()

        for row in result:
            d["last_update"]=row["last_update"]
            d["available_bike_stands"]=row["available_bike_stands"]
            d["available_bikes"]=row["available_bikes"]
            d["name"]=row["name"]

        connection.close() # Close engine connection to tidy up resources
    except Exception as e:
        result = e
        return result

    return d



# def get_station_occupancy_weekly_daily(station_id):
#     days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#     average_bikes_per_day = []
#     average_bikes_per_hour = []
#
#     for day in days:
#         hourly = []
#         with open('/Users/conor/Desktop/COMP30830_Group_Project/oui-team/ouiflask/pickle_files/' + 'model_' + str(station_id) + '_' + day + '.pkl', 'rb') as handle:
#             rob_model = pickle.load(handle)
#
#         for i in range(24):
#             # Run scraper here for weather prediction and use robs dummy encoding to format (maybe do it outside look and loop through data, more efficient?)
#             result = math.ceil(rob_model.predict([[i, 0, 5, 1, 0, 0, 0, 0, 0]]))
#             hourly.append([i, result])
#
#         average_bikes_per_hour.append(hourly)
#
#     dayIndex = 0
#     for day in average_bikes_per_hour:
#         average_bikes = 0
#         for hour in day:
#             average_bikes += hour[1]
#         average_bikes = round(average_bikes / len(day))
#         average_bikes_per_day.append(average_bikes)
#         dayIndex += 1
#
#     combined_list = [average_bikes_per_day, average_bikes_per_hour]
#
#     return jsonify(combined_list)

