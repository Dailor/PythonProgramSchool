const api_topic_url_edit = "/teacher/api_topics";
const edit_topic_error_span = $('#edit-topic-error');
const inputTopicEditName = $('#inputTopicEditName');

$('#editTopic').on('show.bs.modal', function (event) {
    inputTopicEditName.val(topic_name);
})

$('#editTopic').on('hide.bs.modal', function (event) {
    add_topic_error_span.text('');
})

function ajax_success_edit_topic(data, textStatus, jqXHR){
    window.location.href = '/teacher/topics/' + data['id'];
}

function ajax_fail_edit_topic(jqXHR, textStatus, errorThrown){
    edit_topic_error_span.text(textStatus);
}

function ajax_edit_topic(){
    var topic_name = inputTopicEditName.val();

    if (topic_name.length == 0){
        edit_topic_error_span.text('Название должно состоять минимум из одного символа');
        return;
    }

    var data = {};
    data['name'] = topic_name;

    $.ajax({
            url: api_topic_url_add + '/' + topic_id,
            type: 'POST',
            data: data,
            success: ajax_success_edit_topic,
            error: ajax_fail_edit_topic,
        });
}