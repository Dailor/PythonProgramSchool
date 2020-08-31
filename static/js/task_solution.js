url = '/pupil/api_solution'

var editor = CodeMirror(document.getElementById("codeMirror"),
                       {lineNumbers: true,
                        theme: "neat",
                        });


function send_solution(){
    data = {'result': editor.getValue(),
            'group_id': group_id,
            'task_id': task_id}
    $.ajax({
        url: url,
        type: "PUT",
        data: data,
    })

    $('#sendSolution').attr('disabled', true)
    window.setTimeout(function () {
                        document.getElementById('sendSolution').disabled = false;
                    }, 5000);
}


$(document).ready(function(){
    if (task_solution){
        editor.setValue(task_solution.result);
        editor.doc.cantEdit = true;
    }
})