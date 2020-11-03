function load_task_block(task_index_in_lesson){
    var task = lesson.tasks[task_index_in_lesson];

    var task_block = $('.selected_task');

    task_block.find('#taskName').text(task.name);
    task_block.find('#taskDescription').html(task.description);

    task_block.find("#timeLimit").text(task.time_sec);
    task_block.find("#memoryLimit").text(task.memory_mb);

    var tbodyDataExamples = task_block.find('#dataExamples');
    tbodyDataExamples.html('');

    for(var i=0; i < task.examples.length; i++){
        var example = task.examples[i];

        var trRowExample = $('<tr class="rowExample"></tr>');

        trRowExample.append(`<td class="p-0 dataIn">${example.in_data}</td>`)
        trRowExample.append(`<td class="p-0 dataOut">${example.out_data}</td>`)

        tbodyDataExamples.append(trRowExample);
    }

    $('.selected_task').removeAttr('hidden');
    MathJax.Hub.Typeset();

    if(window.location.href.includes('pupil/groups')){
        task_block.find('.card-body').find('button').attr('onclick', `redirect_page_solve(${task.id})`);
    }
}
