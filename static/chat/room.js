console.log("in room.js");
// var imported = document.createElement('script');
// imported.src = "../reconnecting-websocket.js";
// document.head.appendChild(imported);

// var currentChatID = {{room_name_json}};

//     var roomName = {{ room_name_json }};
//     var username = {{ username }};
//     var chatSocket = null;

//     initializeChat();


   


//     function refreshSocketConnection(id){
//         disconnectSocket();
//         socketConnection(id);      
//     }

//     function socketConnection(room){
      
//       chatSocket = new ReconnectingWebSocket(
//         'ws://' + window.location.host +
//         '/ws/chat/' + room + '/');
//       chatSocket.onopen = function(e) {
//         fetchMessages(messageCount);
        
//       }
//       chatSocket.onmessage = function(e) {
//           var data = JSON.parse(e.data);
//           if (data['command'] === 'messages') {
//             console.log(data['flagForVisibility']);
//             if(data['flagForVisibility']==true){
//               document.getElementById('reloadmessages').style.visibility = 'hidden';
//             }
//             else{document.getElementById('reloadmessages').style.visibility = 'visible';}
//             for (let i=0; i<data['messages'].length; i++) {
//               createMessage(data['messages'][i]);
//             }
//           } else if (data['command'] === 'new_message'){
//             createMessage(data['message']);
//           }
//       };
//       chatSocket.onclose = function(e) {
//           console.error('Chat socket closed successfully');
//           document.getElementById("reloadmessages").removeEventListener("click", reloadmsgs);
//       };
//       document.querySelector('#chat-message-input').onkeyup = function(e) {
//           if (e.keyCode === 13) {  // enter, return
//               document.querySelector('#chat-message-submit').click();
//           }
//       };
//       document.querySelector('#chat-message-submit').onclick = function(e) {
//           var messageInputDom = document.getElementById('chat-message-input');
//           var message = messageInputDom.value;
//           chatSocket.send(JSON.stringify({
//               'command': 'new_message',
//               'message': message,
//               'from': username,
//               'chatID':currentChatID
//           }));
//           messageInputDom.value = '';
//       };
      
//       var messageCount = 10;

      
//       document.getElementById("reloadmessages").addEventListener("click", reloadmsgs);

//       function reloadmsgs(){
//         $('.sent').remove();
//         $('.replies').remove();
//         messageCount+=10;
//         console.log("in for "+ room);
//         fetchMessages(messageCount);
//       }

//       function fetchMessages(messageCount) {
//         chatSocket.send(JSON.stringify({'command': 'fetch_messages', 'chatID':currentChatID,'messageCount':messageCount}));
//       }
//     }

//     function disconnectSocket(){
//       chatSocket.close();
//     }

//     function createMessage(data) {
//       var author = data['author'];
//       var msgListTag = document.createElement('li');
//       // msgListTag.className = 'animated jello';
//       var msgListTag1 = document.createElement('li');
//       // var imgTag = document.createElement('img');
//       var pTag = document.createElement('p');
//       var timestamp = document.createElement('small');
//       linebreak = document.createElement("br");
//       pTag.textContent = data.content;
//       // imgTag.src = "user.userprofile.profile_image.url";
//       timestamp.textContent = this.renderTimestamp(data['timestamp'])
//       if (author === username) {
//         msgListTag.className = 'replies';
//       } else {
//         msgListTag.className = 'sent';
//         var nameauthor = document.createElement('strong');
//         nameauthor.textContent = author;
//         msgListTag1.appendChild(nameauthor);
//         msgListTag1.appendChild(linebreak);
//       }
//       // msgListTag.appendChild(imgTag);
//       msgListTag.appendChild(msgListTag1);
//       msgListTag.appendChild(pTag);
      
//       pTag.appendChild(linebreak);
//       pTag.appendChild(timestamp);
//       document.querySelector('#chat-log').appendChild(msgListTag);
//       msgListTag.scrollIntoView();
//     }

