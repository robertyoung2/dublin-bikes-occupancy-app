#!/usr/bin/env python
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
import datetime
import pickle
import os
import ast

URI = ***REMOVED***
DB = ***REMOVED***
PORT = ***REMOVED***
USER = ***REMOVED***
PASSWORD = ***REMOVED***

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)


def sql_query_model():
    """
    Function to get the latest information from the Dublin Bikes and Weather database and then
    merge the two together, with sampling/averaging for the weather.
    :return: a dataframe which is the combined DB and Weather database
    """

    conn = engine.connect()

    sql1 = """SELECT number, date_format(CAST(last_update AS DATETIME), '%%Y-%%m-%%d %%H' ) as myDate, AVG(available_bike_stands) as available_bike_stands, AVG(available_bikes) as available_bikes
            FROM station_status
            GROUP BY number, myDate
            ORDER BY myDate ASC;"""

    df1 = pd.read_sql_query(sql1, conn)
    df1['myDate'] = pd.to_datetime(df1.myDate, unit='ns')
    df1['myDate'] = df1.myDate.map(lambda x: x.replace(minute=0, second=0))

    sql2 = """SELECT date_format(CAST(last_update AS DATETIME), '%%Y-%%m-%%d %%H' ) as myDate, main_weather, (AVG(`main.temp`) -273.15) as main_temp, AVG(rainfall_mm) as rainfall_mm, AVG(`wind.speed`) as wind_speed
            FROM current_weather
            GROUP BY myDate
            ORDER BY myDate ASC;"""

    df2 = pd.read_sql_query(sql2, conn)
    df2['myDate'] = pd.to_datetime(df2.myDate, unit='ns')
    df2['myDate'] = df2.myDate.map(lambda x: x.replace(minute=0, second=0))

    df3 = pd.merge(df1, df2, on='myDate')

    for index, row in df3.iterrows():
        if df3.loc[index, 'myDate'].hour == 0:
            df3.loc[index, 'myDate'] = df3.loc[index, 'myDate'] - datetime.timedelta(
                minutes=(df3.loc[index, 'myDate'].minute + 1))
            df3.loc[index, 'hour'] = 24
        else:
            df3.loc[index, 'hour'] = (df3.loc[index, 'myDate'].hour)

    df3['weekday'] = df3['myDate'].dt.day_name()

    df3.set_index('myDate', inplace=True)

    return df3


def performance_metric(y_true, y_predict):
    """Calculates and returns the performance score between
    true and predicted values based on the metric chosen.

    :param y_true: y true value
    :param y_predict: y predicted value
    :return: score
    """
    score = r2_score(y_true, y_predict)

    return score


def fit_model(X, y,models_score_dict, key_name):
    """ Fits the model using a decision tree regressor. Grid search is implemented for
    hyper parameter tuning and best model selection. Time series is used for cross validation. The split is made on 20
    as there are 20 hours per day (hours 01:00, 02:00, 03:00 and 04:00 are not included. Returns the
    best estimator parameters for use in creating the pickle file and updating the best score dict.

    :param X: Dataframe of predictors
    :param y: Dataframe of target values
    :param models_score_dict: Dictionary which records all models best score
    :param key_name: Model name for dict loop up, eg 'model_114_Thursday'
    :return: returns the best model estimator parameters
    """
    n_splits = int(len(X) / 20)

    cv_sets = TimeSeriesSplit(n_splits)

    regressor = DecisionTreeRegressor()

    params = {'max_depth': range(1, 11)}

    scoring_fnc = make_scorer(performance_metric)

    grid = GridSearchCV(regressor, params, scoring=scoring_fnc, cv=cv_sets)

    grid = grid.fit(X, y)

    best_score = grid.best_score_

    if key_name not in models_score_dict or models_score_dict[key_name] < best_score:
        models_score_dict[key_name] = best_score
        f = open('pickle_files/models_score_dict.txt', "w")
        f.write(str(models_score_dict))
        f.close()
        return grid.best_estimator_

    return grid.best_estimator_


