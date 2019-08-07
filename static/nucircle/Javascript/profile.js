

var imageTypes = ['image/jpeg', 'image/pjpeg', 'image/png'];
var globalIdCount = 0;
var postCount = 0;

// posts array
var postUsers = [
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  },
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  },
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  },
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  },
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  },
  {
    post_profile_img: "Images/user-avatar.jpg",
    post_user_name: "User Name ",
    post_date: "March 5, 2019",
    post_user_title: "Software Engineer",
    post_text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    post_img: "Images/b2.jpg",
    comment_profile_img: "Images/user-avatar.jpg"
  }
];


// change order of suggestions column
if (window.innerWidth < 992) {

  var mainContent = document.getElementById("main-content");
  var classList = mainContent.getAttribute("class");
  classList += " order-12";
  mainContent.setAttribute("class", classList);

}


// toggle like icon
function toggleLike(element) {

  var iconNode = element.firstChild;
  var iconClass = iconNode.getAttribute("class");

  if (iconClass == "far fa-thumbs-up") {
    iconClass = "fas fa-thumbs-up";
  }
  else if (iconClass == "fas fa-thumbs-up") {
    iconClass = "far fa-thumbs-up";
  }

  iconNode.setAttribute("class", iconClass);
}

// hiding default upload button and making icon work
$("#upload_default").css('opacity','0');
    
$("#upload_image").click(function(e) {

  e.preventDefault();
  $("#upload_default").trigger('click');

});


function isTypeValid(file) {
  for(var i = 0; i < imageTypes.length; i++) {
    if(file.type === imageTypes[i]) {
      return true;
    }   
  }
}


$(document).ready(function(){

  $('#upload_default').change(function(){
    
    var uploaded_file_list = document.getElementById("upload_default").files;
 
    if(uploaded_file_list.length !== 0) {
  
      var uploaded_file = uploaded_file_list[0];
      
      if(isTypeValid(uploaded_file)) { 
          $(this).closest('form').submit();
      }
      else {
        alert('File type not supported! Try uploading ".png", ".jpg" or ".jpeg" files.');
      }
  
    } 
  });    


  


});



function jumpAndShowError(error_form, error) {
 
  switch(error_form) {
    case 'edit_personal_info':
      $('#editInfo').modal();
    break; 
 
    case 'add_education':
      $('#addEducation').modal();
    break; 

    case 'edit_education':
      $('#editEdu').modal();
    break; 
    
    case 'add_accomplishment':
    $('#addAccomplishment').modal();
    break; 

    case 'edit_accomplishment':
    $('#editAcomp').modal();
    break; 
    
    case 'add_experience':
    $('#addExperience').modal();
    break; 

    case 'edit_experience':
    $('#editExp').modal();
    break;
    
    case 'add_project':
    $('#addProject').modal();
    break; 

    case 'edit_project':
    $('#editProj').modal();
    break;

    case 'add_skill':
    $('#addSkill').modal();
    break; 

    case 'edit_skill':
    $('#editSkl').modal();
    break;
    
    case 'add_interest':
    $('#addInterest').modal();
    break; 
  
  }
}


function changeSubmitType(modal_id, input_id){
  
  $(modal_id).on('show.bs.modal', function () {
    $(input_id).val('submit');
  }); 

  $(modal_id).on('hidden.bs.modal', function(){
    $(input_id).val('close');
    $(input_id).closest('form').submit();
  });

}

function showLessMore(more_id, less_id){

  $(more_id).click(function(){
    $(this).css('display', 'none');  
  });

  $(less_id).click(function(){
    $(more_id).css('display', 'inline');  
  });

}


jumpAndShowError($('#error_form').val(), $('#error').val());

