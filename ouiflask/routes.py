from flask import render_template
from ouiflask import app
from sqlalchemy import create_engine
# import json #Not using yet

USER=***REMOVED***
PASSWORD=***REMOVED***
URI = ***REMOVED***
PORT=***REMOVED***
DB = ***REMOVED***

#The engine stores the log in details used to connect to RDS instance
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

connection = engine.connect() #connects the engine to the database
result = connection.execute("select address, position_lat, position_lng from stations") #stores results from db query

#Adapted from https://www.geeksforgeeks.org/python-convert-list-tuples-dictionary/
#Function to convert SQLAlchemy ResultProxy execute(query) return type into python list = [[add, lat, lng],[...]]
def Convert(myTuple, myList):
    for add, lat, lng in myTuple:
        myList.append([add, lat, lng])
    return myList


myTuple = result
myList = []
result = Convert(myTuple, myList)


# JSON_result = json.dumps(result) #convert list into JSON format (removed for the minute)

connection.close() # Close engine connection to tidy up resources

#Allows access to home.html through the browser by typing either /home or nothing at the end of url
@app.route("/")
@app.route("/home")
def home():
    # Passing the dictionary result into the home.html page as variable results
    return render_template('home.html', results=result)
