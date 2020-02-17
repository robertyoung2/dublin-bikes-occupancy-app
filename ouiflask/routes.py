from flask import render_template, request, jsonify
from ouiflask import app, SQLAlchemyConnection, getPredictions

@app.route("/")
@app.route("/home")
def home():
    # result contain the address of all the station and  available bikes to build the google map when the page load.
    result = SQLAlchemyConnection.staticQuery()
    return render_template('home.html', results=result)

@app.route("/stationDetail", methods=["GET","POST"])
def stationDetail():
    """
    Retrieves the station ID from the front end
    Returns a json object containing dynamic station information to populate station infowindow
    """
    stationID = request.form['stationID']
    result = SQLAlchemyConnection.dynamicQuery(stationID)
    return jsonify(result)

@app.route("/bikeGraph", methods=["GET","POST"])
def bikeGraph():
    """
    Passes necessary data to the prediction model and returns the result to the front end in the format needed to
    populate the charts
    :return:
    """
    stationID = request.form['stationID']
    maxBikes = int(request.form['maxBikes'])
    name = request.form['station_name']
    result = getPredictions.predict(stationID, maxBikes, name)
    return result


@app.route("/getWeather", methods=["POST"])
def getWeather():
    """
    Returns the current weather to the front end in JSON format
    """
    weather = SQLAlchemyConnection.todayWeather()
    return jsonify(weather)
