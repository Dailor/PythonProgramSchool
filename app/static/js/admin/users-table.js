url_api_user = '/admin/api/user';
url_set_role = url_api_user + '/role';


admin_role = 'Админ';
teacher_role = 'Учитель';
pupil_role = 'Ученик';

roles_setter_btn_class = [[admin_role, 'btn-danger'], [teacher_role, 'btn-warning'], [pupil_role, 'btn-success']]

dataSrc = 'users';


var dataTable_users;


function string_in_quotes(str){
    return "'" + str + "'";
}

function wrap_in_tag(tag, string){
    return `<${tag}>${string}</${tag}>`;
}

function error_ajax_crud(func_default, jqXHR, textStatus, errorThrown){
    func_default(jqXHR, textStatus, errorThrown);
    if('message' in jqXHR.responseJSON){
        var errors = jqXHR.responseJSON.message;
        if(typeof errors == "string"){
            $(".modal-body").children(".alert").text(errors).prepend(error_crud_msg);
        }
        else{
            for(var key in errors)
            $(".modal-body").children(".alert").text(jqXHR.responseJSON.message[key]).prepend(error_crud_msg);
        }
    }

}

function error_set_role(jqXHR, textStatus, errorThrown){
    if(! ('error' in jqXHR.responseJSON)){
        alert("Произошла ошибка при добавлении роли");
    }
    else{
        alert(jqXHR.responseJSON.error);
    }

}

function success_set_role(data, textStatus, jqXHR){
    console.log(jqXHR.responseJSON.roles);
    dataTable_users.row(jqXHR.responseJSON.id - 1).data(jqXHR.responseJSON).invalidate();
}

function set_role(role, user_id){
    data = {'id': user_id,
            'role': role
            }

    $.ajax({
        url: url_set_role,
        type: 'POST',
        data: data,
        success: success_set_role,
        error: error_set_role,
    });
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
            required: true,
            data: 'surname',
            title: 'Фамилия',
            type: 'text'},

           {id: 'email',
            required: true,
            data: 'email',
            title: 'Почта',
            type: 'email',
            // pattern:  "\\w+@[a-zA-Z]+?\\.[a-zA-Z]{2,6}",
            errorMsg: "*Неправильный формат почты",
            hoverMsg: "Пример: test@exmple.com",},

           {id: 'role_id',
            data: 'role_id',
            title: 'Роли',
            type: 'select',
            select2 : { width: "100%",
                        theme: 'bootstrap4'},
            options: all_roles,
            render: function(data, type, row, meta){
                if (data == null || row == null) return null;
                return all_roles[data];
            }},


            {id: 'confident_info',
            data:'confident_info',
            title: 'Личная информация',
            render: function(data, type, row){
                        var result = '';
                        var text_rows = data.split("\n");

                        for (var index in text_rows)
                            result+= wrap_in_tag('div', text_rows[index]);

                        return result;},
            type: 'textarea'},

            {id: 'password',
            data:'password',
            required: true,
            title: 'Пароль',
            type: 'password',
            errorMsg: "*Неправильный формат пароля",
            hoverMsg: "Пароль должне содержать как минимум 6 латинских букв в любом регистре",
            visible: false,
            searchable: false}];

buttons = [{text: 'Добавить',
                title: 'Добавить',
                name: 'add'},

                {extend: 'selected',
                 text: 'Изменить',
                 title: 'Изменить',
                 name: 'edit'},

                {extend: 'selected',
                 text: 'Удалить',
                 title: 'Удалить',
                 name: 'delete'},
                {
                text: 'Обновить',
                name: 'refresh'
                }
                 ];

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
  dataTable_users = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_user,
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,

        onAddRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_user,
                type: 'PUT',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                },
            });
        },
        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_user + '/' + rowdata.id,
                type: 'DELETE',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                },
            });
        },
        onEditRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_user + '/' + rowdata.id,
                type: 'POST',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                    }
                })},

        dom:"<'row my-1'<'col-sm-6'B><'col-sm-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>"
    }
  );
});


