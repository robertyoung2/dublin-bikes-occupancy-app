import json
from flask import jsonify
import pandas as pd
import requests
from datetime import timedelta, datetime
import pickle
import math
# You need to change the absolute path of the pickle_files to make this code work.

def get_dates(days_to_add):

    dates_array = []
    current_date = datetime.now().date()
    for i in range(0, days_to_add + 1):
        dates_array.append([current_date, current_date.strftime("%A")])
        current_date = current_date + timedelta(days=1)

    return dates_array


def choose_nearest_datetime(datetime_options, selected_datetime):
    return min(datetime_options, key=lambda x: abs(x - selected_datetime))


def predict(station_id, maxBikes, name):
    # this function return a json object containing the predicted number of bikes (weekly and hourly prediction) for the folowing 5 days.

    days = get_dates(5)
    average_bikes_per_day = []
    average_bikes_per_hour = []
    df = scrape_forecast_weather()
    items = []
    predictedDays = []

    for forecast in df['list'][0]:
        items.append(pd.to_datetime(forecast["dt_txt"], unit='ns'))

    for day in days:
        hourly = []
        predictedDays.append(day[1])
        with open("C:\\Users\\Arnaud\\Desktop\\UCD\\SoftEngineering\\oui-team\\ouiflask\\pickle_files\\" + 'model_' + str(station_id) + '_' + day[1] + '.pkl', 'rb') as handle:
            rob_model = pickle.load(handle)

        for pred_time in range(24):
            pred_date = day[0]
            weather_prediction_df = getFormattedWeatherData(pred_date, pred_time, df, items)

            result = math.ceil(rob_model.predict([[pred_time, weather_prediction_df['temp'],
                                                   weather_prediction_df['rain_mm'],
                                                   weather_prediction_df['main_weather_Clouds'],
                                                   weather_prediction_df['main_weather_Clear'],
                                                   weather_prediction_df['main_weather_Rain'],
                                                   weather_prediction_df['main_weather_Fog'],
                                                   weather_prediction_df['main_weather_Drizzle'],
                                                   weather_prediction_df['main_weather_Mist'],
                                                   weather_prediction_df['main_weather_Snow'],
                                                   weather_prediction_df['main_weather_Thunderstorm'],
                                                   weather_prediction_df['main_weather_Haze'],
                                                   weather_prediction_df['main_weather_Squall'],
                                                   weather_prediction_df['main_weather_Smoke'],
                                                   weather_prediction_df['main_weather_Dust'],
                                                   weather_prediction_df['main_weather_Tornado'],
                                                   weather_prediction_df['main_weather_Ash']]]))

            if result < 0:
                result = 0
            elif result > maxBikes:
                result = maxBikes

            hourly.append([pred_date, result])

        average_bikes_per_hour.append(hourly)

    dayIndex = 0
    for day in average_bikes_per_hour:
        average_bikes = 0
        for hour in day:
            average_bikes += hour[1]
        average_bikes = round(average_bikes / len(day))
        average_bikes_per_day.append(average_bikes)
        dayIndex += 1

    combined_list = [average_bikes_per_day, average_bikes_per_hour, predictedDays, name]

    return jsonify(combined_list)


def scrape_forecast_weather():
    # return a panda dataframe containing the forecast weather of the next 5 days.

    # API weather URI for city ID "Dublin, IE"
    api_url_base_weather = 'http://api.openweathermap.org/data/2.5/forecast?id=7778677'
    api_token_weather = ***REMOVED***

    # Pull json data with api token provided above
    r = requests.get(api_url_base_weather, params={"APPID": api_token_weather})

    # Decode json to a text format
    data_weather = json.JSONDecoder().decode(r.text)

    # JSON data is nested, normalize it
    df = pd.io.json.json_normalize(data_weather)

    return df


def getFormattedWeatherData(selectedDate, selectedTime, df, items):
    chosen_time = datetime.strptime(str(selectedDate), '%Y-%m-%d')
    chosen_time = chosen_time.replace(hour=selectedTime)

    nearest_date = str(choose_nearest_datetime(items, chosen_time))

    for element in df['list'][0]:
        if element['dt_txt'] == nearest_date:
            main_weather = element['weather'][0]['main']
            temp = round(element['main']['temp'] - 273.15, 2)

          #Error Handling for rainfall prediction due to varying key values from OpenWeatherAPI
            try:
                try:
                    if element['rain']['3h'] == {}:
                        rain = 0
                    else:
                        rain = element['rain']['3h']
                except:
                    try:
                        if element['rain'] == {}:
                            rain = 0
                        else:
                            rain = element['rain']
                    except:
                        try:
                            if element['snow']['3h'] == {}:
                                rain = 0
                            else:
                                rain = element['snow']['3h']
                        except:
                            try:
                                if element['snow'] == {}:
                                    rain = 0
                                else:
                                    rain = element['snow']
                            except:
                                rain = 0
            except:
                rain = 0



            df_db = pd.DataFrame(
                {'time': [chosen_time], 'main_weather': [main_weather], 'temp': [temp], 'rain_mm': [rain]})

    ## Creates an array with every unique station number
    sorted(df_db.main_weather.unique())

    main_weather_dummies = pd.get_dummies(df_db['main_weather'], prefix="main_weather")

    additional_main_weathers = ['main_weather_Thunderstorm', 'main_weather_Haze', 'main_weather_Squall',
                                'main_weather_Smoke', 'main_weather_Dust', 'main_weather_Tornado',
                                'main_weather_Ash', 'main_weather_Clouds', 'main_weather_Clear', 'main_weather_Rain',
                                'main_weather_Fog', 'main_weather_Drizzle', 'main_weather_Mist', 'main_weather_Snow']

    categ_features = main_weather_dummies.columns.values.tolist() + additional_main_weathers
    cont_features = ['hour', 'rainfall_mm', 'main_temp']

    features = cont_features + categ_features
    df_db = pd.concat([df_db, main_weather_dummies], axis=1)
    df_db = df_db.drop('main_weather', axis=1)

    for weather_descriptor in additional_main_weathers:
        if weather_descriptor not in df_db.columns:
            df_db[weather_descriptor] = 0

    df_db = pd.DataFrame({'time': df_db['time'], 'temp': df_db['temp'],
                          'rain_mm': df_db['rain_mm'], 'main_weather_Clouds': df_db['main_weather_Clouds'],
                          'main_weather_Clear': df_db['main_weather_Clear'],
                          'main_weather_Rain': df_db['main_weather_Rain'],
                          'main_weather_Fog': df_db['main_weather_Fog'],
                          'main_weather_Drizzle': df_db['main_weather_Drizzle'],
                          'main_weather_Mist': df_db['main_weather_Mist'],
                          'main_weather_Snow': df_db['main_weather_Snow'],
                          'main_weather_Thunderstorm': df_db['main_weather_Thunderstorm'],
                          'main_weather_Haze': df_db['main_weather_Haze'],
                          'main_weather_Squall': df_db['main_weather_Squall'],
                          'main_weather_Smoke': df_db['main_weather_Smoke'],
                          'main_weather_Dust': df_db['main_weather_Dust'],
                          'main_weather_Tornado': df_db['main_weather_Tornado'],
                          'main_weather_Ash': df_db['main_weather_Ash']})

    for index, row in df_db.iterrows():
        if df_db.loc[index, 'time'].hour == 0:
            df_db.loc[index, 'time'] = 24
        else:
            df_db.loc[index, 'time'] = df_db.loc[index, 'time'].hour

    return df_db
