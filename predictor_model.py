# Library Imports.
import pandas as pd

from patsy import dmatrices
from sqlalchemy import create_engine
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
import datetime
import pickle
import os

URI = ***REMOVED***
DB = ***REMOVED***
PORT = ***REMOVED***
USER = ***REMOVED***
PASSWORD = ***REMOVED***

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)


def sql_query_model():
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

    df3['weekday'] = df3['myDate'].dt.day_name()
    df3['hour'] = (df3['myDate'].dt.hour)

    df3.set_index('myDate', inplace=True)

    return df3


def performance_metric(y_true, y_predict):
    """ Calculates and returns the performance score between
        true and predicted values based on the metric chosen. """

    score = r2_score(y_true, y_predict)
    # Return the score
    return score


def fit_model(X, y):
    n_splits = int(len(X) / 20)

    cv_sets = TimeSeriesSplit(n_splits)

    regressor = DecisionTreeRegressor()

    params = {'max_depth': range(1, 11)}

    scoring_fnc = make_scorer(performance_metric)

    grid = GridSearchCV(regressor, params, scoring=scoring_fnc, cv=cv_sets)

    grid = grid.fit(X, y)

    # Add in previous model and current model best score logic
    # (grid.best_score_)

    # Return the optimal model after fitting the data
    return grid.best_estimator_


def station_day_model(station_number, day_week, df_current, features):
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

    reg = fit_model(X, y)

    file_name = "model_" + str(station_number) + "_" + day_week + ".pkl"

    with open("pickle_files/" + file_name, 'wb') as handle:
        pickle.dump(reg, handle, pickle.HIGHEST_PROTOCOL)


def create_models(station_array,df_db, features):
    days =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for station_number in station_array:
        for day_week in days:
            station_day_model(station_number, day_week, df_db,features)

def start_modelling():

    # Download latest sql info
    df_db = sql_query_model()

    # Creates an array with every unique station number
    station_array = sorted(df_db.number.unique())

    # Make categorical info into binary
    main_weather_dummies = pd.get_dummies(df_db['main_weather'], prefix="main_weather",drop_first = True)

    categ_features = main_weather_dummies.columns.values.tolist()
    cont_features = ['hour', 'rainfall_mm', 'main_temp']

    features = cont_features + categ_features

    df_db = pd.concat([df_db, main_weather_dummies], axis=1)
    df_db = df_db.drop('main_weather', axis = 1)

    # define the name of the directory to be created
    path = "pickle_files"

    if os.path.exists(path) == False:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

    # Make all the models
    create_models(station_array,df_db,features)

start_modelling()