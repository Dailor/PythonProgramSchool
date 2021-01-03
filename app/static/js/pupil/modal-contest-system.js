const api_contest_system_url = "/pupil/api/contest_system";

$('#change-profile').on('hide.bs.modal', function (event) {
    $('#form-change-contest-system-id #error, #success').text('')
})

$('#change-profile').on('show.bs.modal', function (event) {
    $.ajax({
        url: api_contest_system_url + '/pupil/' + pupilId,
        success: function(data, textStatus, jqXHR){
            for (contest_system_id in data){
                $(`form[contest-system-id=${contest_system_id}] input[type="text"]`).val(data[contest_system_id])
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
        }
    })
})



function change_id_in_contest_system(contest_system_id, id_in_contest_system){
    var data = {'id_in_contest_system': id_in_contest_system}

    $('#form-change-contest-system-id #error, #success').text('')
    $.ajax({
        url: api_contest_system_url + '/pupil/' + pupilId + '/contest_system_id/' + contest_system_id,
        type: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(data, textStatus, jqXHR){
            $(`form[contest-system-id=${contest_system_id}] #success`).text('Успешно изменилось')
        },
        error: function(jqXHR, textStatus, errorThrown){
            $(`form[contest-system-id=${contest_system_id}] #error`).text('Произошла ошибка')
        }
    })
}

function change_id_in_contest_system_form_submit(){
    var pressed_btn = event.currentTarget
    var div_contest_system = pressed_btn
    var input_contest_system = div_contest_system.getElementsByTagName('input')[0]

    var contest_system_id = parseInt(div_contest_system.getAttribute('contest-system-id'))
    var id_on_contest_system = input_contest_system.value

    change_id_in_contest_system(contest_system_id, id_on_contest_system)

    return false
}