//     //TIMESTAMP
//     renderTimestamp = timestamp => {
//     let prefix = "";
//     const timeDiff = Math.round(
//       (new Date().getTime() - new Date(timestamp).getTime()) / 60000
//     );
//     if (timeDiff < 1) {
//       // less than one minute ago
//       prefix = "just now...";
//     } else if (timeDiff < 60 && timeDiff > 1) {
//       // less than sixty minutes ago
//       prefix = `${timeDiff} minutes ago`;
//     } else if (timeDiff < 24 * 60 && timeDiff > 60) {
//       // less than 24 hours ago
//       prefix = `${Math.round(timeDiff / 60)} hours ago`;
//     } else if (timeDiff < 31 * 24 * 60 && timeDiff > 24 * 60) {
//       // less than 7 days ago
//       prefix = `${Math.round(timeDiff / (60 * 24))} days ago`;
//     } else {
//       prefix = `${new Date(timestamp)}`;
//     }
//     return prefix;
//   };


//   function onChatClick(chatid,chatTitle,pic){
//     var name = document.getElementById("chatname");
//     var img = document.getElementById("chatimg");
//     makeInvisible(false);

//     $('.sent').remove();
//     $('.replies').remove();


//     // var el = document.getElementById('reloadmessages');
//     // el.onclick = null;

//     currentChatID = chatid;
//     name.textContent = chatTitle;
//     img.src = pic;
//     refreshSocketConnection(chatid);
//     window.history.pushState({}, "Title", "/chat/"+chatid+"/");
//   };


//   function initializeChat(){
//       var flag = {{currentChatFlag}};
//       if(flag == true){
//         makeInvisible(false);
//         socketConnection(roomName);
//         var err = {{errors}};
//         if (err.length>0)
//           AppearDialogBox(flag);
//         window.history.pushState({}, "Title", "/chat/"+roomName+"/");
//       }
//       else{
//         socketConnection(roomName);
//         disconnectSocket();
//         //makeInvisible(true);
//         var f1 = {{isFrontPage}};
//         if(f1 == false)
//           AppearDialogBox();
//       }  
//     }

//   function AppearDialogBox(flag){
    
//         // Get the modal
//         var modal = document.getElementById("myModal");

//         // Get the button that opens the modal
//         var btn = document.getElementById("myBtn");

//         // Get the <span> element that closes the modal
//         var span = document.getElementsByClassName("close1")[0];

//         if(flag==true){
//           var errors = {{errors}};
//           document.getElementById("initialmessage").textContent=errors+" are not found!";
//         }

//         modal.style.display = "block";

//         // When the user clicks on <span> (x), close the modal
//         span.onclick = function() {
//           modal.style.display = "none";
//         }

//         // When the user clicks anywhere outside of the modal, close it
//         window.onclick = function(event) {
//           if (event.target == modal) {
//             modal.style.display = "none";
//           }
//         }
//   }  


//   function makeInvisible(flag) {
//     var x = document.getElementById('makeinvisible');
//     if (flag==true) {
//       x.style.visibility = 'hidden';
//     } else {
//       x.style.visibility = 'visible';
//     }
//   }



//   $("#profile-img").click(function() {
//     $("#status-options").toggleClass("active");
//   });

//   $(".expand-button").click(function() {
//     $("#profile").toggleClass("expanded");
//     $("#contacts").toggleClass("expanded");
//   });

//   $("#status-options ul li").click(function() {
//     $("#profile-img").removeClass();
//     $("#status-online").removeClass("active");
//     $("#status-away").removeClass("active");
//     $("#status-busy").removeClass("active");
//     $("#status-offline").removeClass("active");
//     $(this).addClass("active");
    
//     if($("#status-online").hasClass("active")) {
//       $("#profile-img").addClass("online");
//     } else if ($("#status-away").hasClass("active")) {
//       $("#profile-img").addClass("away");
//     } else if ($("#status-busy").hasClass("active")) {
//       $("#profile-img").addClass("busy");
//     } else if ($("#status-offline").hasClass("active")) {
//       $("#profile-img").addClass("offline");
//     } else {
//       $("#profile-img").removeClass();
//     };
    
//     $("#status-options").removeClass("active");
//   });

//   $('#settingBtn').hover(
//        function(){ $(this).addClass('fa-spin') },
//        function(){ $(this).removeClass('fa-spin') }
// )