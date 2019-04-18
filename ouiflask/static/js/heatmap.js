// setting parameters for icon we're going to use for markers
function generate_heatmap(available_bikes, available_stands){

    percentage_bikes_available = (available_bikes / (available_bikes + available_stands)) * 100;

    if(percentage_bikes_available > 40){
        var icon = 'icon_dublinbikes_sea_blue.png';
    }
    else if(percentage_bikes_available > 20){
        var icon = 'icon_dublinbikes_orange.png';
    }
    else{
        var icon = 'icon_dublinbikes_pastelle_red.png'
    }

    var image = {
        url: '/static/images/marker_icons/'+icon, //the image itself
        scaledSize: new google.maps.Size(50, 50) // resizing image to 50% smaller
    };
    return image
}