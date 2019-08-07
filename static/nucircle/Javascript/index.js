$('#signup_nav_link').click(function(){
    $('#signuptab').tab('show');
    $('html, body').animate({
        scrollTop: $("ul.nav-tabs").offset().top - 100
    }, 10);

});

$('#login_nav_link').click(function(){
    $('#logintab').tab('show');
    $('html, body').animate({
        scrollTop: $("ul.nav-tabs").offset().top - 100
    }, 10);

});
function emptyField(value){

    field = value.attr('name');
    value = value.val();
    if(value == ''){
        alert(field + ' is empty');
      return false;
    }
  
    return true;
  }

function usernameFormat(uname){

    // if(!(/^[A-Za-z0-9_]{1,}$/.test(uname))){
    //     alert('Username can only have A-Z, a-z, 0-9 or _');
    //   return false;
    // }
    return true;
}

function passwordFormat(password){

    if(!(/^[A-Za-z0-9@#$%^&+=]{8,}$/.test(password))){
        alert('Password At least 8 characters and restricted to A-Z, a-z, 0-9 or special characters');
      return false;
    }
    return true;
}


function matchPassword(p1, p2){
    
    if(p1 == p2){
      return true;
    }
    alert(p1 + ' Password mismatch ' + p2);
    return false;
}

function validate_login(){
    return  emptyField($('#login_username'))
    && emptyField($('#login_password'))
    &&  usernameFormat($('#login_username').val())
    &&  passwordFormat($('#login_password').val())
  }

  function validate_signup(){
    return  emptyField($('#signup_username'))
    && emptyField($('#signup_email'))
    && emptyField($('#signup_password_1'))
    && emptyField($('#signup_password_2'))
    &&  usernameFormat($('#signup_username').val())
    &&  passwordFormat($('#signup_password_1').val())
    &&  passwordFormat($('#signup_password_2').val())
    &&  matchPassword($('#signup_password_2').val(), $('#signup_password_1').val())

  }  