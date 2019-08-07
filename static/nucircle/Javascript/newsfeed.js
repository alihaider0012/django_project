function jumpAndShowError(error_form, error) {
  switch(error_form) {
      case 'add_post':  
      $('#newPost').modal();
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

changeSubmitType('#newPost', '#add_post_submitType');
jumpAndShowError($('#error_form').val(), $('#error').val());









var imageTypes = ['image/jpeg', 'image/pjpeg', 'image/png'];
var globalIdCount = 0;
var postCount = 0;
var postFlagArr = [];
var my_profile_pic;






// change order of suggestions column
if (window.innerWidth < 992) {

  var mainContent = document.getElementById("main-content");
  var classList = mainContent.getAttribute("class");
  classList += " order-12";
  mainContent.setAttribute("class", classList);

}


function updatePostModal(textid, id){
  $('#post_text').val($('#post-text-'+textid).text())
  $('#updatePostId').val(id)
  $('#newPost').modal('show')
  $('#updatePost').val('update')
}

$('#newPost').on('show.bs.modal', function(){
  $('#updatePost').val('')
})
function deletePost(id){
  swal({
    title: "Are you sure?",
    text: "This post and all its content will be deleted permanently!",
    type: "warning",
    showCancelButton: true,
    confirmButtonClass: "btn-danger",
    confirmButtonText: "Yes, delete it!",
    closeOnConfirm: false
    },
    function(){
      $('#post_id_del').val(id)
      $('#delete_post').submit()
    }
  );
}


// get div html
function getDivHtml(userid,username, title, profile_image, image, text, id, isMyPost,isMyLike,likes_count,comments_count) {
  var postDivContent = '<div class="card-header pl-1 pb-0 bg-white border-0 mb-0">'
  + '<a href="/profile/'+userid+'"><img id="post-profile-img-' + globalIdCount + '" src="' + profile_image + '" alt="profile image" class="mr-3 rounded-circle float-left">'
  
  + '<h6><span id="post-user-name-' + globalIdCount + '" class="font-weight-bold">' + username + ' </span><small><i id="post-date-' + globalIdCount + '">' + '</i></small></h6>'
  + '<h6><small><i id="post-user-title-' + globalIdCount + '">' + title + '</i></small></h6></a>'
  if(isMyPost){      
    postDivContent += '<button class="btn btn-dark small float-right" onclick="updatePostModal('+globalIdCount+', '+id+')">Update</button>'
    postDivContent += '<button class="btn btn-danger small float-right mr-2 " onclick="deletePost('+id+')">Delete</button>'
  }
  postDivContent += '</div>'
  + '<div class="card-body pb-0 mb-0 pl-1 pr-1 pt-2">'
  + '<p id="post-text-' + globalIdCount + '" class="mt-0 post-body">' + text + '</p>'
  + '<img id="post-img-' + globalIdCount + '"  src="' + image + '" class="mb-0 img-fluid rounded">'
  + '<hr>'
    + '<div class="card-footer pb-0 mb-0 mt-0 border-0 pt-1 mt-0 pl-0">';
    if(isMyLike){
      postDivContent+= '<button style="cursor:pointer;" class="likeComment small"  onclick="toggleLike('+id+',this)"><i class="fas fa-thumbs-up"></i> Liked <span class="badge badge-dark">'+likes_count+'</span></button>';
    }
    else{
      postDivContent+= '<button  style="cursor:pointer;" class="likeComment small"  onclick="toggleLike('+id+',this)"><i class="far fa-thumbs-up"></i> Like <span class="badge badge-dark">'+likes_count+'</span></button>';
    }
    
    postDivContent+= '<button style="cursor:pointer;" class="likeComment small" onclick="onClickComment('+id+',this,'+postCount+')" data-toggle="collapse" data-target="#demo-' + postCount + '"><i class="far fa-comment-alt"></i> Comment <span id="comment-count-'+id+'" class="badge badge-dark">'+comments_count+'</span></button>'
    // + '<button class="likeComment small"><i class="fas fa-share"></i> Share</button>'
    + '<div id="demo-' + postCount + '" class="collapse mt-3">'
    + '<div id="comment-section-'+id+'"></div>'
    // + '<form action="#">'
    + '<div class="form-group mb-2 ml-4">'
    + '<div class="input-group">'
    + '<div class="input-group-prepend">'
    + '<span class="input-group-text" style="padding: 0"><img id="comment-profile-img-' + globalIdCount + '" src="'+my_profile_pic+'" width="40px" height="35px"></span>'
    + '</div>'
    + '<textarea id="comment-text-' + id + '" type="text" class="form-control" placeholder="Add a comment..." name="comment" rows="1"></textarea>'
    + '</div>'
    + '</div>'
    + '<button onclick="onSubmitCommentClick('+id+')" class="btnPostComment mb-2 ml-4"><small>Post</small></button>'
    // + '</form>'
    + '</div>'
    + '</div>'
    + '</div>';

  return postDivContent;
}

// functions for detecting end of page
function getDocHeight() {
  var D = document;
  return Math.max(
    D.body.scrollHeight, D.documentElement.scrollHeight,
    D.body.offsetHeight, D.documentElement.offsetHeight,
    D.body.clientHeight, D.documentElement.clientHeight
  );
}
// $(window).scroll(function () {
//   if ($(window).scrollTop() + $(window).height() == getDocHeight()) {
//     //populateNewsFeed();
//   }
// });





$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
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


function validate_add_post(){
  var file = document.getElementById('customFile')

  if(file.files.length == 0)
  {
    alert('select image');
    return false;
  }

  return  emptyField($('#post_text'))
        
}

var getPostUrl = null;
var index = 0;
// console.log("{{user.userprofile.profile_image.url}}");

function getDetails(){

  if(getPostUrl == null){
    return;
  }
  
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
          
          index += 5;
          var data = JSON.parse(this.responseText);
          flag = data['flag'];
          my_profile_pic = data['pp'];
          // console.log(flag);
          var mainContent = document.getElementById('main-content');
          for (var i = 0; i < data['posts'].length; i++) {
            post = data['posts'][i];  
            var div = document.createElement('div');
            div.setAttribute("class", "card p-2 mb-3 shadow");
            div.innerHTML = getDivHtml(post.userid,post.username, post.title, post.profile_image, post.image, post.text, post.id, post.isMyPost,post.isMyLike,post.likes_count,post.comments_count);
            mainContent.appendChild(div);
            globalIdCount++;
            postCount++;
            postFlagArr.push(false);
          
          }
          
      }
  };
  xmlhttp.open("GET", getPostUrl + '?index=' + index, true);
  xmlhttp.send();
}


