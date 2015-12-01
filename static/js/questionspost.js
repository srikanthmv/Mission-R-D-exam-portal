/**
 * Created with PyCharm.
 * User: tony
 * Date: 10/24/14
 * Time: 9:04 PM
 * To change this template use File | Settings | File Templates.
 */
function post_questions() {
    $('input[type="text"]').each(function () {
            if ($.trim($(this).val()) == '') {
                $(this).css({
                    "border": "1px solid red"

                });
            }
    });
    json_data =
    {
        testid: $('#testid').val(),
        question: $('#question').val(),
        option1: $('#option1').val(),
        option2: $('#option2').val(),
        option3: $('#option3').val(),
        option4: $('#option4').val(),
        answerindex: $('#answerindex').val()
    }
    $.ajax({
        url: "http://localhost:8000/create/",
        type: "post",
        headers: {
            "X-CSRFToken": cookie('csrftoken')
        },
        datatype: "application/json",
        data: json_data,
        success: function (response) {
            location.href = '/testPages/'
            console.log("success");
        },
        error: function (response) {
            console.log('error');
//            console.log("fail");
        }
    });
}
function cookie(name) {
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