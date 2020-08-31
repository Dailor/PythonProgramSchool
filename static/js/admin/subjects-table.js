url_api_subject = '/admin/api_subject';


dataSrc = 'subjects';


var dataTable_subjects;

function wrap_in_tag(tag, string){
    return `<${tag}>${string}</${tag}>`;
}

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
            title: 'Название',
            type: 'text'},

           {id: 'teachers',
            data: 'teachers_names',
            title: 'Учителя',
            type: 'readonly',
            render: function(data, type, row, meta){
                var result = ''
                for (index in data)
                    result += wrap_in_tag('div', data[index]);
                return result;}},

           {id: 'groups',
            data: 'groups_names',
            title: 'Группы',
            type: 'readonly',
            render: function(data, type, row, meta){
                var result = ''
                for (index in data)
                    result += wrap_in_tag('div', data[index]);
                return result;
            }
            }
           ];

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
                "title" : "Добавить предмет",
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
  dataTable_subjects = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_subject,
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,

        onAddRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_subject,
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
                url: url_api_subject + '/' + rowdata.id,
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
                url: url_api_subject + '/' + rowdata.id,
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


