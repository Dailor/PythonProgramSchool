url_api_user = '/admin/api_user';
url_set_role = url_api_user + '/set_role';


admin_role = 'ADMIN';
teacher_role = 'TEACHER';
pupil_role = 'PUPIL';

dataSrc = 'users';




test_data =  {
      "confident_info": "test success",
      "email": "admin@admin.com",
      "id": 1,
      "name": "1fgf",
      "password": "1",
      "roles": "ADMIN, TEACHER",
      "surname": "Admin"
    }

var dataTable_users;


function string_in_quotes(str){
    return "'" + str + "'";
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
    data = dataTable_users.row(user_id - 1).data();
    data.set_role = role;


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

           {id: 'roles',
            data: 'roles',
            title: 'Роли',
            type: 'readonly'},

            {id: 'set_role',
            title: "Назначить роли",
            type: 'readonly',
            render: function(data, type, row, meta){
                result = '';
                left_obj = false;


                if (!row.roles.includes(admin_role)){
                    params_function = string_in_quotes(admin_role) + ", " + row.id;
                    result += '<button class="btn btn-danger" onclick="set_role('  + params_function + ')">Админ</button>';
                    left_obj = true;
                }
                if (!row.roles.includes(teacher_role)){
                    params_function = string_in_quotes(teacher_role) + ", " + row.id;
                    result += '<button class="btn btn-warning' +  (left_obj?' ml-1':'') + '" onclick="set_role('  + params_function + ')">Учитель</button>';
                    left_obj = true;
                }
                if (!row.roles.includes(pupil_role)){
                    params_function = string_in_quotes(pupil_role) + ", " + row.id;
                    result += '<button class="btn btn-success'  +  (left_obj?' ml-1':'') + '" onclick="set_role('  + params_function + ')">Ученик</button>';
                }

                return result;
            },
            searchable: false
            },

            {id: 'confident_info',
            data:'confident_info',
            title: 'Личная информация',
            render: function(data, type, row){
                        return data.split("\n").join("<br/>");},
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
                    error(jqXHR, textStatus, errorThrown);
                    if('error' in jqXHR.responseJSON){
                        $(".modal-body").children(".alert").text(jqXHR.responseJSON.error).prepend(error_crud_msg);
                    }
                },
            });

        },
        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_user,
                type: 'DELETE',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error(jqXHR, textStatus, errorThrown);
                    if('error' in jqXHR.responseJSON){
                        $(".modal-body").children(".alert").text(jqXHR.responseJSON.error).prepend(error_crud_msg);
                    }
                },
            });
        },
        onEditRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_user,
                type: 'POST',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error(jqXHR, textStatus, errorThrown);
                    if('error' in jqXHR.responseJSON){
                        $(".modal-body").children(".alert").text(jqXHR.responseJSON.error).prepend(error_crud_msg);
                    }
                },
            });
        },

        dom:"<'row my-1'<'col-sm-6'B><'col-sm-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>"
    }
  );
});


