const api_course_url_add = "/teacher/api/course";
const add_course_error_span = $('#add-course-error');

$('#add_course').on('hide.bs.modal', function (event) {
    add_course_error_span.text('');
})

function ajax_success_add_course(data, textStatus, jqXHR){
    window.location.href = '/teacher/course/' + data['id'];
}

function ajax_fail_add_course(jqXHR, textStatus, errorThrown){
    add_course_error_span.text(textStatus);
}

function ajax_add_course(){
    var course_name = $('#inputCourseName').val();

    if (course_name.length == 0){
        add_course_error_span.text('Название должно состоять минимум из одного символа');
        return;
    }

    var data = {};
    data['name'] = course_name;

    $.ajax({
            url: api_course_url_add,
            type: 'PUT',
            data: data,
            success: ajax_success_add_course,
            error: ajax_fail_add_course,
        });
}