def station_day_model(station_number, day_week, df_current, features):
    """ Function that creates a data frame for the given week day and station number. Ensures Whole days
    only are included in the data frame. Creates the file name for the pickle model. Checks the previous
    model best score versus the current model best score. If higher, updates the pickel model.

    :param station_number: current station number
    :param day_week: current day of the week
    :param df_current: data frame for model work
    :param features: list of features to be used for model
    :return: Void. Updates pickle models.
    """

    df_current = df_current[df_current['weekday'] == day_week]
    df_current = df_current[df_current['number'] == station_number]

    break_case = datetime.time(23, 59, 0)
    df_temp = df_current

    for index, row in df_current[::-1].iterrows():
        if index.time() == break_case:
            break
        else:
            df_temp = df_temp.drop(index)

    df_current = df_temp
    X = df_current[features]
    y = df_current.available_bikes

    file_name = "model_" + str(station_number) + "_" + day_week + ".pkl"
    key_name = file_name[:-4]

    f = open('pickle_files/models_score_dict.txt', "r")
    models_score_dict = f.read()
    models_score_dict = ast.literal_eval(models_score_dict)
    f.close()

    if key_name in models_score_dict:
        previous_best_score = models_score_dict[key_name]
    else:
        previous_best_score = -9999999

    reg = fit_model(X, y, models_score_dict, key_name)

    f = open('pickle_files/models_score_dict.txt', "r")
    models_score_dict = f.read()
    models_score_dict = ast.literal_eval(models_score_dict)
    f.close()

    current_best_score = models_score_dict[key_name]

    if previous_best_score < current_best_score:
        with open("pickle_files/" + file_name, 'wb') as handle:
            pickle.dump(reg, handle, pickle.HIGHEST_PROTOCOL)


def create_models(station_array,df_db, features):
    """
    Loops through each station number and day of the week for model creation.
    :param station_array: list of all valid station numbers
    :param df_db: dataframe of all database data to be manipulated
    :param features: features to be used for model training
    :return: Void. Updates pickle models.
    """
    days =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for station_number in station_array:
        for day_week in days:
            station_day_model(station_number, day_week, df_db,features)


def start_modelling():
    """
    Initial function. First calls SQL query to generate the dataframe from the databases. Creates a list
    with each unique station number. Converts all the categorical weather features to binary features for
    the purpose of modelling. Creates a df filtered by the desired features to be used for modelling.
    Makes a directory for the pickle files if it does not exist. Creates the mode best score dictionary if it does
    not exist. Calls the function to start the modelling process.
    :return:
    """

    # Download latest sql info
    df_db = sql_query_model()

    # Creates an array with every unique station number
    station_array = sorted(df_db.number.unique())

    # Make categorical info into binary
    main_weather_dummies = pd.get_dummies(df_db['main_weather'], prefix="main_weather")

    additional_main_weathers = ['main_weather_Thunderstorm', 'main_weather_Haze', 'main_weather_Squall',
                                'main_weather_Smoke', 'main_weather_Dust', 'main_weather_Tornado',
                                'main_weather_Ash']

    # This is ensuring that the order in which the model was originally trained is preserved
    # This is to allow for the reordering of data frame columns in the for loop below as new weather descriptions are
    # added to the database history
    categ_features = ['main_weather_Clouds', 'main_weather_Clear', 'main_weather_Rain', 'main_weather_Fog',
                      'main_weather_Drizzle', 'main_weather_Mist', 'main_weather_Snow'] + additional_main_weathers
    cont_features = ['hour', 'rainfall_mm', 'main_temp']

    features = cont_features + categ_features
    df_db = pd.concat([df_db, main_weather_dummies], axis=1)
    df_db = df_db.drop('main_weather', axis=1)

    for weather_descriptor in additional_main_weathers:
        if (weather_descriptor) not in df_db.columns:
            df_db[weather_descriptor] = 0

    # define the name of the directory to be created
    path_pickle = "pickle_files"

    if not os.path.exists(path_pickle):
        try:
            os.mkdir(path_pickle)
        except OSError:
            print ("Creation of the directory %s failed" % path_pickle)
        else:
            print ("Successfully created the directory %s " % path_pickle)

    path_pickle_file = 'pickle_files/models_score_dict.txt'

    if not os.path.isfile(path_pickle_file):
        dict = {}
        f = open(path_pickle_file, "w")
        f.write(str(dict))
        f.close()

    # Make all the models
    create_models(station_array, df_db, features)


start_modelling()

