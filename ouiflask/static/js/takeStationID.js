function takeStationID() {
    // when the user select a station from the dropdown menu this function will select the station on google map.

    var shownVal= document.getElementById("stationSelector").value;
    // replace ' by \' for an easier interpretation
    shownVal = String(shownVal).replace(/&#39;/g,"\\'");
    var x=document.querySelector("#stationsList option[value=\""+shownVal+"\"]").dataset.value;
    var selectedStation = dict[x];

    // trigger a click event to select the wanted station
    google.maps.event.trigger(selectedStation, 'click');
}


function AjaxCommunicationForStationID(stationID){
    // function triggered when the user select a station. This will populate the infowindow with the number of bike available.
    $.ajax({
        type: "POST",
        data:{stationID: stationID},
        url: $SCRIPT_ROOT + '/stationDetail',
        dataType: "json",

        success: function(station) {
            var queryData = "queryData" + stationID;

            // populate the info window with data from back end.
            document.getElementById(queryData).innerHTML =`
                <td>`+station.available_bikes+`</td>
                <td>`+station.available_bike_stands+`</td>`;
        },

        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
}