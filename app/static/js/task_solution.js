const wait_solution = 'На проверке';
const success_solution = 'Принято';
const failed_solution = 'Не принято';

const url_all_solutions = '/api/solutions';
const url_solutions_checker = '/api/solution'
const url_get_solution_on_task = '/pupil/api/solution_on_task';

const time_check_task = 5000;

var all_solutions = {};

var tries_left;

var solutions_count = 0;
var last_solution_id = null;
var solution_identify = 'solution_'
var solution_info_modal = $('#solutionInfo');

var editor = CodeMirror(document.getElementById("codeMirror"),
                       {lineNumbers: true,
                        theme: "neat",
                        matchBrackets: true,
                        autoCloseBrackets: true,
                        mode: language_mime_type,
                        });

function scrollToBottomSolutionsHistory(){
    var container = document.getElementsByClassName('solutions-history')[0]
    container.scrollTop = container.scrollHeight;
}

function add_solution(solution){
    solutions_count++
    var row = `
    <tr class="cursor-pointer" id='${solution_identify}${solution.id}' solution-id='${solution.id}' onclick=load_solution(${solution.id})>
        <th scope="row" id="solution-attempt-count">${solutions_count}</th>
        <td id="solution-date">${moment(new Date(solution.date_delivery_iso)).local().format('LLLL')}</td>
        <td id="solution-status">${status_span(solution.review_status)}</td>
    </tr>
    `;
    last_solution_id = solution.id;
    var row_dom_element = $(row);
    row_dom_element.dblclick(function(event){
        var solution_id_clicked = event.target.parentElement.getAttribute('solution-id');
        setSolutionInfoInModal(solution_id_clicked);
    });
    $('#solutions').append(row_dom_element);

    all_solutions[solution.id] = solution;
    if(solution.review_status == null){
        setCheckerOnTimer(solution.id);
    }
}

function setSolutionInfoInModal(solution_id_clicked){
    var solution_by_id = all_solutions[solution_id_clicked];
    var solution_info_clicked = solution_by_id.solution_info;

    if(solution_info_clicked === null){
        return;
    }

    solution_info_modal.find('#modal-solution-info').html('');

    if(solution_by_id.review_status == null){
        return;
    }

    solution_info_modal.modal();

    var solution_info_modal_body = solution_info_modal.find('#modal-solution-info');

    var info_p;
    info_p = $('<p></p>');
    info_p.text(`Всего тестов: ${solution_info_clicked.tests_count}`);
    solution_info_modal_body.append(info_p);

    info_p = $('<p></p>');
    info_p.text(`Пройдено: ${solution_info_clicked.passed}`);
    solution_info_modal_body.append(info_p);

    info_p = $('<p></p>');
    info_p.text(`Не пройдено: ${solution_info_clicked.failed}`);
    solution_info_modal_body.append(info_p);

    info_p = $('<p></p>');
    info_p.text(`Максимальное время: ${solution_info_clicked.max_time} секунд`);
    solution_info_modal_body.append(info_p);

    info_p = $('<p></p>');
    info_p.text(`Максимальное потребление памяти: ${solution_info_clicked.max_memory} МБ`);
    solution_info_modal_body.append(info_p);

    info_p = $('<p></p>');
    info_p.text(`Ошибки: ${solution_info_clicked.errors}`);
    solution_info_modal_body.append(info_p);
}

function status_span(status){
    if (status == true)
        return `<span class='text-success'>${success_solution}</span>`;
    if (status == false)
        return `<span class='text-danger'>${failed_solution}</span>`;
    return `<span class='text-warning'>${wait_solution}</span>`;
}

function load_all_solutions(){
    var data = {
            'pupil_id': pupil_id,
            'group_id': group_id,
            'task_id': task_id,
    }

    $.ajax({
        url: url_all_solutions,
        type: "GET",
        data: data,
        success: function(data, textStatus, jqXHR){
                    for(var i=0; i < data.solutions.length; i++){
                        var solution = data.solutions[i];
                        add_solution(solution);
                    }
                    if(last_solution_id != null){
                        load_solution(last_solution_id);
                        $('#acceptSolution').removeAttr('disabled');
                        $('#declineSolution').removeAttr('disabled');
                        }
                    scrollToBottomSolutionsHistory()
                    tries_left = data.tries_left;
                    $('#tries-left').html(tries_left);

                    if(tries_left <= 0){
                        $('#sendSolution').attr('disabled', true);
                    }
                    getSolutionOnText();
                   }
    })
}

function load_solution(solution_id){
    var data = {"solution_id": solution_id};

    set_solve_in_mirror_code(all_solutions[solution_id].result);

    if(last_solution_id != null){
        $('#solutions').find('tr').css('background-color', '#FFFFFF')
    }
    $(`#${solution_identify}${solution_id}`).css('background-color', '#DEDEDE');
    last_solution_id = solution_id;
}

function set_solve_in_mirror_code(result){
    editor.setValue(result);
}

$(document).ready(function(){
    load_all_solutions();
    if(is_teacher == true){
        editor.doc.cantEdit = true;
    }
    if(deadline){
        start_timer('deadline', new Date(deadline), 'lesson_deadline');
    }
})

function changeSolutionReviewStatus(solution){
    var solution_row = $(`#${solution_identify}${solution.id}`);
    var solution_review_status_data = solution_row.children('#solution-status');
    solution_review_status_data.html(status_span(solution.review_status));
    return solution_row;
}

function setCheckerOnTimer(solution_id){
    var data = {"solutions_id": solution_id};
//    for(var sol_id in all_solutions){
//        if(all_solutions[sol_id].review_status === null){
//            data.solutions_id.push(sol_id);
//        }
//    }
    $.ajax({
        url: url_solutions_checker,
        type: 'GET',
        data: data,
        success: function(data, textStatus, jqXHR){
            var solution_before_change = all_solutions[data.id];

            if(solution_before_change.review_status != data.review_status){
                changeSolutionReviewStatus(data);
                solution_before_change.review_status = data.review_status;
                solution_before_change.solution_info = data.solution_info;
            }

            if(data.review_status == null){
                    setTimeout(setCheckerOnTimer, time_check_task, solution_id)
            }
        },
        error: function(textStatus){
            console.log(textStatus);
        }
    });
}


function success_ajax_get_solution_on_task(data, textStatus, jqXHR){
    var solution_block = $('#SolutionOnTask');
    solution_block.removeAttr('hidden');
    solution_block.find('p').html(data.solution);
}


function getSolutionOnText(){
    var data = {'group_id': group_id,
                'task_id': task_id};
    $.ajax({
        url: url_get_solution_on_task,
        type: 'GET',
        data: data,
        success: success_ajax_get_solution_on_task,
        error: function(jqXHR, textStatus, errorThrown){
            console.log(textStatus);
        }
    });
}
