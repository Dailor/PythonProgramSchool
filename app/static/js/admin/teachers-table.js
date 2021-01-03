const url_api_teacher = '/admin/api/teacher';
const site_url = document.location.origin

dataSrc = 'teachers';

var dataTable_teacher;


function string_in_quotes(str){
    return "'" + str + "'";
}


columns = [{id: 'id',
            data: 'id',
            title: 'ID',
            type: 'hidden'
            },

           {id: 'name',
            data: 'name',
            title: 'Имя',
            type: 'text',},

           {id: 'surname',
            data: 'surname',
            title: 'Фамилия',
            type: 'text'},

           {id: 'email',
            data: 'email',
            title: 'Почта',
            type: 'text',
            },


            { id: 'subjects',
              data: 'subjects',
              title: 'Предметы',
              render: function(data, type, row){
                        return data.split("\n").join("<br/>");},
            },

            { id: 'groups',
              data: 'groups',
              title: 'Группы',
              render: function(data, type, row){
                        return data.split("\n").join("<br/>");},
            },

            {id: 'confident_info',
            data:'confident_info',
            title: 'Личная информация',
            render: function(data, type, row){
                        return data.split("\n").join("<br/>");},
            type: 'textarea'},
            ];

buttons = [

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
  dataTable_teacher = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_api_teacher,
            dataSrc: dataSrc
        },
        language: language,
        select : 'single',
        altEditor : true,
        buttons: buttons,


        onDeleteRow: function(datatable, rowdata, success, error) {
            $.ajax({
                url: url_api_teacher + '/' + rowdata.id,
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

        dom:"<'row my-1'<'col-sm-6'B><'col-sm-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-5'i><'col-sm-7'p>>"
    }
  );
});


