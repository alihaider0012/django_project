var searchWidgetPool = new Array();
function SearchWidget(searchType, criteriaList, dataSource, id) {
    this.searchType = searchType;
    this.criteriaList = criteriaList;
    this.dataSource = dataSource;
    this.filteredData = dataSource;
    this.id = id;
    this.divId = "";
    searchWidgetPool[this.id] = this;
}
SearchWidget.prototype.prefixId = function (str) {
    return this.id + "_" + str;
}
SearchWidget.prototype.render = function (divId) {
    this.divId = divId;
    var html = this.getJumbotronhtml();
    html += this.getCardViewHtml();
    document.getElementById(divId).innerHTML = html;
}
SearchWidget.prototype.getJumbotronhtml = function () {
    var html = '<div class="container"><div class="jumbotron bg-1 p-4"><div class="row">';
    html += '<div class="col-lg-6 mt-3 mb-1">';    
    html += '<select id="';
    html += this.prefixId("criteria");
    html += '" class="custom-select">';
    html += '<option value="ignore" selected>Select Search Criteria</option>';
    for (var i in this.criteriaList) {
        html += '<option value="';
        html += i;
        html += '">';
        html += this.criteriaList[i];
        html += '</option>';
    }
    html += '</select></div><div class="col-lg-6  mt-3 mb-1"><div class="input-group">';
    html += '<div class="input-group-prepend">';
    html += '<span class="btn bg-3 white"><i class="fas fa-search"></i><span></div>';
    html += '<input type="text" class="form-control" id="';
    html += this.prefixId("queryString");
    html += '" onkeyup="filterData(\'';
    html += this.id;
    html += '\')">';
    html += '<div class="input-group-append">';
    html += '<button class="btn bg-3 white" type="submit" onclick="filterData(\'';
    html += this.id;
    html += '\')">Search</button>';
    html += '</div></div></div></div></div><hr></div>';
    return html
}
SearchWidget.prototype.getCardViewHtml = function () {
    var html = '<div class="container">';
    html += '<div class="row" id="';
    html += this.prefixId("cardRow");
    html += '">';
    html += this.getCardDetailsHtml();
    html += '</div>';
    html += '</div>';
    return html
}

SearchWidget.prototype.getCardDetailsHtml = function () {
    var html = "";
    for (var i = 0; i < this.filteredData.length; i++) {
        html += '<div class="col-lg-3 col-md-4 col-sm-6"><div class="card mb-4 box-shadow"><img class="card-img-top mb-0" src="'
        html += this.filteredData[i].img;
        html += '" alt="img" style="width:100%; height:200px">';
        html += '<hr class="mt-0 pt-0"><div class="card-body pt-0 mt-0"><div class="clearfix"><span class="font-weight-bold">';
        html += this.filteredData[i].title;
        html += '</span><p class="small"><i>';
        html += this.filteredData[i].post;
        html += '</i></p></div>';
        html += '<p class="small mb-0"><i class="fas fa-user-tie mr-2 color-4"></i> ';
        html += this.filteredData[i].employer;
        html += '</p>';
        html += '<p class="small mb-0"><i class="fas fa-certificate mr-2 color-4"></i> ';
        html += this.filteredData[i].description;
        html += '</p>';
        html += '<p class="small mb-0"><i class="fas fa-link mr-2 color-4"></i> ';
        html += this.filteredData[i].relevency;
        html += ' relevent</p><p class="small"><i class="fas fa-location-arrow mr-2 color-4"></i> ';
        html += this.filteredData[i].location;
        html += '</p><span class="font-weight-bold"><i class="fas fa-microchip mr-2"></i>Job Tags</span>';
        html += '<div style="height:50px; overflow:hidden;">'
        html += '<p class="small ml-4">';
        html += this.filteredData[i].tags;
        html += '</p></div>';
        html += '<button type="submit" style="width:70px;" onclick="getDetails(\''+ this.filteredData[i].job_url + '\')" class="btn bg-4 white btn-sm btn-outline-secondary">Details</button>';
        if(!this.filteredData[i].isMyJob) {
            if(this.filteredData[i].isRecruited == 'yes'){
                html += '<span class="badge bg-4 float-right mt-2 white">Hired</span>';
            }
            else{
                if(this.filteredData[i].hasApplied ==  'no') {
                    html += '<button type="submit" style="width:70px" onclick="submitApplyForm(\''+ this.filteredData[i].id + '\')" class="btn bg-1 color-4 btn-sm btn-outline-secondary ml-1">Apply</button>';       
                }
                else{
                    html += '<button type="submit" style="width:70px" onclick="submitCancelForm(\''+ this.filteredData[i].id + '\')" class="btn bg-1 color-4 btn-sm btn-outline-secondary ml-1">Cancel</button>';       
                }
            }
        }
        else{
            html += '<button type="submit" style="width:70px" onclick="submitDeleteForm(\''+ this.filteredData[i].id + '\')" class="btn btn-danger white btn-sm ml-1">Delete</button>';       
        }    
        html += '</div></div></div>';
    }
    return html;
}


function filterData(id){
    searchWidgetPool[id].performFiltering();
}
SearchWidget.prototype.performFiltering = function() {   
    var criteriaDropDown = document.getElementById(this.prefixId("criteria"));
    var searchInput = document.getElementById(this.prefixId("queryString"));
    var criteria = criteriaDropDown.value.toLowerCase();
    var queryString = searchInput.value.toLowerCase();
    if(queryString === ""){
        this.filteredData = new Array();
        for(var i = 0 ; i < this.dataSource.length; i++) {
            this.filteredData.push(this.dataSource[i]);
        }
        this.reRender(this.prefixId("cardRow"));
    }
    if(criteria == "ignore"){
        alert('Select an appropirate criteria');
        return;
    }
    else{
        this.filteredData = new Array();   
        for(var i = 0 ; i < this.dataSource.length; i++) {
            if(this.dataSource[i][criteria].toLowerCase().search(queryString) != -1){
                this.filteredData.push(this.dataSource[i]);
            }
        }
        this.filteredData.sort(function(a, b){
            var x = a["title"].toLowerCase();
            var y = b["title"].toLowerCase();
            if (x < y) {return -1;}
            if (x > y) {return 1;}
            return 0;
        });
        this.reRender(this.prefixId("cardRow"));
    }
}
SearchWidget.prototype.reRender = function (divId) {
    document.getElementById(divId).innerHTML = this.getCardDetailsHtml();
}