// populate newsfeed
var populateNewsFeed = function (url = null) {

  if(getPostUrl == null){
    getPostUrl = url;
  }
  getDetails();
 
}

var current_posts = 3;
var flag = null;
// console.log(flag);


$(window).scroll(function() {
  // console.log($(window).scrollTop() + $(window).height() + 1 >= $(document).height());
  if($(window).scrollTop() + $(window).height() == $(document).height() || $(window).scrollTop() + $(window).height() + 1 >= $(document).height()) {
    if(flag){
      current_posts+=3;  
      $.ajax({
        url: "/get_post_ajax/",
        method:"POST",
        data:{"count":current_posts,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()},
        success: function(data){
          // console.log('in');
          flag = data.flag;

          var mainContent = document.getElementById('main-content');
          
          for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];  
            var div = document.createElement('div');
            div.setAttribute("class", "card p-2 mb-3 shadow");
            div.innerHTML = getDivHtml(post.userid,post.username, post.title, post.profile_image, post.image, post.text, post.id, post.isMyPost,post.isMyLike,post.likes_count,post.comments_count);
            mainContent.appendChild(div);
            globalIdCount++;
            postCount++;
            postFlagArr.push(false);
          }
        },
        error: function(errorData){
          console.log(errorData);
        }
      })
    }
  }
});


function toggleLike(id,btn){
  console.log(id);
  $.ajax({
    url:"/like_dislike_post/",
    method:'post',
    data:{'postid':id,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}
    ,
    success: function(data){
      var spaneletext = parseInt(btn.lastElementChild.innerHTML);
      // console.log(spanele);

      if(data.flag=='true'){
        spaneletext++;
        btn.innerHTML = '<i class="fas fa-thumbs-up"></i> Liked <span class="badge badge-dark">'+spaneletext+'</span>';
      }
      else{
        spaneletext--;
        btn.innerHTML = '<i class="far fa-thumbs-up"></i> Like <span class="badge badge-dark">'+spaneletext+'</span>'
      }
    },
    error: function(errorData){
        console.log(errorData);
    }
  })
}


