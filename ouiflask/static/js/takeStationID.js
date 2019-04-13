function takeStationID() {
    // retrive the station that the user selected in the drop down menue
    // var x = document.getElementById("stationSelector").value
    var shownVal= document.getElementById("stationSelector").value;
    var x=document.querySelector("#stationsList option[value='"+shownVal+"']").dataset.value;

    // initialises a variable that references the marker object from dictionary with the key the station
    // name selected in the dropdown menu
    var selectedStation = dict[x];

    // Triggers the 'click' listener even of the marker object corresponding to the selectstation from
    // dropdown menu
    // the google map event will call the ajax function AjaxCommunicationForStationID
    google.maps.event.trigger(selectedStation, 'click');

    // call the function making the ajax call
    //  not needed since the google.maps.event.trigger call it
    // AjaxCommunicationForStationID(x);
}
// function that pass the stationID to the back end and do something with the response
function AjaxCommunicationForStationID(stationID){

    // AjAX call
    $.ajax({
        type: "POST",
        // put stationID in the post call so the back end can have access to the stationID
        data:{stationID: stationID},
        // will use the function stationDetail() in the routes.py file
        url: $SCRIPT_ROOT + '/stationDetail',
        dataType: "json",
        // when the python function return (Ajax have a response of 200 succcess) we can do something with the data returned
        success: function(station) {
            // TO DO: make something useful with the retrieved data
            // console.log(station);
            //
            // var infoStationHtml = "Station " + station.name + " have " + station.available_bikes+" available bikes and " +station.available_bike_stands+ " free bike stand" ;
            // document.getElementById("infoStation").innerHTML = infoStationHtml;

            var queryData = "queryData" + stationID;

            document.getElementById(queryData).innerHTML =`
                <td>`+station.available_bikes+`</td>
                <td>`+station.available_bike_stands+`</td>`;
        },
        // If there is a problem with the ajax request we retrieve the error
        error: function(jqXHR) {
            console.log(jqXHR);
        }
    })
}