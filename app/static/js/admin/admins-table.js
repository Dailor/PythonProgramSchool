url_api_user = '/admin/api/user';
url_set_role = url_api_user + '/role';

admin_role = 'Админ';
teacher_role = 'Учитель';
pupil_role = 'Ученик';

role_in_this_table = admin_role;

dataSrc = 'users';


var dataTable_admins;


function string_in_quotes(str){
    return "'" + str + "'";
}

function error_ajax_crud(func_default, jqXHR, textStatus, errorThrown){
    func_default(jqXHR, textStatus, errorThrown);
    if('error' in jqXHR.responseJSON){
        $(".modal-body").children(".alert").text(jqXHR.responseJSON.error).prepend(error_crud_msg);
    }
    else if('message' in jqXHR.responseJSON){
        for(var key in jqXHR.responseJSON.message)
        $(".modal-body").children(".alert").text(jqXHR.responseJSON.message[key]).prepend(error_crud_msg);
    }

}


columns = [{id: 'id',
            data: 'id',
            title: 'ID',
            type: 'readonly',
            },

           {id: 'name',
            required: true,
            data: 'name',
            title: 'Имя',
            type: 'text'},

           {id: 'surname',
            attr: {required: true},
            data: 'surname',
            title: 'Фамилия',
            type: 'text'},

           {id: 'email',
            required: true,
            data: 'email',
            title: 'Почта',
            type: 'text',
            pattern:  "\\w+@[a-zA-Z]+?\\.[a-zA-Z]{2,6}",
            errorMsg: "*Неправильный формат почты",
            hoverMsg: "Пример: test@exmple.com",},

            {id: 'confident_info',
            data:'confident_info',
            title: 'Личная информация',
            render: function(data, type, row){
                        return data.split("\n").join("<br/>");},
            type: 'textarea'}]


var buttons = [{extend: 'selected',
            text: 'Удалить',
            title: 'Удалить',
            name: 'delete'},

            {text: 'Обновить',
             name: 'refresh'
                }];

error_crud_msg = "<strong>Ошибка: </strong>"

language = {
      "processing": "Подождите...",
      "search": "Поиск:",
      "lengthMenu": "Показать _MENU_ записей",
      "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
      "infoEmpty": "Записи с 0 до 0 из 0 записей",
      "infoFiltered": "(отфильтровано из _MAX_ записей)",
      "infoPostFix": "",
      "loadingRecords": "Загрузка записей...",
      "zeroRecords": "Записи отсутствуют.",
      "emptyTable": "В таблице отсутствуют данные",
      "paginate": {
        "first": "Первая",
        "previous": "Предыдущая",
        "next": "Следующая",
        "last": "Последняя"
      },
      "aria": {
        "sortAscending": ": активировать для сортировки столбца по возрастанию",
        "sortDescending": ": активировать для сортировки столбца по убыванию"
      },
      "select": {
        "rows": {
          "_": "Выбрано записей: %d",
          "0": "Кликните по записи для выбора",
          "1": "Выбрана одна запись"
        }
      },
      "altEditor" : {
            "modalClose" : "Отмена",
            "edit" : {
                "title" : "Изменить",
                "button" : "Изменить"
            },
            "add" : {
                "title" : "Добавить пользователя",
                "button" : "Создать"
            },
            "delete" : {
                "title" : "Удалить",
                "button" : "Удалить"
            },
            "success" : "Успешно.",
            "error" : {
                "message" : "Произошла непредвиденая ошибка",
                "label" : "Ошибка",
                "responseCode" : "Response code:",
            }
        }
    };


// Call the dataTables jQuery plugin
$(document).ready(function() {
  dataTable_admins = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_user,
            data: {'role':  role_in_this_table},
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,


        onDeleteRow: function(datatable, rowdata, success, error) {
            var data = {'id': rowdata.id,
                    'role': role_in_this_table};
            $.ajax({
                url: url_set_role,
                type: 'DELETE',
                data: data,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                },
            });
        },

        dom:"<'row my-1'<'col-sm-6'B><'col-sm-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>"
    }
  );
});


