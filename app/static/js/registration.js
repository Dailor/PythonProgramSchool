var formControlSubjectsSelect;
var formControlGroupsSelect;

$(document).ready(function() {
    formControlSubjectsSelect = $('#FormControlSubjects');
    formControlGroupsSelect = $('#FormControlGroups');

    formControlSubjectsSelect.val(null).trigger('change');
    formControlGroupsSelect.val(null).trigger('change');

    formControlSubjectsSelect.select2({theme: 'bootstrap4'});
    formControlGroupsSelect.select2({theme: 'bootstrap4'});
});

$('#FormControlSubjects').on('select2:select', function (e) {
  var subject_id = e.params.data.id;
  var groups_studying_subject = groups_by_subject_dict[subject_id]['groups'];

  for (var i in groups_studying_subject){
    var group_info = groups_studying_subject[i];
    var row_option = `<option value="${group_info.id}">${group_info.name}</option>`;
    formControlGroupsSelect.append(row_option);
  }
});

$('#FormControlSubjects').on('select2:unselect', function (e) {
  var subject_id = e.params.data.id;
  var groups_studying_subject = groups_by_subject_dict[subject_id]['groups'];
  for (var i in groups_studying_subject){
    var group_info = groups_studying_subject[i];
    formControlGroupsSelect.find(`option[value='${group_info.id}']`).remove();
  }
});

function submit_form(){
    console.log(1);
    return false;
}