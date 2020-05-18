// сокрытие блока ошибок если их нет
 $(document).ready(function() {
  if($(".text").children('p').length == 0)
    $(".text").hide()
  else 
    $(".text").show()
 });
// ------------- валидация регистрации -------------
let regAvatarOkay = false;
$('#reg-button').click(function() {
  let errorDiv = $('.registration .text');

  let regErrors = "";
  let regName = $("#id_fio");
  let regMail = $("#id_email");
  let regLogin = $("#id_username");
  let regPass1 = $("#id_password1");
  let regPass2 = $("#id_password2");

  let regLoginB = false;
  let regLogin2B = false;

  if(isValidName(regName.val())) {
    regName.css('background-color', '#b9f5c9');
  } else {
    regName.css('background-color', '#f18686');
    regErrors += "<p>В ФИО должно содержаться только кириллица, без цифр и знаков препинания</p>";
  }

  if(isValidEmail(regMail.val())) {
    regMail.css('background-color', '#b9f5c9');
  } else {
    regMail.css('background-color', '#f18686');
    regErrors += "<p>E-mail должен быть вида email@mail.ru</p>";
  }

  if(isValidPassword(regPass1.val())) {
    regPass1.css('background-color', '#b9f5c9');
  } else {
    regPass1.css('background-color', '#f18686');
    regErrors += "<p>Пароль должен содержать не менее 6 символов английской раскладки, верхнего и нижнего регистра</p>";
  }

  if(isValidSecondPassword(regPass1.val(), regPass2.val())) {
    regPass2.css('background-color', '#b9f5c9');
  } else {
    regPass2.css('background-color', '#f18686');
    regErrors += "<p>Пароли не совпадают</p>";
  }

  if(isValidAvatar() || regAvatarOkay) {
    $("input[type=file]").css('background-color', '#b9f5c9');
  } else {
    $("input[type=file]").css('background-color', '#f18686');
    regErrors += "<p>Аватар не должен превышать размер в 2mb</p>";
  }

  // логин
  // прверка на занятость
  $.ajax({
    async: false,
    url: "/checkUserName",
    type: "GET",
    data: {u_login: regLogin.val()},
    success: function(data) {
      if(data == 1)
        regLoginB = false;
      else
        regLoginB = true;
    }
  });

  if(isValidLogin(regLogin.val())) {
    regLogin2B = true;
  }
  else {
    regLogin2B = false;
    regErrors += "<p>Логин должен состоять из 4 - 12 символов</p>";
  }

  if(!regLoginB) {
    regErrors += "<p>Такой логин уже занят</p>"
  }

  if(regLoginB && regLogin2B) {
    regLogin.css('background-color', '#b9f5c9');
  } else {
    regLogin.css('background-color', '#f18686');
  }

  // ********************************
  // если все правильно регаем
  // && regAvatarB  regErrors == ""
  // ********************************
  if(regErrors == "") {
    $("form").submit();
  }
  // выводим ошибки
  else {
    errorDiv.show();
    errorDiv.html(regErrors);
  }

});

// загрузка фото, предварительный показ
$('input[type=file]').change(function(event) {
  // чистим output
  $('#output').html("");
  // получаем файл
  let avatar = event.target.files[0];
  let reader = new FileReader();
  reader.onload = (function(theFile) {
    return function(e){
      let span = document.createElement('span');
      span.innerHTML = ['<img class="thumb" title="', escape(theFile.name), '" src="', e.target.result, '" />'].join('');
      document.getElementById('output').insertBefore(span, null);
    };
  })(avatar);
  reader.readAsDataURL(avatar);

  // проверка размера аватара
  if(avatar.size <= 2097152) 
    regAvatarOkay = true
  else 
    regAvatarOkay = false
  console.log(avatar.size);
});
// --------------------------------------


function isValidName(name) {
return /^([А-яёЁ][А-яёЁ]+[\-\s]?){3,}/.test(name);
}

function isValidEmail(email) {
return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,6})+$/.test(email);
}

function isValidPassword(password) {
  return /^[0-9a-zA-Z]{6,}/.test(password);
}

function isValidSecondPassword(firstPass, secondPass) {
  return firstPass === secondPass && isValidPassword(secondPass);
}

function isValidAvatar() {
  // проверка на существование
  if($("#output").html() == "") return true;
}

function isValidLogin(login) {
  return /^([@a-zA-Z0-9\-\.\_\*]){4,12}$/gi.test(login);
}