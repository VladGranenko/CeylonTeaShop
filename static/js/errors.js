document.addEventListener("DOMContentLoaded", function() {
    var messages = document.getElementsByClassName('message');

    for (var i = 0; i < messages.length; i++) {
        var message = messages[i];
        setTimeout(function(element) {
            element.style.display = "none";
        }, 4000, message);
    }
});


