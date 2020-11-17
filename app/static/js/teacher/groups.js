const group_api_url = '/teacher/api_group/'
const group_data_ = 'group-data-';

var groupTopicsSelect;
var editing_group_id = null;

$('#change-topics').on('show.bs.modal', function (e) {
    $('#group-name').text(groups[editing_group_id].name);

    $('#group-name-input').val(groups[editing_group_id].name);
    $('#group-status').val(groups[editing_group_id].is_active + 0);
    $('#group-subject').val(groups[editing_group_id].subject_id);

    groupTopicsSelect.val(groups[editing_group_id].topics.map(function(topic){
        return topic.id;
    }));
    groupTopicsSelect.trigger('change');
})

$('#change-topics').on('hide.bs.modal', function (e) {
  editing_group_id = null;
  $('#change-topics').val(null).trigger('change');
})

function editing_group_now(group_id){
    editing_group_id = group_id;
}

function success_editing_group(data, textStatus, jqXHR){
    groups[editing_group_id].topics = data.topics;
    groups[editing_group_id].name = data.name;
    groups[editing_group_id].is_active = data.is_active;
    groups[editing_group_id].subject_id = data.subject_id;
    $(`#${group_data_ + editing_group_id} #group-name-view`).html(data.name);
    $('#change-topics').modal('hide');
}

function failed_editing_group(jqXHR, textStatus, errorThrown){
    alert(textStatus);
}

function send_changed_group(){
    var name = $('#group-name-input').val();
    var is_active = $('#group-status').val();
    var subject_id = $('#group-subject').val();
    var topics_id_list = $('#group-topics').val().map(parseInt);

    var data = new Object();
    data.name = name;
    data.is_active = is_active;
    data.subject_id = subject_id;
    data.topics_id_list = topics_id_list;

    $.ajax({
        url: group_api_url + editing_group_id,
        data: JSON.stringify(data),
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        success: success_editing_group,
        error: failed_editing_group
    })
}

function show_pupil(group_id){
    var pupils = groups[group_id].pupils;
    var pupils_ul_block = $('#pupils');
    pupils_ul_block.html('');
    for (var i in pupils){
        var pupil = pupils[i];
        var li_html = `<li class="list-group-item"><a class="nav-link p-0" href="/pupils/${pupil.id}">${pupil.user.full_name}</a></li>`;
        pupils_ul_block.append(li_html);
    }
}


$(document).ready(function(){
    groupTopicsSelect = $('#group-topics');
    groupTopicsSelect.select2({theme: 'bootstrap4'});

    for (var group_id in groups){
        show_pupil(group_id);
        break;
    }
})