var url_api_topics = '/admin/api/course';

var dataTable_topics;
var dataSrc = 'courses';

function wrap_in_tag(tag, string){
    return `<${tag}>${string}</${tag}>`;
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
            type: 'hidden',
            },

           {id: 'name',
            required: true,
            data: 'name',
            title: 'Название',
            type: 'text'},

           {id: 'groups_id',
            data: 'groups_id',
            title: 'Группы',
            type: 'hidden',
            render: function(data, type, row, meta){
                        if (data == null || row == null) return null;
                        return data.map(group_id => wrap_in_tag('div', groups_dict[group_id])).join('\n');
                    }
            },

           {id: 'curators_id',
            required: true,
            data: 'curators_id',
            title: 'Учитель',
            type: 'select',
            options: teachers_dict,
            render: function(data, type, row, meta){
                        if (data == null || row == null) return null;
                        return teachers_dict[data];
                        return data.map(teacher_id => wrap_in_tag('div', teachers_dict[teacher_id])).join('\n');
                    }
            },

           {id: 'lessons_count',
            data: 'lessons_count',
            title: 'Количество уроков',
            type: 'hidden',
            }]


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
                "title" : "Добавить категорию",
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
    dataTable_topics = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_topics,
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,

        onAddRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_topics,
                type: 'PUT',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                },
            });
        },

        onEditRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_topics + '/' + rowdata.id,
                type: 'POST',
                data: rowdata,
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                    }
                })},

        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_topics + '/' + rowdata.id,
                type: 'DELETE',
                data: rowdata,
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


