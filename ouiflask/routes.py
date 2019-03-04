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

"""
SQL query to get data from RDS db stations table
To populate more details on the InfoWindow, add them to query here
"""
result = connection.execute("select address, position_lat, position_lng from stations")

"""
Adapted from https://www.geeksforgeeks.org/python-convert-list-tuples-dictionary/
Function to convert SQLAlchemy ResultProxy execute(query) return type into python list = [[add, lat, lng],[...]]
If details added to the query, make sure to account for them in this function also
This function could auto adjust for extra variables added to query using nested for loop. Implement later
"""
def Convert(myTuple, myList):
    for add, lat, lng in myTuple:
        myList.append([add, lat, lng])
    return myList


myTuple = result
myList = []
result = Convert(myTuple, myList)


# JSON_result = json.dumps(result) #convert list into JSON format (removed atm as having issues with formatting)

connection.close() # Close engine connection to tidy up resources

#Allows access to home.html through the browser by typing either /home or nothing at the end of url
@app.route("/")
@app.route("/home")
def home():
    # Passing the list "result" into the home.html page as variable "results"
    return render_template('home.html', results=result)
