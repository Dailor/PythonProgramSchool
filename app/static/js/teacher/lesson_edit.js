var id_taskDescription = 'taskDescription';
var id_taskSolution = 'taskSolution';
var id_card = 'card';
var id_now = 0;

var api_url = document.location.origin + '/teacher/api_lesson/' + topic_id;
var url_success_ajax = document.location.origin + '/teacher/' + 'topics/' + topic_id;

if (http_request_type == 'POST'){
    api_url += '/lesson/' + lesson.id;
}

function addTaskExample(task_id){
    var examplesBlock = $('#' + task_id).find('#taskExamples');
    var exampleBlockHtml = `<div id='taskExample' class='mb-3'>
                                                    <div class='d-flex justify-content-between'>
                                                        <h3>Пример</h3>
                                                        <span style="cursor: pointer;" class="fas fa-times my-auto fa-lg" onclick="delete_example(this)"></span>
                                                    </div>
                                                    <div>
                                                        <div>Входные данные</div>
                                                        <textarea name="in_data" type="text" class="form-control data" id="in_data" required></textarea>
                                                    </div>
                                                    <div class="mt-3">
                                                        <div>Выходные данные</div>
                                                        <textarea name="out_data" type="text" class="form-control data" id="out_data" required></textarea>
                                                    </div>

                                                    <div class="form-group row mt-2">
                                                        <div class="col-sm-2">Скрытый тест</div>
                                                        <div class="col-sm-10">
                                                          <div class="form-check">
                                                            <input class="form-check-input" type="checkbox" id="hide-example">
                                                            <label class="form-check-label" for="hide-example">
                                                              Да
                                                            </label>
                                                          </div>
                                                        </div>
                                                    </div>
                                                </div>`;
    var jQueryExampleBlock = $(exampleBlockHtml);
    examplesBlock.append(jQueryExampleBlock);
    return jQueryExampleBlock;
}

function delete_example(span){
    $(span.parentNode.parentNode).remove();
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
                        <label for="taskSolution">Решение задачи</label>
                        <textarea name="solution" type="text" class="form-control" id="${id_taskSolution + id}"></textarea>
                    </div>

                    <div class="form-group">
                        <label for="taskTimeLimit">Ограничение по времени (в секундах)</label>
                        <input name="taskTimeLimit" type="number" class="form-control" id="taskTimeLimit" min=0 step="any" max=${time_limit_max} required>
                    </div>

                    <div class="form-group">
                        <label for="taskMemoryLimit">Ограничение по памяти (в мегабайтах)</label>
                        <input name="taskMemoryLimit" type="number" class="form-control" id="taskMemoryLimit" min=0 max=${memory_limit_max} required>
                    </div>

                    <div class="form-group">
                        <label for="maxCountTries">Число попыток</label>
                        <input name="maxCountTries" type="number" class="form-control" id="maxCountTries" min=1 required>
                    </div>

                    <div class="form-group">
                        <div id="taskExamples" class="taskExamples">
                        </div>
                        <button type='button' class='btn btn-secondary mt-3' id='add-example-btn' onclick='addTaskExample("task${id}")'>Добавить пример</button>
                    </div>

                    <div class="form-group row">
                        <div class="col-sm-2">Авто проверка</div>
                        <div class="col-sm-10">
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="autotest-example">
                            <label class="form-check-label" for="autotest-example">
                              Да
                            </label>
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
    alert(textStatus);
}

function add_new_task(){
    var task_id = id_now;

    $('#tasks').append(get_new_task_div(id_now));
    CKEDITOR.replace( id_taskDescription + id_now );
    CKEDITOR.replace( id_taskSolution + id_now );
    id_now++;

    return task_id;
}

function delete_task(task_id){
    $('#' + id_card + task_id).remove();
}

function task_collection(){
    var tasks = new Array();
    var tasks_cards = $('#tasks').children();

    for(var i = 0; i < tasks_cards.length; i++){
        var task_card = $(tasks_cards[i]);
        var examples_block = task_card.find('#taskExamples').children();

        var task_description_id = task_card.find('textarea[name="description"]').attr('id');
        var task_solution_id = task_card.find('textarea[name="solution"]').attr('id');

        var task = new Object();
        var examples = new Array();
        var examples_hidden = new Array();

        task.name = task_card.find('#taskName').val();

        task.time_limit = parseFloat(task_card.find('#taskTimeLimit').val());
        task.memory_limit = parseInt(task_card.find('#taskMemoryLimit').val());
        task.tries_limit = parseInt(task_card.find('#maxCountTries').val());

        task.description = CKEDITOR.instances[task_description_id].getData();
        task.solutions = CKEDITOR.instances[task_solution_id].getData();

        for(var j=0; j < examples_block.length; j++){
            var example_data = new Object();
            var example_block = $(examples_block[j]);
            var hide_example_checkbox = example_block.find('#hide-example')

            example_data.in_data = example_block.find('#in_data').val();
            example_data.out_data = example_block.find('#out_data').val();

            if(hide_example_checkbox.is(':checked')){
                examples_hidden.push(example_data);
            }else{
                examples.push(example_data);
            }
        }
        task.examples_hidden = examples_hidden;
        task.examples = examples;
        task.api_check = task_card.find('#autotest-example').is(':checked');
        tasks.push(task);
    }

    return tasks;
}

function send_data(){
    var name = $("#lessonName").val();
    var language_id = parseInt($("#programming-language").val());
    var lessonMaterial = CKEDITOR.instances['lessonMaterial'].getData();
    var tasks = task_collection();


    var data = JSON.stringify({'name': name,
                'tasks': tasks,
                'language_id': language_id,
                'html_page': lessonMaterial});

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

    CKEDITOR.replace('lessonMaterial');
    CKEDITOR.instances['lessonMaterial'].setData(lesson.html, {callback: function() {
                                                                                                this.checkDirty(); // true
                                                                                            }
                                                                                    });

    $('#lessonName').val(lesson.name);

    for(var i = 0; i < lesson.tasks.length; i++){
        var task = lesson.tasks[i];

        var task_id = add_new_task();
        var task_card = $('#' + "task" + task_id);
        var btn_add_example = task_card.find('add-example-btn');
        var examples_block = task_card.find('#taskExamples');

        task_card.find('#taskName').val(task.name);
        CKEDITOR.instances[id_taskDescription + task_id].setData(task.description, {callback: function() {
                                                                                                this.checkDirty(); // true
                                                                                            }
                                                                                    }
                                                               );

        CKEDITOR.instances[id_taskSolution + task_id].setData(task.solutions, {callback: function() {
                                                                                                this.checkDirty(); // true
                                                                                            }
                                                                                    }
                                                               );

        task_card.find('#taskTimeLimit').val(task.time_sec);
        task_card.find('#taskMemoryLimit').val(task.memory_mb);
        task_card.find('#maxCountTries').val(task.tries_count);

        for(var j = 0; j < task.examples.length; j++){
            var example_block = addTaskExample(`task${task_id}`);

            example_block.find('#in_data').val(task.examples[j].in_data);
            example_block.find('#out_data').val(task.examples[j].out_data);
        }

        for(var j = 0; j < task.examples_hidden.length; j++){
            var example_block = addTaskExample(`task${task_id}`);

            example_block.find('#in_data').val(task.examples_hidden[j].in_data);
            example_block.find('#out_data').val(task.examples_hidden[j].out_data);
            example_block.find('#hide-example').prop('checked', true);
        }
    }
})