changeSubmitType('#editInfo', '#edit_personal_info_submitType');
changeSubmitType('#addEducation', '#add_education_submitType');
changeSubmitType('#editEdu', '#edit_education_submitType');
changeSubmitType('#addAccomplishment', '#add_accomplishment_submitType');
changeSubmitType('#editAcomp', '#edit_accomplishment_submitType');
changeSubmitType('#addExperience', '#add_experience_submitType');
changeSubmitType('#editExp', '#edit_experience_submitType');
changeSubmitType('#addProject', '#add_project_submitType');
changeSubmitType('#editProj', '#edit_project_submitType');
changeSubmitType('#addSkill', '#add_skill_submitType');
changeSubmitType('#editSkl', '#edit_skill_submitType');
changeSubmitType('#addInterest', '#add_interest_submitType');

showLessMore('#edu_show_more', '#edu_show_less');
showLessMore('#acomp_show_more', '#acomp_show_less');
showLessMore('#exp_show_more', '#exp_show_less');
showLessMore('#proj_show_more', '#proj_show_less');
showLessMore('#skl_show_more', '#skl_show_less');
showLessMore('#int_show_more', '#int_show_less');

function addDelete(id)
{
    $(id).val('true');
}


$('.delete_interest').click(function(){
    $('#interest_id_field').val($(this).attr('data-id'))
    $('#edit_interest_form').submit();
});


$('#send_request_link').click(function(){

  $(this).closest('form').submit();
});

$('#cancel_request_link').click(function(){

  $(this).closest('form').submit();
});

$('#remove_friend_link').click(function(){

  $(this).closest('form').submit();
});

$('#approve_request_link').click(function(){

  $(this).closest('form').submit();
});


// function yearValidation(year){

//   if(!(/^\d{4}$/.test(year))){
//   	alert('Enter correct 4 digit numeric year');
//     return false;
//   }
  
//   if(parseInt(year) < 1950 || parseInt(year) > 2100){
//     alert('Enter a year between 1950 and 2100');
//     return false;
//   }

//   return true;
// }

function fromto(from, to){

  
  if(parseInt(from) > parseInt(to)){
    alert('From year should be less than to year');
    return false;
  }
  return true;
}

function emptyField(value){

  field = value.attr('name');
  value = value.val();
  if(value == ''){
  	alert(field + ' is empty');
    return false;
  }

  return true;
}


function validate_add_accomplishment(){
  return  emptyField($('#institute_acm'))
          && emptyField($('#title_acm'))
          &&yearValidation($('#year_acm').val())
}
function validate_edit_accomplishment(){
  return  emptyField($('#institute_acm_edit'))
          && emptyField($('#title_acm_edit'))
          &&yearValidation($('#year_acm_edit').val())
}

function validate_add_project(){
  return  emptyField($('#title_proj'))
          && emptyField($('#description_proj'))
}
function validate_edit_project(){
  return  emptyField($('#title_proj_edit'))
          && emptyField($('#description_proj_edit'))
}

function validate_add_education(){
  return  emptyField($('#institute_edu'))
          && emptyField($('#degree_edu'))
          && yearValidation($('#fromyear_edu').val())
          &&yearValidation($('#toyear_edu').val())
          &&fromto($('#fromyear_edu').val(), $('#toyear_edu').val())
}
function validate_edit_education(){
  return  emptyField($('#institute_edu_edit'))
          && emptyField($('#degree_edu_edit'))
          && yearValidation($('#fromyear_edu_edit').val())
          &&yearValidation($('#toyear_edu_edit').val())
          &&fromto($('#fromyear_edu_edit').val(), $('#toyear_edu_edit').val())
}

function validate_add_experience(){
  return  emptyField($('#title_exp'))
          && emptyField($('#company_exp'))
          && yearValidation($('#year_exp').val())
        
}
function validate_edit_experience(){
  return  emptyField($('#title_exp_edit'))
          && emptyField($('#company_exp_edit'))
          && yearValidation($('#year_exp_edit').val())
          
}
        
        
function validate_add_interest(){
  return  emptyField($('#interest_int'))
  
}

function validate_add_skill(){
  return  emptyField($('#title_skl'))
          && emptyField($('#description_skl'))
          
}
function validate_edit_skill(){
  return  emptyField($('#title_skl_edit'))
  && emptyField($('#description_skl_edit'))
  
}


