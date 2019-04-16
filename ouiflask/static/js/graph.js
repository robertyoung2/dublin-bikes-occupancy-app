// function that pass the stationID to the back end and do something with the response
function AjaxCommunicationForBikeGraph(stationID, maxBikes, name){

    // AjAX call
    $.ajax({
        type: "POST",
        // put stationID in the post call so the back end can have access to the stationID
        data:{stationID: stationID, maxBikes: maxBikes, station_name: name},
        // will use the function bikeGraph() in the routes.py file
        url: $SCRIPT_ROOT + '/bikeGraph',
        dataType: "json",

        // when the python function return (Ajax have a response of 200 success) we can do something with the data returned
        success: function(station) {
            // console.log(station);

             if($('#chartSection:visible').length == 0){
                document.getElementById("chartSection").style.display = "block";
                document.getElementById("arrowSection").style.display = "block";
            }

            // draw the weekly graph
            drawChartJS(station);
            SmoothVerticalScrolling("chart", 1000, 'top');
        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
}

function drawChartJS(station_data) {
    flashMessage('Click on a day for more prediction')
    resize()

    // remove the canvas this way we can switch from the weekly to daily graph without artifact 
    $('#chart_0').remove(); 
    $('#chartContainerInner').append('<canvas id="chart_0"><canvas>'); // make a new canvas

    // select the wanted data
    var avgBikesData = station_data[0];

    // labels for the graph
    var weekday = station_data[2];


    // get the canvas and make the graph
    var canvas = document.getElementById('chart_0');
    var ctx = canvas.getContext('2d');
    ctx.canvas.width = $('#chartContainerOuter').width(); // resize to parent width
    ctx.canvas.height = $('#chartContainerOuter').height(); // resize to parent height
    Chart.defaults.global.defaultFontFamily = 'Roboto', "sans-serif";
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: weekday,
        datasets: [{
            label: station_data[3] + ' - Average Available Bikes - Weekly',
            data: avgBikesData,
            backgroundColor: '#3F898C',
            hoverBorderColor: "#AB6F69",
            borderColor: '#EEEEEE',
            borderWidth: 5
        }]
    },
    options: {
        legend: {
            labels: {
                fontColor: "black",
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    fontColor:'black'
                }
            }],
            xAxes: [{
                ticks: {
                    fontColor:'black'
                }
            }]
        }
    }
    });

    // when clicking on a bar make a new graph corresponding to the day
    canvas.onclick = function (evt){

        // select what bar is clicked
        var activePoints = myChart.getElementsAtEvent(evt);
        // console.log("Active Points");
        // console.log(activePoints);

        if (activePoints[0]) {
            // get the index 
            var idx = activePoints[0]['_index'];

            // call the function to draw the daily graph
            dayChart(station_data, idx)
        }
    }
}

// make the daily graph 
function dayChart(station_data, idx) {
    // remove the canvas this way we can switch from the weekly to daily graph without artifact 
    $('#chart_0').remove(); 
    $('#chartContainerInner').append('<canvas id="chart_0"><canvas>'); // make a new canvas
    flashMessage('Click on the chart to go back on the weekly graph')
    // used later to select the title of the graph
    var weekday = station_data[2];

    // label of the graph
    var timeHour = [];

    // console.log(station_data[1]);
    for (let index = 5; index < station_data[1][idx].length; index++) {
        timeHour.push(index+":00");
    }
    timeHour.push('Midnight');
    // console.log(timeHour);
    // station_data[2] contain all the hourly data for each day [idx] select the wanted day 0 monday 1 tuesday...
    var avgBikesData = station_data[1][idx];
    //
    // console.log("day index: ",idx);
    // console.log("Station Data: " + station_data[1]);


    // make a simple array with all the data needed to make the graph
    var meanAvailableHourly = [];

    for (let i = 0; i < avgBikesData.length; i++) {
        meanAvailableHourly.push(avgBikesData[i][1]);
    }

    // get the canvas and draw the graph
    var canvas = document.getElementById('chart_0');
    var ctx = canvas.getContext('2d');
    ctx.canvas.width = $('#chartContainerOuter').width(); // resize to parent width
    ctx.canvas.height = $('#chartContainerOuter').height();
    new Chart(ctx, {
        type: 'bar',
        data: {

            labels: timeHour,
            datasets: [{
                label: station_data[3] + ' - Predicted Available Bikes - ' + weekday[idx],
                data: meanAvailableHourly,
                backgroundColor: '#3F898C',
                hoverBorderColor: "#AB6F69",
            borderColor: '#EEEEEE',
                borderWidth: 5
            }]
        },
        options: {
            legend: {
                labels: {
                    fontColor: "black",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontColor:'black'
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor:'black'
                    }
                }]
            }
        }
    });
    // when clicking anywhere on the graph we return to the weekly graph (we redraw it in fact)
    canvas.onclick = function (){
        drawChartJS(station_data)
    }

}

function resize (){
    // document.getElementById('mapContainer').style.minHeight = "";
    // document.getElementById("chartContainerOuter").style.height = "70%";
    document.getElementById("chartContainerOuter").style.width = "50%";
}