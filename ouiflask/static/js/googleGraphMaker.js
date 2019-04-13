  function drawChart(station_data) {
      console.log("Drawing Graph!");
      // console.log("Drawing Graph!");


      var avgStandsData = station_data[0];
      console.log("Avg Stands Data:")
      console.log(avgStandsData[0]);
      var avgBikesData = station_data[1];


    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'weekday');
    data.addColumn('number', 'stands');

    console.log("About to add rows")
    data.addRows(avgStandsData)
      console.log("rows added");

    // Set chart options
    var options = {
      'title': 'Avg. Available Bike Stands - ' + name,
      'width': 600,
      'height': 400,
        // 'backgroundColor': 'rgb(53, 112, 158)',
        backgroundColor: { fill:'transparent' },
        series: {
          0 : {color: 'rgb(71, 146, 209)'}
        }
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('chart_1'));
    chart.draw(data, options);
    //
    // var chart2 = new google.visualization.BarChart(document.getElementById('chart_2'));
    // chart2.draw(data, options);

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'weekday');
    data.addColumn('number', 'bikes');

    data.addRows(avgBikesData)

    // Set chart options
    var options = {
      'title': 'Avg. Available Bikes - ' + name,
      'width': 600,
      'height': 400,
        // 'backgroundColor': 'rgb(53, 112, 158)',
        backgroundColor: { fill:'transparent' },
        series: {
          0 : {color: 'rgb(71, 146, 209)'}
        }
    };

    var chart2 = new google.visualization.LineChart(document.getElementById('chart_2'));
    chart2.draw(data, options);
    
  }

  