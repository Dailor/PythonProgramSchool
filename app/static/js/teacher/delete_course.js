const api_course_url_delete = "/teacher/api/course";
const delete_course_error_p = $('#delete-course-error');

$('#deleteCourse').on('hide.bs.modal', function (event) {
    delete_course_error_p.text('');
})

function ajax_success_add_delete(data, textStatus, jqXHR){
    window.location.href = '/';
}

function ajax_fail_add_delete(jqXHR, textStatus, errorThrown){
    delete_course_error_p.text(textStatus);
}

function ajax_delete_course(){
    $.ajax({
            url: api_course_url_delete + '/' + course_id,
            type: 'DELETE',
            success: ajax_success_add_delete,
            error: ajax_fail_add_delete,
        });
}