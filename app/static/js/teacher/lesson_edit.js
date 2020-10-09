var id_taskDescription = 'taskDescription';
var id_card = 'card';
var id_now = 0;

var api_url = document.location.origin + '/teacher/api_lesson/' + topic_id;
var url_success_ajax = document.location.origin + '/teacher/' + 'topics/' + topic_id;

if (http_request_type == 'POST'){
    api_url += '/lesson/' + lesson.id;
}

function get_new_task_div(id){
    var new_task_div = `
        <div class="card shadow mb-4" id="${id_card + id_now}">
            <div class="card-header py-3 d-flex justify-content-between">
                <h4 class="m-0 font-weight-bold text-primary">Задача</h4>
                <span style="cursor: pointer;" class="far fa-trash-alt my-auto fa-lg" onclick="delete_task(${id})"></span>
            </div>
            <div class="card-body">
                <div id='task${id}'>
                    <div class="form-group">
                        <label for="taskName">Название задачи</label>
                        <input name="taskName" type="text" class="form-control" id="taskName" required>
                    </div>

                    <div class="form-group">
                        <label for="taskDescription">Описание задачи</label>
                        <textarea name="description" type="text" class="form-control" id="${id_taskDescription + id}"></textarea>
                    </div>

                    <div class="form-group">
                        <h4 for="taskExamples">Примеры:</h4>
                        <div id="taskExamples">
                            <div>
                                <div>Входные данные</div>
                                <textarea name="in_data" type="text" class="form-control data" id="in_data" required></textarea>
                            </div>
                            <div class="mt-3">
                                <div>Выходные данные</div>
                                <textarea name="out_data" type="text" class="form-control data" id="out_data" required></textarea>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    `;
    return new_task_div;
}

function success_ajax(data, textStatus, jqXHR){
    window.location.replace(url_success_ajax);
}

function error_ajax(jqXHR, textStatus, errorThrown){

}

function add_new_task(){
    var task_id = id_now;

    $('#tasks').append(get_new_task_div(id_now));
    CKEDITOR.replace( id_taskDescription + id_now );
    id_now++;

    return task_id;
}

function delete_task(task_id){
    $('#' + id_card + task_id).remove();
}

function send_data(){
    var name = $("#lessonName").val();
    var tasks = new Array();

    var tasks_cards = $('#tasks').children();

    for(var i = 0; i < tasks_cards.length; i++){
        var task_card = $(tasks_cards[i]);
        var task_description_id = task_card.find('textarea[name="description"]').attr('id');
        var task = new Object();

        task.name = task_card.find('#taskName').val();
        task.description = CKEDITOR.instances   [task_description_id].getData();
        task.in_data = task_card.find('#in_data').val();
        task.out_data = task_card.find('#out_data').val();

        tasks.push(task);
    }

    var data = JSON.stringify({'name': name,
                'tasks': tasks});

    console.log(data);


    $.ajax({
        url: api_url,
        type: http_request_type,
        data: data,
        success: success_ajax,
        error: error_ajax,
        contentType: "application/json; charset=utf-8",
    });

    return false;
}

$(document).ready(function(){
    if(!lesson){
        return;
    }

    $('#lessonName').val(lesson.name);

    for(var i = 0; i < lesson.tasks.length; i++){
        var task = lesson.tasks[i];

        var task_id = add_new_task();
        var task_card = $('#' + "task" + task_id);

        task_card.find('#taskName').val(task.name);
        CKEDITOR.instances[id_taskDescription + task_id].setData(task.description, {callback: function() {
                                                                                                this.checkDirty(); // true
                                                                                            }
                                                                                    }
                                                               );
        task_card.find('#in_data').val(task.in_data);
        task_card.find('#out_data').val(task.out_data);
    }
})