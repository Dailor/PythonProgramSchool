var selected_task = null;

function redirect_page_solve(task_id){
    window.location.href = `/pupil/groups/${group_id}/lesson/${lesson.id}/task/${task_id}`;
}

function task_results(task_id){
    var card = $('#' + task_id);
    var card_body = card.find('.card-body');
    var is_selected = false;

    var attr = card_body.attr('selected');
    if (typeof attr !== typeof undefined && attr !== false) {
        is_selected = true;
    }

    if(is_selected){
        card.find('#arrow').removeClass('fa-angle-left').addClass('fa-angle-right');
        card_body.removeAttr('selected');
        selected_task = task_id;

        load_task_block(task_id);


    }else{
        card.find('#arrow').removeClass('fa-angle-right').addClass('fa-angle-left');
        card_body.attr('selected', true);
    }

}