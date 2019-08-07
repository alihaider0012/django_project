var dataSource = new Array();


function getData(profile_url, profile_image, username, location, title, discipline, graduation_date){

    dataSource.push({

                    profile_url: profile_url,
                    img: profile_image,
                    title: username,
                    location: location,
                    post: title,
                    description: discipline,
                    date: graduation_date,
                   
                });        
           
}  


function showResults(){

    var searchType = "friend";
    var criteriaList = { title: "Username", location: "Location", date: "Email", description:"Name"};
    var resultSearch = new SearchWidget(searchType, criteriaList, dataSource, "resultSearch");
    resultSearch.render('resultsDiv');
    
    
}

