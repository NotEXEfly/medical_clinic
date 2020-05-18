$(document).ready(function (){

    let current_time;
    // нажатие на свободную кнопку
    $(".timetable .free").click(function() {
        $('#dialog').dialog({
            'dialogClass': "Dialog",
            'resizable': false,
            'draggable': false,
            'modal': true,
            'width': 600
        });
        // дата время в модалке
        $('.record-datetime').html($(this).attr('rel'));
        
        current_time = this;
    });

    // добавление ссылки кнопке подтвердить
    $('#record-button').click(function() {
        if($(this).hasClass('disabled')) {
            $(current_time).attr('href', 'javascript:;')
            return false;
        }
        else {
            let rel = "?rec_date=" + $(current_time).attr('data-ftime');
            $(this).attr('href', rel);
        }
    });

    // активация кнопки "подтвердить" при согласии
    $( "#agree" ).change(function() {
		$( "#record-button" ).toggleClass('disabled', !$(this).is(':checked'));
		return false;
	})
	
});