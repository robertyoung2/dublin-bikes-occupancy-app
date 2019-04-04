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

            document.getElementById("weatherTemp").innerHTML = Math.round(weather.temp - 273.15) + " &#8451" ;
            document.getElementById("weatherDescription").innerHTML = weather.description;
            document.getElementById("weatherIcon").src = "http://openweathermap.org/img/w/"+weather.icon+".png";
        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
    }