function onClickComment(id,btn,postC){
  if(postFlagArr[postC]==false){
    postFlagArr[postC] = true;
    console.log('in comment ajax');
    $.ajax({
      url:"/get_comments_post/",
      method:'post',
      data:{'postid':id,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}
      ,
      success: function(data){
        console.log(data);
        var comments = data.comments;
        for(var i = 0; i < comments.length ; i++){
          create_one_comment(comments[i],id);
        }
      },
      error: function(errorData){
          console.log(errorData);
      }
    })
  }
}


function create_one_comment(comment,postid){
  var elemain = document.getElementById('comment-section-'+postid);
  var toAdd = document.createElement('div');
  toAdd.id = 'comment-'+comment.commentid;
  toAdd.classList.add('row');
  toAdd.style.marginBottom = '10px';
  var html = '<div class="col-sm-1">'
  +'<div class="thumbnail">'
  +'<img class="img-responsive user-photo" width="40px" height="35px" src="'+comment.profile_pic+'">'
  +'</div>'
  +'</div>'
  
  +'<div class="col-sm-11">'
  +'<div class="panel panel-default">'
  +'<div class="panel-heading">'
  +'<strong>'+comment.username+'</strong>';
  if(comment.isAuthor){
    html+='<button class="btn btn-danger btn-sm" style="float:right;margin-left:5px;" onclick="onClickDeleteComment('+comment.commentid+','+postid+')"><i class="fa fa-trash" aria-hidden="true"></i></button>'
    +'<button class="btn btn-secondary btn-sm" style="float:right;" onclick="onClickEditComment('+comment.commentid+')"><i class="fa fa-pen" aria-hidden="true"></i></button>';
  }
  html+='</div>'
  +'<pre style="white-space: pre-wrap;font-family: calibri;" class="panel-body">'
  +comment.text
  +'</pre><!-- /panel-body -->'
  +'<hr></div>'
  +'</div>'
  toAdd.innerHTML = html;

  elemain.appendChild(toAdd);
}


function onSubmitCommentClick(postid){
  var text = document.getElementById('comment-text-'+postid).value;
  // console.log(text);

  if (text!=''){
    //ajax
    $.ajax({
      url:"/submit_comments_post/",
      method:'post',
      data:{'postid':postid,'text':text,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}
      ,
      success: function(data){
        console.log(data);
        var comment = data.comment;
        create_one_comment(comment,postid);
        var count = parseInt(document.getElementById('comment-count-'+postid).textContent);
        count++;
        document.getElementById('comment-count-'+postid).textContent = count;
        document.getElementById('comment-text-'+postid).value = '';
      },
      error: function(errorData){
        console.log(errorData);
      }
    })
  }
}


function onClickDeleteComment(commentid,postid){
  swal({
    title: "Are you sure?",
    text: "This comment will be deleted permanently!",
    type: "warning",
    showCancelButton: true,
    confirmButtonClass: "btn-danger",
    confirmButtonText: "Yes, delete it!",
    closeOnConfirm: false
    },
    function(){
      $.ajax({
        url:"/delete_comment_from_post/",
        method:'post',
        data:{'id':commentid,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}
        ,
        success: function(data){
          console.log(data);
          swal('Comment deleted successfully!','','success');
          document.getElementById('comment-'+commentid).remove();
          var count = parseInt(document.getElementById('comment-count-'+postid).textContent);
          count--;
          document.getElementById('comment-count-'+postid).textContent = count;
        },
        error: function(errorData){
          console.log(errorData);
        }
      })
    }
  );
}

function onClickEditComment(commentid){
  document.getElementById('Edit_comment_id').textContent = commentid;
  document.getElementById('Edit_comment_text').value = document.getElementById('comment-'+commentid).getElementsByTagName('pre')[0].innerHTML;
  $('#Edit_comment').modal('show');
}

function onSubmitEditComment(){
  var commentid = document.getElementById('Edit_comment_id').textContent;
  var text = document.getElementById('Edit_comment_text').value;

  if(text!=''){
    $.ajax({
      url:"/edit_comment_from_post/",
      method:'post',
      data:{'commentid':commentid,'text':text,csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()}
      ,
      success: function(data){
        console.log(data);
        // $('#Edit_comment').modal('close');
        document.getElementById('comment-'+commentid).getElementsByTagName('pre')[0].innerHTML = text;
      },
      error: function(errorData){
        console.log(errorData);
      }
    })
  }
}