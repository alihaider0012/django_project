SearchWidget.prototype.getJumbotronhtml = function () {

    var html = '<div class="container">';
    html += '<div class="jumbotron bg-1 p-4">';
    html += '<div class="row">';
    html += '<div class="col-lg-12 mt-3 mb-1">';    
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

    html += '</select>';
    html += '</div>';
    html += '<div class="col-lg-12  mt-3 mb-1">';
    html += '<div class="input-group">';
    html += '<div class="input-group-prepend">';
    html += '<span class="btn bg-3 white"><i class="fas fa-search"></i><span>';
    html += '</div>';
    html += '<input type="text" class="form-control" id="';
    html += this.prefixId("queryString");
    html += '" onkeyup="filterData(\'';
    html += this.id;
    html += '\')">';
    html += '<div class="input-group-append">';
    html += '<button class="btn bg-3 white" type="submit" onclick="filterData(\'';
    html += this.id;
    html += '\')">Search</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<hr>';
    html += '</div>';

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
        html += '<div class="col-lg-6 col-md-4 col-sm-6">'
        html += '<div class="card mb-4 box-shadow mx-auto"  style="width:200px; height:350px; font-size: 15px;">';
        html += '<div class ="mb-3 widget_card_image">'
        html += '<img class="card-img-top mb-3 rounded-circle d-block mx-auto mt-3" src="';
        html += this.filteredData[i].img;
        html += '" alt="img" style="width:120px; height:120px; border: 1px solid black;">';
        html += '</div>';
        html += '<div class="card-body pt-0 mt-0">';
        html += '<div class="clearfix">';
        html += '<span class="font-weight-bold">';
        html += this.filteredData[i].title;
        html += '</span>';
        html += '<p class="small"><i>';
        html += this.filteredData[i].post;
        html += '</i></p>';
        html += '</div>';
        
        html += '<p class="small mb-0"><i class="fas fa-certificate mr-2 color-4"></i> ';
        html += this.filteredData[i].description;
        html += '</p>';
        html += '<p class="small mb-0"><i class="fa fa-envelope mr-2 color-4"></i>';
        html += this.filteredData[i].date;
        html += '</p>';
        html += '<p class="small"><i class="fas fa-location-arrow mr-2 color-4"></i> ';
        html += this.filteredData[i].location;
        html += '</p>';
        // html += '<span class="font-weight-bold"><i class="fas fa-microchip mr-2"></i>';
        // html += 'Interests';
        // html += '</span>';
        // html += '<div style="height:30px; overflow:hidden;">'
        // html += '<p class="small ml-4">';
        // html += this.filteredData[i].interests;
        // html += '</p>';
        // html += '</div>';
        html += '<a href="';
        html += this.filteredData[i].profile_url;
        html += '">';
        html += '<button style="margin-left:20%;" type="submit" class="btn bg-4 white btn-sm btn-outline-secondary">See Profile</button>';
        html += '</a>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
    }

    return html;
}


