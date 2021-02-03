# Oui Bikes - A Dublin Bikes Application
#### ReadMe Authored by - Robert Young

"Oui Bikes" is an application for the popular bike rental scheme "Dublin Bikes", which is based in Dublin, Ireland. The app is built using the Flask framework. To gather the required information for the application, the Dublin Bikes API and Open Weather API were scraped over a number of months and stored in a database.
This information was used to populate the application and to allow the training and implementation of a Machine Learning model which predicted the expected available bikes at a given station on a day of the week, hour-by-hour.

If you wish to see how many bikes will be available in the future, say you want to get a bike at 8am on a Tuesday, you can click on a day of the week to get an hour-by-hour break down of the day and a prediction for available bikes and vacant bike slots at the given station. Real time bike availability can also be viewed quickly and easily view the implementation of a bike station marker heat-icon.

## Scripts and Notebooks

* Main Flask application can be viewed in the directory: [ouiflask](https://github.com/robertyoung2/dublin-bikes-occupancy-app/tree/master/ouiflask).
* Data Analysis and Predictive Model Training can be seen: [here](https://github.com/robertyoung2/dublin-bikes-occupancy-app/blob/master/Machine-Learning-Predictive-Model.ipynb).
* Dublin Bikes webscraper: [dbscraper.py](https://github.com/robertyoung2/dublin-bikes-occupancy-app/blob/master/dbscraper.py).
* The Open Weather webscraper: [weather_scraper.py](https://github.com/robertyoung2/dublin-bikes-occupancy-app/blob/master/weather_scraper.py).
* The Machine Learning predictor model: [predictor_model.py](https://github.com/robertyoung2/dublin-bikes-occupancy-app/blob/master/predictor_model.py).

## Documentation

For security reasons, all passwords and user names in the codebase have been redacted. No access to the database is provided.

The additional packages required to create and run this application are as follows:

* flask
* scikit-learn
* pandas
* numpy (installed as part of scikit-learn)
* requests
* jsonschema
* sqlalchemy
* jupyter
* PyMySQL

## How the App Works

The backend of the application is managed through the Python framework Flask. A MySql database is hosted on RDS and proivides current and historical bike station information and weather data. The front end is constructued through Javascript. A total of 793 machine learning models exits, one for each bike station for each day of the week (113 bike stations * 7 days of the week). These have been serialised into pickle files. Every five minutes a web scraper is run which accesses the JCDecaux API (Dublin Bikes) and stores the information for each bike station in the database. This scraper also collects the current weather data from the Open Weather API, but the frequency of this collection is every half hour, due to weather not updating as frequently. 

Training of the ML models occurs once a week, as one more week of additional information has been gathered. If any of the new models result in a lower error loss, the previous model is replaced with the new model. When using the app to predict, the following information is provided to the ML model for prediction:

* Which day of the week and bike station is requested (this provides the model to be selected).
* The hour of the day, eg. 15:15 -> 15.
* The current weather conditions: rainfall in mm, temperature in C, and weather descriptor, such as 'Clouds'.

With this inputs, a prediction is made for how many bikes will be available for the selected hourly time period. 

## Known Issues

* Graph sizing issue on larger screens (does not fill the screen in the map, causes resolution issues)
* Need to add and check for the creation of new bike stations, and have these auto-populate the static database
* Compatability issues with jquery in Firefox browser: " Using //@ to indicate sourceMappingURL pragmas is deprecated. Use //# instead"
