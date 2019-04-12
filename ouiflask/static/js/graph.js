// function that pass the stationID to the back end and do something with the response
function AjaxCommunicationForBikeGraph(stationID){
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
            // draw the weekly graph
            drawChartJS(station)

        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
}

function drawChartJS(station_data) {
    resize()
    // remove the canvas this way we can switch from the weekly to daily graph without artifact 
    $('#chart_0').remove(); 
    $('#chartContainerInner').append('<canvas id="chart_0"><canvas>'); // make a new canvas
    // select the wanted data
    var avgBikesData = station_data[1];
    // labels for the graph
    var weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    // data for the graph
    var meanAvailableBikeWeakly = [];
    for (let i = 0; i < avgBikesData.length; i++) {
        meanAvailableBikeWeakly.push(avgBikesData[i][1]);
    }
    // get the canvas and make the graph
    var canvas = document.getElementById('chart_0');
    var ctx = canvas.getContext('2d');
    ctx.canvas.width = $('#chartContainerOuter').width(); // resize to parent width
    ctx.canvas.height = $('#chartContainerOuter').height(); // resize to parent height
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: weekday,
        datasets: [{
            label: 'Available bikes weekly',
            data: meanAvailableBikeWeakly,
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
    // when clicking on a bar make a new graph corresponding to the day
    canvas.onclick = function (evt){
        // select what bar is clicked
        var activePoints = myChart.getElementsAtEvent(evt);
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
    // used later to select the title of the graph
    var weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    // label of the graph
    var timeHour = ['Midnight'];
    for (let index = 5; index < station_data[2][idx].length; index++) {
        timeHour.push(index+":00");
    }
    // station_data[2] contain all the hourly data for each day [idx] select the wanted day 0 monday 1 tuesday...
    var avgBikesData = station_data[2][idx];
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
            label: weekday[idx],
            data: meanAvailableHourly,
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