url = '/pupil/api/solution'



function success_ajax_send_solution(data, textStatus, jqXHR){
    add_solution(data);
    scrollToBottomSolutionsHistory();

    tries_left = data.tries_left;
    $('#tries-left').html(tries_left);
    getSolutionOnText();
}

function send_solution(){
    if(tries_left <= 0){
        alert('Не надо пытаться взломать :)');
        return;
    }

    data = {'result': editor.getValue(),
            'group_id': group_id,
            'task_id': task_id};
    $.ajax({
        url: url,
        type: "PUT",
        data: data,
        success: success_ajax_send_solution,
        error: function(jqXHR, textStatus, errorThrown){
           alert(jqXHR.responseJSON.error);
        }
    });

    $('#sendSolution').attr('disabled', true)
    window.setTimeout(function(){
                                document.getElementById('sendSolution').disabled = false;
                                }, 5000);
}
