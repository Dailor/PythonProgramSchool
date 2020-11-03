const acceptedSolutionStatus = true;
const declinedSolutionStatus = false;

function successChangeReviewStatus(data, textStatus, jqXHR){
    changeSolutionReviewStatus(data);
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