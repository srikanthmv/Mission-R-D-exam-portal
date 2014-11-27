function entry()
{
    json_data = {
    testname:$('#testname').val(),
    testdescription:$('#testdescription').val(),
    testduration:$('#testduration').val()
    }
    $.ajax({
        url: "http://localhost:8000/createtest/",
        type: "post",
        datatype: "application/json",
        data:
            json_data,
        success: function(response){
            location.href = '/testPages/'
            console.log("success");
        },
        error: function(response){
             console.log('error');
        }
    });
};
