$(document).ready(function(){
    
    if($("#jumptowhat").val() == 'login'){
        $('#logintab').tab('show');
        
        if($("#error_field").val() == 'username'){
            $('#login_username').trigger('focus');                
        }
        if($("#error_field").val() == 'password'){
            $('#login_password').trigger('focus');                
        }

    }
    else if ($("#jumptowhat").val() == 'signup'){
        $('#signuptab').tab('show');

        
        if($("#error_field").val() == 'username'){
            
            $('#signup_username').trigger('focus');                
        }
        if($("#error_field").val() == 'email'){
            
            $('#signup_email').trigger('focus');                
        }
        if($("#error_field").val() == 'password_1'){
            
            $('#signup_password_1').trigger('focus');                
        }
        if($("#error_field").val() == 'password_2'){
            
            $('#signup_password_2').trigger('focus');                
        }

    }
       
    $('html, body').animate({
        scrollTop: $("ul.nav-tabs").offset().top - 100
    }, 10);


 

});


