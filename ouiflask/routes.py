from flask import render_template, request, jsonify
from ouiflask import app, SQLAlchemyConnection, getPredictions

@app.route("/")
@app.route("/home")
def home():
    # result contain the address of all the station and also the available bikes to build the google map when the page load.
    result = SQLAlchemyConnection.staticQuery()
    return render_template('home.html', results=result)

@app.route("/stationDetail", methods=["GET","POST"])
def stationDetail():
    # retrive the station ID from the front end.
    stationID = request.form['stationID']
    result = SQLAlchemyConnection.dynamicQuery(stationID)
    # return a json object to the front end that can be used JavaScript
    return jsonify(result)

@app.route("/bikeGraph", methods=["GET","POST"])
def bikeGraph():
    stationID = request.form['stationID']
    maxBikes = int(request.form['maxBikes'])
    name = request.form['station_name']
    # use the prediction model to return the predicted available bikes to the front end.
    result = getPredictions.predict(stationID, maxBikes, name)
    return result


@app.route("/getWeather", methods=["POST"])
def getWeather():
    weather = SQLAlchemyConnection.todayWeather()
    # return the weather of the day to the front end.
    return jsonify(weather)

