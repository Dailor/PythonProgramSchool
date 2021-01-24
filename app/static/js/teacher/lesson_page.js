var url_api_lesson_available = '/teacher/api/lesson_available';
var url_api_solutions = '/teacher/api/solutions/';
var selected_task = null;
var already_changing_lesson_status = false;

var selector_pupils_blocks = ['waiting-check-pupils', 'success-passed-pupils', 'failed-pupils', 'not-passed-pupils']
var solution_results_keys = ['waiting', 'solved','failed', 'not pass']

function get_url_api_solutions_on_task(group_id, task_id){
    return `${url_api_solutions}/group/${group_id}/task/${task_id}`;
}


function add_pupil_status(pupils, block_ul, task_id){
    block_ul.html('');

    for(var index=0; index < pupils.length; index++){
        var pupil = pupils[index];
        var pupil_full_name = pupil.user.full_name;
        var li_html;

        if ('solution_id' in pupil){
            var url_for_solution = `/teacher/groups/${group_id}/lessons/${lesson.id}/task/${task_id}/pupil/${pupil.id}`;
            li_html = `<a href='${url_for_solution}'><li class="list-group-item list-group-item-action">${pupil_full_name}</li></a>`;
        }else{
            li_html = `<li class="list-group-item">${pupil_full_name}</li>`;
        }


        block_ul.append(li_html);
    }

    if(block_ul.html().length == 0){
        block_ul.append('<li class="list-group-item"></li>');
    }


}

function success_get_solutions(data, textStatus, jqXHR, task_index_in_lesson){
    var card_body = $('#' + task_index_in_lesson).find('.card-body');
    var task_id = lesson.tasks[task_index_in_lesson].id;

    for(var index=0; index < selector_pupils_blocks.length; index++){
        var selector_pupil = selector_pupils_blocks[index];
        var dict_key = solution_results_keys[index];

        var pupils = data[dict_key];
        var block_ul = card_body.find(`.${selector_pupil}`).find('ul');

        add_pupil_status(pupils, block_ul, task_id);
    }

    var success_passed_pupils_ul = card_body.find('.failed-pupils').find('ul');
    var failed_pupils_ul = card_body.find('.fa').find('ul');
    var not_passed_pupils_ul = card_body.find('.not-passed-pupils').find('ul');

}

function load_task_pupil_done_info(task_index_in_lesson){
    var task_id = lesson.tasks[task_index_in_lesson].id;
    $.ajax({
        url: get_url_api_solutions_on_task(group_id, task_id),
        type: "GET",
        success: function(data, textStatus, jqXHR){
                    success_get_solutions(data, textStatus, jqXHR, task_index_in_lesson);
                 },
        error: function(){alert("Произошла ошибка при загрузке учеников")},
    })
}

function task_results(task_index_in_lesson){
    if(selected_task !== null && selected_task != task_index_in_lesson){
        var card_prev_selected = $('#' + selected_task);
        card_prev_selected.find('#arrow').removeClass('fa-angle-up').addClass('fa-angle-down');
        card_prev_selected.find('.card-body').attr('hidden', true);
    }

    var card = $('#' + task_index_in_lesson);
    var card_body = card.find('.card-body');
    var is_hidden = false;

    var attr = card_body.attr('hidden');
    if (typeof attr !== typeof undefined && attr !== false) {
        is_hidden = true;
    }

    if(is_hidden){
        card.find('#arrow').removeClass('fa-angle-down').addClass('fa-angle-up');
        card_body.removeAttr('hidden');
        selected_task = task_index_in_lesson;

        load_task_block(task_index_in_lesson);
        load_task_pupil_done_info(task_index_in_lesson);
    }else{
        card.find('#arrow').removeClass('fa-angle-up').addClass('fa-angle-down');
        card_body.attr('hidden', true);
    }
}

function set_lesson_available(lesson_id, set_status){
    if (already_changing_lesson_status){
        return
    }

    var http_request_type;

    if(set_status){
        http_request_type = "PUT"
    }else{
        http_request_type = 'DELETE'
    }

    var data = {'lesson_id': lesson_id,
                'group_id': group_id}

    already_changing_lesson_status = true

    $.ajax({
        url: url_api_lesson_available,
        data: data,
        type: http_request_type,
        complete: function(jqXHR, textStatus){
                       location.reload()
                  }
    })
}

function start_contest(){
    var date_string = $('#datetime-input').val();
    if(!date_string.length){
        $('#datetime-error').text('Это поле объязательно')
        return;
    }

    var dateNow = new Date();

    var dateDeadline = new Date(date_string);

    var data = {'lesson_id': lesson.id,
                'group_id': group_id,
                'seconds_to_deadline': (dateDeadline - dateNow) / 1000 }
    $.ajax({
        url: url_api_lesson_available,
        data: data,
        type: "PATCH",
        success: function(){
                            location.reload();
                            },
        error: function(jqXHR, textStatus, errorThrown){
                            $('#datetime-error').text(jqXHR.responseJSON.message.seconds_to_deadline);
                        }
    });
}