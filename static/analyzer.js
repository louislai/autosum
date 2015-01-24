$(document).ready( function() {

    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
        var input = $('#article_summarize_input').html();
        $.get('/index', 
    });
});