var hijri = document.getElementById('hijri');
var grigorian = document.getElementById('grigorian');

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

function senPost(url, data, error) {
    $.post(
        url,
        data,
        function(response) {
            if (!response.status) {
                var data = response.message;
                Object.keys(data).forEach(function (key) {
                    error.html(key + ': ' + data[key].toString());
                });
            } else {
                $(location).attr('href', response.message);
            }
      }
    ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
    });
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    }
});

function vote(elem, value) {

    var obj = elem.id.split('_'),
        obj_name = obj[0],
        obj_id = obj[1];

    var obj_rate = $('#' + elem.id + '_rate');

    $.post(
        '/vote/',
        { 'obj_name': obj_name, 'obj_id': obj_id, 'value': value },
        function(response) {
            if (!response.status) {
                alert(response.message.value);
            } else {
                var rate = +obj_rate.text();
                obj_rate.text(rate+value);
            }
      }
    ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
    });
}

function setTrue(elem) {
    var state = $(elem).is(':checked'),
          id_answer = elem.id.split('_')[1],
          href = window.location.href.split('/'),
          checked = elem;

      var currentQuestion = href[3] + '/' + href[4];
      var checkboxes = $('.custom-checkbox');

      $.post(
          '/' + currentQuestion + '/answer/' + id_answer,
          { 'is_true': state },
          function(response) {
              if (!response.status) {
                  alert(response.message.value);
              } else {
                  if (state) {
                        for (var i=0; i < checkboxes.length; i++) {
                            if (checkboxes[i].id !== checked.id + '_') {
                                checkboxes[i].innerHTML = "";
                            }
                        }
                  } else {
                      for (var i=0; i < checkboxes.length; i++) {
                          if (checkboxes[i].id !== checked.id + '_') {
                              var id = checkboxes[i].id.slice(0, checkboxes[i].id.length - 1);

                              var checkbox = document.createElement("input");
                              checkbox.type = "checkbox";
                              checkbox.setAttribute('onclick', 'setTrue(this);');
                              checkbox.className = "custom-control-input";
                              checkbox.id = id;

                              var label = document.createElement("label");
                              label.htmlFor = id;
                              label.innerText = "Is true";
                              label.className = "custom-control-label";

                              checkboxes[i].append(checkbox);
                              checkboxes[i].append(label);
                          }
                      }
                  }
              }
          }
      ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
      });
}

function addAnswer(answer) {
    var answers = $('#answers'),
        answer_count = $('#answer_count');

    var a_count = +answer_count.text();
    answer_count.text(++a_count);

    answers.append(answer);
    tinymce.activeEditor.setContent('');
}

jQuery(document).ready(function() {

  $('#logIn').on('submit', function (event) {

      event.preventDefault();
      var email = $('#email').val(),
          password = $('#password').val(),
          next = $(this).find('input[name=\'next\']').eq(0).val(),
          error = $('.errorLogin').eq(0);

      if (next === '') next = '/';

      senPost('/login/' ,
             { 'email': email, 'password': password, 'next': next },
                  error);
  });

  $('#signUp').on('submit', function (event) {

      event.preventDefault();
      var username = $('#login').val(),
          email = $('#email2').val(),
          password1 = $('#password1').val(),
          password2 = $('#password2').val(),
          error = $('.errorSignup').eq(0);

      if (password1 !== password2) {
          error.html('Passwords doesn\'t match');
      } else {
          senPost('/signup/' ,
                 { 'username': username, 'email': email, 'password1': password1, 'password2': password2 },
                      error);
      }
  });

  $('#askForm').on('submit', function (event) {

      event.preventDefault();
      var title = $('#title').val(),
          text = $('#tinymce').val(),
          tags = $('#tags').val(),
          error = $('.errorSignup').eq(0);

      senPost('/ask/' ,
             { 'title': title, 'text': text, 'tags': tags },
                  error);
  });

  $('#addAnswer').on('submit', function (event) {

      event.preventDefault();
      var text = $('#tinymce'),
          action = $(this).attr("action"),
          error = $('.errorSignup').eq(0);

      $.post(
          action,
          {'text': text.val()},
          function(response) {
              if (!response.status) {
                  var data = response.message;
                  Object.keys(data).forEach(function (key) {
                        error.html(key + ': ' + data[key].toString());
                  });
              }
          }
      ).fail(function(jqXHR, textStatus, err) {
          alert('text status ' + textStatus + ', err ' + err)
      });
  });


  // $.post(
  //     '/publish/',
  //     function(response) {
  //         if (response.status) {
  //             console.log(response.message);
  //             var cent = new Centrifuge('ws://askimam.tj:8001/connection/websocket');
  //                 cent.setToken(response.message);
  //                 cent.subscribe('news', function(msg) { console.log(msg) });
  //                 cent.connect();
  //         } else {
  //             console.log(response.message);
  //         }
  //     }
  // ).fail(function(jqXHR, textStatus, err) {
  //     console.log('text status ' + textStatus + ', err ' + err)
  // });
});