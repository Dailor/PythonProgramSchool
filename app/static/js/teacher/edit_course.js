const api_course_url_edit = "/teacher/api/course";
const edit_course_error_span = $('#edit-course-error');
const inputCourseEditName = $('#inputCourseEditName');

$('#editCourse').on('show.bs.modal', function (event) {
    inputCourseEditName.val(course_name);
})

$('#editCourse').on('hide.bs.modal', function (event) {
    add_course_error_span.text('');
})

function ajax_success_edit_course(data, textStatus, jqXHR){
    window.location.href = '/teacher/courses/' + data['id'];
}

function ajax_fail_edit_course(jqXHR, textStatus, errorThrown){
    edit_course_error_span.text(textStatus);
}

function ajax_edit_course(){
    var course_name = inputCourseEditName.val();

    if (course_name.length == 0){
        edit_course_error_span.text('Название должно состоять минимум из одного символа');
        return;
    }

    var data = {};
    data['name'] = course_name;

    $.ajax({
            url: api_course_url_add + '/' + course_id,
            type: 'POST',
            data: data,
            success: ajax_success_edit_course,
            error: ajax_fail_edit_course,
        });
}