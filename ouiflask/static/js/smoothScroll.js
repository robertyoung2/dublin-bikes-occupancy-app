//Adapted from Stack Overflow Answer: https://stackoverflow.com/a/52522150

var firstLoad = true;

function SmoothVerticalScrolling(element, time, where) {
    // Function which handles the autoscroll functionality of the site
    //  It checks to see what direction the arrow is pointing and scrolls in the appropriate direction
    //  the function uses a timeout to handle animation
    if(firstLoad){
        var e = document.getElementById("mapSection");
        e.classList.add("scroll_on");
        firstLoad = false;
    }
    var bodyElement = document.getElementById("body");
    if(element === "map"){
        var eTop = -1 * bodyElement.clientHeight;
    }
    else if(element === "chart"){
        var eTop = bodyElement.clientHeight;
    }
    var eAmt = eTop / 100;
    var curTime = 0;
    while (curTime <= time) {
        window.setTimeout(SVS_B, curTime, eAmt, where);
        curTime += time / 100;
    }
}

function SVS_B(eAmt, where) {
    // This isn't used but was left is as may be useful for future functionality
    // Determines whether to anchor the destination of the scroll at the top or bottom of the target element
    if(where == "center" || where == "")
        window.scrollBy(0, eAmt / 2);
    if (where == "top")
        window.scrollBy(0, eAmt);
}

