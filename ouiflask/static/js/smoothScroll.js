var firstLoad = true;

function SmoothVerticalScrolling(element, time, where) {
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
    console.log(eTop);
    var eAmt = eTop / 100;
    var curTime = 0;
    while (curTime <= time) {
        window.setTimeout(SVS_B, curTime, eAmt, where);
        curTime += time / 100;
    }
}

function SVS_B(eAmt, where) {
    if(where == "center" || where == "")
        window.scrollBy(0, eAmt / 2);
    if (where == "top")
        window.scrollBy(0, eAmt);
}

