//picture is the link to the picture
function timeline(date,picture){
    this.date = date;
    //link to picture that is included in html later
    this.picture = picture;
};

//Used to create a new list for an empire
var NewList = function(empire){
    window[empire] = [];
};

var AddTimeline = function(empire,timeline){
    window[empire].push(timeline);
};

//date is required everytime for modification
var editTimeline = function(timeline,date,picture){
    if(typeof date === "undefined"){
	return;
    }
    timeline.date = date;
    //picture is optional parameter
    if (!(typeof picture === "undefined")) {
	timeline.picture = picture;
    }
};
