# READ ME

## Package Information

Below is a list of the required packages to run in the virtual environment. 
This is a working list, as each team member finds a new package required, add to the list
and notify the team via the dublin-bikes Slack channel.

Required packages. Use _"conda install PACKAGE\_NAME"_:


### sql
* scikit-learn
* pandas
* numpy (installed as part of scikit-learn)
* requests
* jsonschema
* sqlalchemy 
* jupyter
* PyMySQL

### flask
* flask
* conda install beautifulsoup4 

Optional:

* matplotlib (for data analytics/plotting)

Current venv: ouiteam_v2.

## Starting and Stopping Flask App on EC2

Flask app is run using a combination of Nginx and Gunicorn. The IP for our web app is [18.220.169.53](http://18.220.169.53).

Gunicorn is the server the runs the application. Nginx is used as the reverse-proxy server.

To start the flask app running, and to keep it running on our IP address, the process call on the EC2 instance is:
* nohup gunicorn run:app &

To stop gunicorn running, the command is:
* pkill gunicorn

See a quick overview of the implementation [here](https://chrisdtran.com/2017/deploy-flask-on-ec2/).

## Predictor Model Inputs

The predictor model, loaded as a pickle file requires a total of 16 inputs.

Each input must be given in the exact order and form as follows:

[[hour, rainfall_mm, main_temp, main_weather_Clouds, main_weather_Drizzle, main_weather_Fog,	
  main_weather_Mist, main_weather_Rain,	main_weather_Snow, main_weather_Thunderstorm, main_weather_Haze,	
  main_weather_Squall, main_weather_Smoke, main_weather_Dust, main_weather_Tornado, main_weather_Ash]]
  
The type for each of the previous variables is as follows:

* hour - integer value for the hour, such as '23' for 11pm.
* rainfall_mm - float value for rainfall, such as '0.5' for 0.5mm of rainfall in the last hour.	
* main_temp	- float value for current temperature in degrees celsius, such as '14.5' for 14.5C.
* main_weather_Clouds - binary value for descriptor, '1' for true, '0' for false
* main_weather_Drizzle - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Fog - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Mist - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Rain - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Snow - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Thunderstorm - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Haze - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Squall - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Smoke - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Dust - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Tornado - binary value for descriptor, '1' for true, '0' for false	
* main_weather_Ash - binary value for descriptor, '1' for true, '0' for false

The resulting output will be a float value estimating the number of bikes available for the given inputs.
This should be rounded to an integer to allow for a sensible result. Eg "5 bikes" as oppose to "4.7 bikes".

The path for the pickle files on EC2 is: /home/ubuntu/oui-team/pickle_files/
