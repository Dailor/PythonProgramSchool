var selected_task = null;

function redirect_page_solve(task_id){
    window.location.href = `/pupil/groups/${group_id}/lesson/${lesson.id}/task/${lesson.tasks[task_id].id}`;
}

function load_task_block(task_id){
    var task = lesson.tasks[task_id];

    var task_block = $('.selected_task');
    task_block.find('#taskName').text(task.name);
    task_block.find('#taskDescription').html(task.description);

    var tbodyDataExamples = task_block.find('#dataExamples');
    tbodyDataExamples.html('');

    var trRowExample = $('<tr class="rowExample"></tr>');

    trRowExample.append(`<td class="p-0 dataIn">${task.in_data}</td>`)
    trRowExample.append(`<td class="p-0 dataOut">${task.out_data}</td>`)

    tbodyDataExamples.append(trRowExample);
    task_block.find('.card-body').find('button').attr('onclick', `redirect_page_solve(${task_id})`);
    $('.selected_task').removeAttr('hidden');
    MathJax.Hub.Typeset();
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