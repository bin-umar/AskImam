var hijri = document.getElementById("hijri");
var grigorian = document.getElementById("grigorian");

hijri.innerHTML = HijriJS.todayHijri();
grigorian.innerHTML = HijriJS.todayGregorian();

tinymce.init({
  selector: 'textarea#tinymce',
  height: 120,
  menubar: false,
  plugins: [
    'advlist autolink lists link image charmap print preview anchor textcolor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime media table contextmenu paste code help wordcount'
  ],
  toolbar: 'insert | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
  content_css: [
    '/static/js/tinymce/skins/lightgray/codepen.min.css']
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

jQuery(document).ready(function() {

  $("#logIn").on("submit", function (event) {

      event.preventDefault();
      var email = $("#email").val(),
          password = $("#password").val(),
          next = $(this).find("input[name='next']").eq(0).val(),
          error = $('.errorLogin').eq(0);

      if (next === '') next = '/';

      $.post(
          "/login/",
          { "email": email, "password": password, "next": next },
          function(response) {
              if (!response.status) {
                  var data = response.message;
                  Object.keys(data).forEach(function (key) {
                      error.html(key + ": " + data[key].toString());
                  });
              }
              else
                  $(location).attr('href', response.message);
          }
      ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
      });
  });

  $("#signUp").on("submit", function (event) {

      event.preventDefault();
      var username = $("#login").val(),
          email = $("#email2").val(),
          password1 = $("#password1").val(),
          password2 = $("#password2").val(),
          error = $('.errorSignup').eq(0);

      if (password1 !== password2) {
          error.html("Passwords doesn't match");
      } else {
          $.post(
              "/signup/",
              { "username": username, "email": email, "password1": password1, "password2": password2 },
              function(response) {
                  if (!response.status) {
                      var data = response.message;
                      Object.keys(data).forEach(function (key) {
                          error.html(key + ": " + data[key].toString());
                      });
                  } else
                      $(location).attr('href', response.message);
              }
          ).fail(function(jqXHR, textStatus, err) {
              alert('text status ' + textStatus + ', err ' + err)
          });
      }
  });

});