function flashMessage (message){
  // This function will create a flash message using the flash function from a jquery library
    flash(message ,{
        // background color
        'bgColor' : '#508698',
        // text color
        'ftColor' : 'white',
        // or 'top'
        'vPosition' : 'bottom',
        // or 'left'
        'hPosition' : 'right',
        // duration of animation
        'fadeIn' : 400,
        'fadeOut' : 400,
        // click to close
        'clickable' : true,
        // auto hides after a duration time
        'autohide' : true,
        // timout
        'duration' : 4000
      });
}