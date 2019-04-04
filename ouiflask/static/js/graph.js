// function that pass the stationID to the back end and do something with the response
function AjaxCommunicationForBikeGraph(stationID){
    console.log("Querying: " + stationID);
    // AjAX call
    $.ajax({
        type: "POST",
        // put stationID in the post call so the back end can have access to the stationID
        data:{stationID: stationID},
        // will use the function bikeGraph() in the routes.py file
        url: $SCRIPT_ROOT + '/bikeGraph',
        dataType: "json",

        // when the python function return (Ajax have a response of 200 succcess) we can do something with the data returned
        success: function(station) {
            // TO DO: make something useful with the retrieved data
            // console.log(station);
            // drawChart(station);
            drawChartJS(station)

        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
}

function drawChartJS(station_data) {
    var avgBikesData = station_data[1];
    

    var weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

    var meanAvailableBikeWeakly = [];
    for (let i = 0; i < avgBikesData.length; i++) {
        meanAvailableBikeWeakly.push(avgBikesData[i][1]);
    }
    

    var ctx = document.getElementById('chart_3').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: weekday,
        datasets: [{
            label: 'Available bikes weekly',
            data: meanAvailableBikeWeakly,
            backgroundColor: [
                'rgba(255, 99, 132, 1)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
    });
}