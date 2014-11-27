/**
 * Created with PyCharm.
 * User: tony
 * Date: 10/9/14
 * Time: 11:37 AM
 * To change this template use File | Settings | File Templates.
 */
function saveanswers()
{
    if (!$('input[name=radio]:checked').val())
    {
        alert('please select one option')
    }
    else {
        json_data =
        {
            questionid: $('#questionid').val(),
            radio: $('input[name=radio]:radio:checked').val(),
            questionno: $('#questionno').val(),
            testid: $('#testid').val()
        }
        $.ajax({
            url: "http://localhost:8000/save/",
            type: "post",
            datatype: "application/json",
            headers: {
                "X-CSRFToken": cookie('csrftoken')
            },
            data: json_data,

            success: function (response) {
//             location.href ='/result/'
                console.log(response)
                $('input[name=radio]').attr('checked', false);
                $('#questionid').val(response.questions);
                $('#questionno').val(response.quesno);
                $('#question').text(response.questionvalue);
                $('#val1').val(response.option1);
                $('#val2').val(response.option2);
                $('#val3').val(response.option3);
                $('#val4').val(response.option4);
                $('#label1').text(response.option1);
                $('#label2').text(response.option2);
                $('#label3').text(response.option3);
                $('#label4').text(response.option4);
                $('#username').val(response.username);
                $('#testid').val(response.test);
            },
            error: function (response) {

                location.href = '/result/'
//            console.log("fail");
            }
        });
    }
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