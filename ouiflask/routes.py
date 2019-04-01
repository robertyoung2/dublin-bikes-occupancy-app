from flask import render_template, request, flash, jsonify, make_response
from ouiflask import app, SQLAlchemyConnection


#Allows access to home.html through the browser by typing either /home or nothing at the end of url
@app.route("/")
@app.route("/home")
def home():
    result = SQLAlchemyConnection.staticQuery()

    return render_template('home.html', results=result)
    

# this route is called by a javascript (AJAX) call
@app.route("/stationDetail", methods=["GET","POST"])
def stationDetail():
    # assign the value stationID from the ajax post
    stationID = request.form['stationID']


    result = SQLAlchemyConnection.dynamicQuery(stationID)
    # return a json object to the front end that can be used by jinja

    return jsonify(result)


# this route is called by a javascript (AJAX) call
@app.route("/bikeGraph", methods=["GET","POST"])
def bikeGraph():

    # assign the value stationID from the ajax post
    stationID = request.form['stationID']

    result = SQLAlchemyConnection.get_station_occupancy_weekly(stationID)
    # return a json object to the front end that can be used by jinja

    return result


@app.route("/getWeather", methods=["POST"])
def getWeather():
    weather = SQLAlchemyConnection.todayWeather()

    return jsonify(weather)