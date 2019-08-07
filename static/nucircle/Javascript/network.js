

var dataSource1 = [
    {
        img: "Images/u1.jpg",
        title: "User 1 abc",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u2.jpg",
        title: "User 2 xyz",
        location: "Karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u3.jpg",
        title: "User 3 abc",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u4.jpg",
        title: "User 4 abc",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u5.jpg",
        title: "User 5 xyz",
        location: "karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u6.jpg",
        title: "User 6 cd",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u7.jpg",
        title: "User 7 yz",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    }

];


var dataSource2 = [
    {
        img: "Images/u1.jpg",
        title: "User 1 abc pend",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u2.jpg",
        title: "User 2 xyz pend",
        location: "Karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u3.jpg",
        title: "User 3 abc pend",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u4.jpg",
        title: "User 4 abc pend",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u5.jpg",
        title: "User 5 xyz pend",
        location: "karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u6.jpg",
        title: "User 6 cd pend",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u7.jpg",
        title: "User 7 yz pend",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    }

];


var dataSource3 = [
    {
        img: "Images/u1.jpg",
        title: "User 1 abc sug",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u2.jpg",
        title: "User 2 xyz sug",
        location: "Karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u3.jpg",
        title: "User 3 abc sug",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u4.jpg",
        title: "User 4 abc sug",
        location: "Lahore",
        post: "Web dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u5.jpg",
        title: "User 5 xyz sug",
        location: "karachi",
        post: "soft dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u6.jpg",
        title: "User 6 cd sug",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    },
    {
        img: "Images/u7.jpg",
        title: "User 7 yz sug",
        location: "Islamabad",
        post: "android dev",
        description: "This is a sample description. You can see all your friends here. This is a very good feature.",
        date: "March 5, 2019"
    }

];


// var networkSearch = new SearchWidget(searchType, criteriaList, dataSource1, "networkSearch");
// networkSearch.render('networkDiv');


// var pendingSearch = new SearchWidget(searchType, criteriaList, dataSource2, "pendingSearch");
// pendingSearch.render('pendingDiv');

// var suggestionSearch = new SearchWidget(searchType, criteriaList, dataSource3, "suggestionSearch");
// suggestionSearch.render('suggestionDiv');


$("#pendingDiv").css("display", "none");

$("#suggestionDiv").css("display", "none");


$("#pendLink").click(function(){
  if($("#pendingDiv").css("display") === "none"){
   
    $("#suggestionDiv").css("display", "none");
    $("#networkDiv").css("display", "none");
      
    $("#pendingDiv").css("display", "block");
    $("#heading").text("Followers");
}
});

$("#sugLink").click(function(){
    if($("#suggestionDiv").css("display") === "none"){
        $("#pendingDiv").css("display", "none");
    $("#networkDiv").css("display", "none");
      
    $("#suggestionDiv").css("display", "block");
    $("#heading").text("Recommended for you");
  }
});

$("#netLink").click(function(){
    if($("#networkDiv").css("display") === "none"){
        $("#pendingDiv").css("display", "none");
    $("#suggestionDiv").css("display", "none");
      
    $("#networkDiv").css("display", "block");
    $("#heading").text("Following");
  }
});

var friends = new Array();
var pending_requests = new Array();

function getFriendData(profile_url, profile_image, username, location, title, discipline, graduation_date, interests){

    friends.push({

                    profile_url: profile_url,
                    img: profile_image,
                    title: username,
                    location: location,
                    post: title,
                    description: discipline,
                    date: graduation_date,
                    interests: interests
                   
                });        
           
}  




function getPendingRequestData(profile_url, profile_image, username, location, title, discipline, graduation_date, interests){

    pending_requests.push({

                    profile_url: profile_url,
                    img: profile_image,
                    title: username,
                    location: location,
                    post: title,
                    description: discipline,
                    date: graduation_date,
                    interests: interests
                   
                });        
           
} 


function showResults(){

    var searchType = "friend";
    var criteriaList = { title: "Username", location: "Location", date: "Email", description:"Name"};
    
    var networkSearch = new SearchWidget(searchType, criteriaList, friends, "networkSearch");
    networkSearch.render('networkDiv');

    var pendingSearch = new SearchWidget(searchType, criteriaList, pending_requests, "pendingSearch");
    pendingSearch.render('pendingDiv');

}

