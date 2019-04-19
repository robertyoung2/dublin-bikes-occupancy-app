function AjaxCommunicationForBikeGraph(stationID, maxBikes, name){
// function gathering data from the back end and distribute formated data to charts builder
    $.ajax({
        type: "POST",
        data:{stationID: stationID, maxBikes: maxBikes, station_name: name},
        // will use the function bikeGraph() in the routes.py file
        url: $SCRIPT_ROOT + '/bikeGraph',
        dataType: "json",
        success: function(station) {
             if($('#chartSection:visible').length == 0){
                document.getElementById("chartSection").style.display = "block";
                document.getElementById("arrowSection").style.display = "block";
            }
            // send the formated data to a function dra wing the charts
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
    // this function draw a chart with the weekly previsions 

    flashMessage('Select day to view daily predictions')
    resize()

    // Before a chart is drew the div container is removed and rebuilt to avoid interferences
    $('#chart_0').remove(); 
    $('#chartContainerInner').append('<canvas id="chart_0"><canvas>'); 

    // select the wanted data and labels
    var avgBikesData = station_data[0];
    var weekday = station_data[2];


    // get the canvas and make the chart
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
    options: { legend: {
        labels: { fontColor: "black",}},
        scales: {
            yAxes: [{ticks: {beginAtZero: true,fontColor:'black'}}],
            xAxes: [{ticks: {fontColor:'black'}}]
        }
    }
    });

    // allow the chart to be clicable
    canvas.onclick = function (evt){

        // select what bar is clicked
        var activePoints = myChart.getElementsAtEvent(evt);

        if (activePoints[0]) {
            // get the index 
            var idx = activePoints[0]['_index'];
            // call the function to draw the daily chart
            dayChart(station_data, idx)
        }
    }
}

// make the daily chart 
function dayChart(station_data, idx) {
    // please refer to drawChartJS for more comments
    $('#chart_0').remove(); 
    $('#chartContainerInner').append('<canvas id="chart_0"><canvas>'); 
    flashMessage('Click anywhere on chart to return to weekly data')

    // used later to select the title of the chart
    var weekday = station_data[2];

    // build the value of the x axis
    var timeHour = [];
    for (let index = 5; index < station_data[1][idx].length; index++) {
        timeHour.push(index+":00");
    }
    timeHour.push('Midnight');

    // select hourly data of day idx, and average it per hour.
    var avgBikesData = station_data[1][idx];
    var meanAvailableHourly = [];
    for (let i = 0; i < avgBikesData.length; i++) {
        meanAvailableHourly.push(avgBikesData[i][1]);
    }

    // get the canvas and draw the chart
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
            legend: {labels: {fontColor: "black",}},
            scales: {
                yAxes: [{ticks: {beginAtZero: true,fontColor:'black'}}],
                xAxes: [{ticks: {fontColor:'black'}}]
            }
        }
    });
    // when clicking anywhere on the chart we return to the weekly chart (we redraw it in fact)
    canvas.onclick = function (){
        drawChartJS(station_data)
    }

}

function resize (){
    // will resize the chart to its outer container every time a chart is built
    document.getElementById("chartContainerOuter").style.width = "50%";
}