function getWeather (){

    // AjAX call
    $.ajax({
        type: "POST",
        // will use the function stationDetail() in the routes.py file
        url: $SCRIPT_ROOT + '/getWeather',
        // when the python function return (Ajax have a response of 200 success) we can do something with the data     returned
        success: function(weather) {
            // TO DO: make something useful with the retrieved data
            // console.log(weather);
            // var weatherHtml = "we are the "+ weather.last_update +" and today the weather is "+ weather.description ;
            // document.getElementById("weather").innerHTML = weatherHtml;

            var current_temp_celcius = Math.round(weather.temp - 273.15);
            document.getElementById("weatherTemp").innerHTML = current_temp_celcius + " &#8451" ;

            if(current_temp_celcius < 4){
                var thermo_icon = "temp0.svg";
            }
            else if(current_temp_celcius < 12){
                var thermo_icon = "temp25.svg";
            }
            else if(current_temp_celcius < 19){
                var thermo_icon = "temp50.svg";
            }
            else if(current_temp_celcius < 23){
                var thermo_icon = "temp75.svg";
            }
            else{
                var thermo_icon = "temp100.svg";
            }

            document.getElementById("weatherThermometer").src = "/static/images/weather_icons/"+thermo_icon;
            document.getElementById("weatherDescription").innerHTML = weather.description;
            document.getElementById("weatherIcon").src = "/static/images/weather_icons/"+weather.icon+".svg";
        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
    }