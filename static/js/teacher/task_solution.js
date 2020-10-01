const acceptedSolutionStatus = true;
const declinedSolutionStatus = false;

function successChangeReviewStatus(data, textStatus, jqXHR){
    changeSolutionReviewStatus(data);
}

function changeSolutionReviewStatus(solution){
    var solution_row = $(`#${solution_identify}${solution.id}`);
    var solution_review_status_data = solution_row.children('#solution-status');
    solution_review_status_data.html(status_span(solution.review_status));
}

function apiRequestChangeReviewStatus(review_status){
    if(last_solution_id == null) return;
    var data = {'solution_id': last_solution_id,
            'review_status': review_status};
    $.ajax({
        url: url_solution,
        type: "POST",
        data:data,
        success: successChangeReviewStatus
    })

}

function acceptSolution(){
    apiRequestChangeReviewStatus(acceptedSolutionStatus);
}

function declineSolution(){
    apiRequestChangeReviewStatus(declinedSolutionStatus);
}