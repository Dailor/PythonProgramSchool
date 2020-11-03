const api_topic_url_add = "/teacher/api_topics";
const add_topic_error_span = $('#add-topic-error');

$('#add_topic').on('hide.bs.modal', function (event) {
    add_topic_error_span.text('');
})

function ajax_success_add_topic(data, textStatus, jqXHR){
    window.location.href = '/teacher/topics/' + data['id'];
}

function ajax_fail_add_topic(jqXHR, textStatus, errorThrown){
    add_topic_error_span.text(textStatus);
}

function ajax_add_topic(){
    var topic_name = $('#inputTopicName').val();

    if (topic_name.length == 0){
        add_topic_error_span.text('Название должно состоять минимум из одного символа');
        return;
    }

    var data = {};
    data['name'] = topic_name;

    $.ajax({
            url: api_topic_url_add,
            type: 'PUT',
            data: data,
            success: ajax_success_add_topic,
            error: ajax_fail_add_topic,
        });
}