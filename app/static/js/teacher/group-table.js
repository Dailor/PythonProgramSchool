var url_api_groups = '/teacher/api/group';
var url_data = url_api_groups + '/' + group_id;

var dataTable_groups;
var dataSrc = 'pupils';

function wrap_in_tag(tag, string){
    return `<${tag}>${string}</${tag}>`;
}


columns = [{id: 'id',
            data: 'id',
            title: 'ID',
            type: 'readonly',
            },

           {id: 'name',
            data: 'user.full_name',
            title: 'Имя',
            type: 'text'},

           {id: 'confident_info',
            data: 'user.confident_info',
            title: 'Личная информация',
            type: 'text'},

            {id: 'profile_url',
            title: 'Действия',
            render: function(data, type, row, meta){
                return `<a href='/pupils/${row.id}'>Перейти в профиль</a>`;
            }}
        ];


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
    dataTable_groups = $("#dataTable").DataTable({
        columns: columns,
        ajax: {
            url: url_data,
            dataSrc: dataSrc
        },
        language: language,
    }
  );
});


