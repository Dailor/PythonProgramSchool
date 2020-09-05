function show_pupil(group_id){
    var pupils = groups[group_id].pupils;
    var pupils_ul_block = $('#pupils');
    pupils_ul_block.html('');
    for (var i in pupils){
        var pupil = pupils[i];
        var li_html = `<li class="list-group-item"><a class="nav-link p-0" href="/pupils/${pupil.id}">${pupil.user.full_name}</a></li>`;
        pupils_ul_block.append(li_html);
    }
}

$(document).ready(function(){
    for (var group_id in groups){
        show_pupil(group_id);
        break;
    }
})