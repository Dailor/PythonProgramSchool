const api_topic_url_delete = "/teacher/api_topics";
const delete_topic_error_p = $('#delete-topic-error');

$('#deleteTopic').on('hide.bs.modal', function (event) {
    delete_topic_error_p.text('');
})

function ajax_success_add_delete(data, textStatus, jqXHR){
    window.location.href = '/';
}

function ajax_fail_add_delete(jqXHR, textStatus, errorThrown){
    delete_topic_error_p.text(textStatus);
}

function ajax_delete_topic(){
    $.ajax({
            url: api_topic_url_delete + '/' + topic_id,
            type: 'DELETE',
            success: ajax_success_add_delete,
            error: ajax_fail_add_delete,
        });
}