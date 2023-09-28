           /* CHECK TIME SESSION USERS */
var TIMER_SESSION = 10 * 60000; // 60000 = 1 min
var lastActivityTime = Date.now();

setInterval(function() {
    var currentTime = Date.now();
    var timeDifference = currentTime - lastActivityTime;

    if (timeDifference > TIMER_SESSION) {
        window.location.href = '/logout';
    }
}, TIMER_SESSION);

$(document).on('click mousemove keydown', function() {
    lastActivityTime = Date.now();
});



