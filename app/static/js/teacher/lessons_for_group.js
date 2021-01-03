const api_group_url = "/teacher/api/group/"

function getAlertWindow(){
    return $(`<div class="alert alert-dismissible fade show" id="" role="alert">
              <div id="message"></div>
              <button type="button" class="close" data-dismiss="alert" aria-label="Закрыть">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            `)
}


function copyInvite() {
    var invite_code_input = $("#urlInvite")
    var invite_code = invite_code_input.val()
    var urlInvite = window.location.host + '/invite_to_group/' + invite_code
    invite_code_input.val(urlInvite).select()
    document.execCommand("copy")
    invite_code_input.val(invite_code)
}

function generateNewInvite(){
   var alertMsg = getAlertWindow()
   var alertsBlock = $("#alertsBlock")

   $.ajax({
        url: api_group_url + groupId,
        type: "PATCH",
        success: function(data, textStatus, jqXHR){
            alertMsg.addClass("alert-success")
            alertMsg.find('#message').text('Новое приглашение скопировано')

            $('#urlInvite').val(data.group.invite_code)
        },
        error: function(jqXHR, textStatus, errorThrown){
            alertMsg.addClass("alert-warning")
            alertMsg.find('#message').text('Ошибка при получении нового приглашения')
        },
        complete: function(data) {
            alertsBlock.prepend(alertMsg)
        }

   })
}