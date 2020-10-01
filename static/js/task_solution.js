const wait_solution = 'На проверке';
const success_solution = 'Принято';
const failed_solution = 'Не принято';

const url_all_solutions = '/api_solutions';
const url_solution = '/api_solution'

var solutions_count = 0;
var last_solution_id = null;
var solution_identify = 'solution_'

var editor = CodeMirror(document.getElementById("codeMirror"),
                       {lineNumbers: true,
                        theme: "neat",
                        });

function scrollToBottomSolutionsHistory(){
    var container = document.getElementsByClassName('solutions-history')[0]
    container.scrollTop = container.scrollHeight;
}

function add_solution(solution){
    solutions_count++;
    var row = `
    <tr class="cursor-pointer" id='${solution_identify}${solution.id}' onclick=load_solution(${solution.id})>
        <th scope="row" id="solution-attempt-count">${solutions_count}</th>
        <td id="solution-date">${solution.date_delivery}</td>
        <td id="solution-status">${status_span(solution.review_status)}</td>
    </tr>
    `;
    last_solution_id = solution.id;
    $('#solutions').append(row);
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
                   }
    })
}

function load_solution(solution_id){
    var data = {"solution_id": solution_id};

    $.ajax({
        url: url_solution,
        type: 'GET',
        data: data,
        success: function(data, textStatus, jqXHR){
            set_solve_in_mirror_code(data.result);
        }
    })
    if(last_solution_id != null){
        $(`#${solution_identify}${last_solution_id}`).css('background-color', '#FFFFFF');
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
})