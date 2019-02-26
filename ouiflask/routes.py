from flask import render_template, url_for, flash, redirect
from ouiflask import app

GOOGLE_MAP_API_KEY = 'AIzaSyCaKjODpgATcORSqO1bYUWY2V29zTv7r40'

@app.route("/")
@app.route("/home")
def home(googleApiKey=GOOGLE_MAP_API_KEY):
    return render_template('home.html', googleApiKey=googleApiKey)
