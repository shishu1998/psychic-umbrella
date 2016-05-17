//picture is the link to the picture
function timeline(date,picture){
    this.date = date;
    //link to picture that is included in html later
    this.picture = picture;
};

//Used to create a new list for an empire
var NewList = function(name){
    window[name] = [];
};

var AddTimeline = function(empire,timeline){
    window[name].push(timeline);
};

var editTimeline = function(timeline,date,picture){
    timeline.date = date;
    if (!(typeof picture === "undefined")) {
	timeline.picture = picture;
    }
};
