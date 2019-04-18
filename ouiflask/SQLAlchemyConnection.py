from sqlalchemy import create_engine
from sqlalchemy.sql import column, text
from functools import lru_cache

# set up all the information to access the RDS
USER=***REMOVED***
PASSWORD=***REMOVED***
URI = ***REMOVED***
PORT=***REMOVED***
DB = ***REMOVED***

#The engine stores the log in details used to connect to RDS instance
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

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
    print("results:", result)

    return result

def Convert(myTuple, myList):
    for add, lat, lng, number, available_bikes, available_bike_stands in myTuple:
        myList.append([add, lat, lng, number, available_bikes, available_bike_stands])
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
    result = connection.execute(sql)

    d=dict()
    for row in result:
        d["last_update"]=row["last_update"]
        d["description"]=row["description"]
        d["icon"]=row["icon"]
        d["temp"]=row["main.temp"]

    connection.close()
    
    return d 


def dynamicQuery(stationID):

    connection = engine.connect()  
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