from sqlalchemy import create_engine


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
    result = connection.execute("select address, position_lat, position_lng, number from stations")

    connection.close() # Close engine connection to tidy up resources

    myTuple = result
    myList = []
    result = Convert(myTuple, myList)

    return result

def Convert(myTuple, myList):
    for add, lat, lng, number in myTuple:
        myList.append([add, lat, lng, number])
    return myList

    





# result = convert_ResultProxy_to_Array(result)


# JSON_result = json.dumps(result) #convert list into JSON format (removed atm as having issues with formatting)





def dynamicQuery(stationID):

    connection = engine.connect()  # connects the engine to the database

    """
    SQL query to get data from RDS db stations table
    To populate more details on the InfoWindow, add them to query here
    """
    sql = ("SELECT last_update, available_bike_stands, available_bikes, name "
                                "FROM station_status, stations "
                                "WHERE station_status.number = "+ stationID + " and station_status.number = stations.number "
                                "ORDER BY last_update DESC LIMIT 1")
    try:
        result = connection.execute(sql)
        result = convert_ResultProxy_to_Array(result)
        connection.close() # Close engine connection to tidy up resources
    except Exception as e:
        result = e
    return result

def convert_ResultProxy_to_Array(resultProxy):
    """
    Adapted from https://www.geeksforgeeks.org/python-convert-list-tuples-dictionary/
    Function to convert SQLAlchemy ResultProxy execute(query) return type into python list = [[add, lat, lng],[...]]
    If details added to the query, make sure to account for them in this function also
    This function could auto adjust for extra variables added to query using nested for loop. Implement later
    """

    newArray = []
    for row in resultProxy:
        for element in row:
            newArray.append(element)
    return newArray