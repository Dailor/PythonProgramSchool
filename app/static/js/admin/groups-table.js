var url_api_groups = '/admin/api_group';
var url_api_get_teachers_dict = '/admin/api_teacher/get_dict';
var url_api_get_subjects_dict = '/admin/api_subject/get_dict';
var active_status_dict = {1:'Обучается',
                          0: 'Закончен'};

var dataTable_groups;
var dataSrc = 'groups';

function wrap_in_tag(tag, string){
    return `<${tag}>${string}</${tag}>`;
}

function get_dict_from_api(url){
    $.ajax({
    async: false,
    url: url,
    success: function(data, textStatus, jqXHR){
    if(url == url_api_get_teachers_dict){
        teachers_dict = data;
    }
    else if(url == url_api_get_subjects_dict){
        subjects_dict = data;
    }},
    error: function(jqXHR, textStatus, errorThrown){
        alert("Произошла ошибка при загрузке данных, попробуйте перезагрузить страницу.");
    }
    })
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

           {id: 'is_active',
            required: true,
            data: 'is_active',
            title: 'Статус',
            type: 'select',

            options: active_status_dict,
            render: function(data, type, row, meta){
                        row.is_active = data + 0;
                        if (data == null || row == null) return null;
                        return active_status_dict[row.is_active];
                    }
            },

           {id: 'subject_id',
            required: true,
            data: 'subject_id',
            title: 'Предметы',
            type: 'select',
            options: subjects_dict,
            render: function(data, type, row, meta){
                        if (data == null || row == null) return null;
                        return subjects_dict[data];
                    }
            },

           {id: 'teacher_id',
            data: 'teacher_id',
            title: 'Учитель',
            type: 'select',
            options: teachers_dict,
            render: function(data, type, row, meta){
                        if (data == null || row == null) return null;
                        return teachers_dict[data];
                    }
            },

            {id: 'topics',
            data: 'topics_id_list',
            title: "Категории",
            type: 'select',
            select2 : { width: "100%",
                        theme: 'bootstrap4'},
            multiple : true,
            options: topics_dict,
            render: function(data, type, row, meta){
                        if (data == null || row == null) return null;
                        return data.map(topic_id => wrap_in_tag('div', topics_dict[topic_id])).join('\n');
            }}];

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
                "title" : "Добавить группу",
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
    dataTable_groups = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_groups,
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,

        onAddRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_groups,
                type: 'PUT',
                data: JSON.stringify(rowdata),
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                },
                contentType: "application/json; charset=utf-8",
            });
        },

        onEditRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_groups + '/' + rowdata.id,
                type: 'POST',
                data: JSON.stringify(rowdata),
                success: success,
                error: function(jqXHR, textStatus, errorThrown){
                    error_ajax_crud(error, jqXHR, textStatus, errorThrown);
                    },
                contentType: "application/json; charset=utf-8",
                })},

        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_groups + '/' + rowdata.id,
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


