$(document).ready(function (){

  // аватар в профиле с картинки в background для bg-cover
  let user_avatar_image = $('.user-avatar img').attr('src');
  $('.user-avatar').css('background-image','url(' + user_avatar_image + ')');

  // поиск врачей
  $("#doc_search").autocomplete({
    source: "/lk/doc_search/",
    minLength: 2,
    select: function( event, ui ) {
			location.href += ui.item.doc_speciality_id + '/' + ui.item.doc_id + '/timetable';
      $(this).val('');
			event.preventDefault();
			return false;
    },
    open: function( event, ui ) {
      // подсветка написанного в поиске по врачам
      let input_text = $(this).val();
      let list = $('.ui-menu-item-wrapper');
      let source_part = "";
      let str = "";
      let i = 0;
      while (i < list.length) {
        str = $(list[i]).html();
        t_index = str.toLowerCase().indexOf(input_text.toLowerCase());
        t_len = input_text.length;
        source_part = str.substr(t_index, t_len);
        str = str.replace(new RegExp(input_text, 'gi'), "<span>" + source_part + "</span>");

        $(list[i]).html(str);
        i++;
      }
    }
  });

  // смена пароля
  $( "#change_pass_link" ).click(function() {
    $( 'div#change_pass_block' ).toggle(400);
		return false;
	})

  // активная вкладка у пользователя
  if(window.location.pathname.search('/lk/history/')  != -1)
    $('.menu ul .history-li').addClass('active');
  else if (window.location.pathname.search('/lk/record/') != -1)
    $('.menu ul .record-li').addClass('active');
  else if (window.location.pathname.search('/lk/schedule/') != -1)
    $('.menu ul .schedule-li').addClass('active');
  else if (window.location.pathname.search('/lk/contact/') != -1)
    $('.menu ul .contact-li').addClass('active');
  else if (window.location.pathname.search('/lk/info/') != -1)
  $('.menu ul .info-li').addClass('active');

  // сайдбар в личном кабинете
  $('.lk .sidebar .link').click(function(){
    let sidebar = $('.lk .sidebar .dropdown');
    sidebar.slideToggle();
    $('.sidebar-arrow').toggleClass('active-arrow');
  });

  // окрытие блока смены пароля при наличии ошибок
  if($(".user-profile .error-block p").length) {
    $( 'div#change_pass_block' ).toggle();
  }

  // сокрытие сайдбара при адаптиве
  $('#humburger-menu').click(function(){
      $('.lk .sidebar').toggleClass('show-lk-sidebar');
      $(this).children().toggleClass('burger-arrow-active');
  });

  // фильтр
  $('.lk .filter').click(function(){
    $('.lk .filter-block').slideToggle();
    $('.lk .filter img').toggleClass('active-arrow');
  });

  // сортировка в обратном направлении
  let history_sort_links = $('.tbl-head-order tr td a');
  for (let i = 0; i < history_sort_links.length; i++) {
    let element = $(history_sort_links[i]);
    let el_href = element.attr('href');
    // значение order текущего элемента
    let order_value = el_href.match(new RegExp('order' + '=([^&=]+)'))[1];
    // добавление - к ссылке 
    if (get_url_arg('order') == order_value){
      element.append('<img src="/static/images/arr-ico.png" title="Сортировать в другом направлении">');
      element.addClass('active-date-link');
      let end_href = el_href.replace('order=', 'order=-');
      element.attr('href', end_href);
    }
    else if(get_url_arg('order') == "-" + order_value) {
      element.append('<img src="/static/images/arr-ico.png" class="active-arrow" title="Сортировать в другом направлении">');
      element.addClass('active-date-link');
    }
  }


// --------- Модальные окна --------------
  // закрытие модалки
  $(document).on("click", "span.close", function() {
    $(this).parent().dialog( "close" );
    return false;
    });

    // закрытие модалки кнопкой
    $("#modal-close-button").click(function() {
    $(this).parent().parent().dialog( "close" );
    return false;
  });


  // модалка об успешном запросе в обратную связь
  if ($('.contact .h-block').html() == '1') {
    console.log('Okay');
    $('#contact-dialog').dialog({
      'dialogClass': "Dialog",
      'resizable': false,
      'draggable': false,
      'modal': true,
      'width': 500
    });
  }

  // модалка на подтверждение отмены записи
  let id_annulment_record;
  $('.annulment-block').click(function() {
    $('#annulment-dialog').dialog({
      'dialogClass': "Dialog",
      'resizable': false,
      'draggable': false,
      'modal': true,
      'width': 500
    });

    id_annulment_record = this;
  });

  // кнопка в модалке отмены записи
  $('#annulment-button').click(function() {
    let rel = $(id_annulment_record).attr('data-rec-id');
    $(this).attr('href', rel);
  });



  
  

});

// получение гет параметра с поисковой строки
function get_url_arg(key) {
  var p = window.location.search;
  p = p.match(new RegExp(key + '=([^&=]+)'));
  return p ? p[1] : false;
}