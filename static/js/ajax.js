
$(document).ready(function() {

  $('#article_summarize_url').keydown(function (e){
    if(e.keyCode == 13){
      e.preventDefault();
      $('#article_summarize_submit').click();
    }
  })

  $('#article_url_2').keydown(function (e){
    if(e.keyCode == 13){
      e.preventDefault();
      $('#article_compare_submit').click();
    }
  })

  $('#article_cluster_urls').keydown(function (e){
    if(e.keyCode == 13){
      e.preventDefault();
      $('#article_cluster_submit').click();
    }
  })

  $('#article_summarize_submit').click(function() {
    var input = $('#article_summarize_url').val();
    if (!test_url.test(input)) {
      $('#summary_error').fadeIn();
    } else {
      $("#spinner").fadeIn();
      $('#article_summarize_result p').html('');
      $('#summary_error').fadeOut();
      $.post('/summarize', {article_url: input}, function(data) {
        $("#spinner").fadeOut();
        var result = "<p><h2>Summary</h2></p><ul>" + data + "</ul>";
        $('#article_summarize_result p').html(result);
      });
    }
  });

  $('#article_compare_submit').click(function() {
    var article_url_1 = $('#article_url_1').val();
    var article_url_2 = $('#article_url_2').val();
    if (!test_url.test(article_url_1)) {
      $('#compare_error_1').fadeIn();
    } else {
      $('#compare_error_1').fadeOut();
    }
    if (!test_url.test(article_url_2)) {
      $('#compare_error_2').fadeIn();
    } else {
      $('#compare_error_2').fadeOut();
    }
    if (test_url.test(article_url_1) && test_url.test(article_url_2)) {
      $("#spinner").fadeIn();
      $.post('/compare', {article_url_1: article_url_1, article_url_2: article_url_2}, function(data) {
        $("#spinner").fadeOut();
        var result = data;
        $('#article_compare_result p').html(result);
      })
    }
  })

  $('#article_cluster_submit').click(function() {
    var urls = $('#article_cluster_urls').val();
    var array = urls.split(';');
    var valid = true;
    for(var i = 0; i < array.length; i++) {
      valid = test_url.test(array[i].trim());
    }
    if (valid) {
      $("#spinner").fadeIn();
      $('#cluster_error').fadeOut();
      $('#article_cluster_result p').html('');
      $.post('/cluster', {article_urls: urls}, function(data) {
        $("#spinner").fadeOut();
        var result = data;
        $('#article_cluster_result p').html(result);
      })
    } else {
      $('#cluster_error').fadeIn();
    }
  })

});

var test_url = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});