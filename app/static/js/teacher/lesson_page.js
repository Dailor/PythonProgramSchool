var url_api_lesson_available = '/teacher/lesson_available_api';
var url_api_solutions = '/teacher/api_solutions/';
var async_http_already = false;
var selected_task = null;

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

function success_set_lesson_available(data, textStatus, jqXHR, lesson_id, set_status){
    var div_lesson_available_switcher = $('#lesson_available_switcher');

    if(!set_status){
        div_lesson_available_switcher.html('<h5 class="my-3"><span class="fas fa-eye"></span> Показать урок</h5>');
    }else{
        div_lesson_available_switcher.html('<h5 class="my-3"><span class="fas fa-eye-slash"></span> Скрыть урок</h5>');
    }

    div_lesson_available_switcher.attr('onclick', `set_lesson_available(${lesson_id}, ${!set_status})`);
};

function error_set_lesson_available(jqXHR, textStatus, errorThrown){
    location.reload();
};

function set_lesson_available(lesson_id, set_status){
    var http_request_type;

    if(set_status){
        http_request_type = "PUT";
    }else{
        http_request_type = 'DELETE';
    }

    var data = {'lesson_id': lesson_id,
                'group_id': group_id}

    if (async_http_already){
        return
    }

    async_http_already = true;

    $.ajax({
        url: url_api_lesson_available,
        data: data,
        type: http_request_type,
        success: function(data, textStatus, jqXHR){
                    success_set_lesson_available(data, textStatus, jqXHR, lesson_id, set_status);
                },
        error: error_set_lesson_available,
        complete: function(jqXHR, textStatus){
                   async_http_already = false;
                  }
    })
}