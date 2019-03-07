from flask import render_template, request, flash, jsonify
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
result = connection.execute("select address, position_lat, position_lng, number from stations")

"""
Adapted from https://www.geeksforgeeks.org/python-convert-list-tuples-dictionary/
Function to convert SQLAlchemy ResultProxy execute(query) return type into python list = [[add, lat, lng],[...]]
If details added to the query, make sure to account for them in this function also
This function could auto adjust for extra variables added to query using nested for loop. Implement later
"""
def Convert(myTuple, myList):
    for add, lat, lng, number in myTuple:
        myList.append([add, lat, lng, number])
    return myList


myTuple = result
myList = []
result = Convert(myTuple, myList)


# JSON_result = json.dumps(result) #convert list into JSON format (removed atm as having issues with formatting)

connection.close() # Close engine connection to tidy up resources

"""
@app.route("/stationDetail/<StationID>")
def stationDetail():
    # jinja to transform into jason
    return 
"""



#Allows access to home.html through the browser by typing either /home or nothing at the end of url
@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def home():
    test = "1er"
    return render_template('home.html', results=result, test=test)
    """
    try:
        if request.method == "POST":
            test = "posted"
            flash("posted something")
            stationID = request.form['stationID']
            return render_template('home.html', results=result, test=test, stationIDposted=stationID)
        return render_template('home.html', results=result, test=test)



    except Exception as e:
        test = "excepted"
        flash(e)
    # Passing the list "result" into the home.html page as variable "results"
        return render_template('home.html', results=result, test=test)
    """
# AJAX First comit