var slidenum = 0;
var slider = document.getElementById("slider");
var label = document.getElementById("dateLabel");
var dateArray = dates.split(" ");
var mapArray = maps.split(" ");
var map = document.getElementById("map");
var timeline = [];

function struct(date,map){
    this.date = date;
    this.map = map;
}

function sortDate(a,b){
    return a.date - b.date;
}
var update = function(slide){
    //
    if(slide > dateArray.length - 1|| slide < 0){
	update(slidenum);
    }
    else{
	slidenum = slide;
	map.src = timeline[slidenum].map;
	label.innerHTML = timeline[slidenum].date;
    }
};

//console.log(dates);
//console.log(maps);

window.addEventListener("load",function(){
    dateArray.pop();
    var i;
    for(i = 0; i < dateArray.length; i ++){
	dateArray[i] = parseInt(dateArray[i]);
	timeline.push(new struct(dateArray[i],mapArray[i]));
    }
    timeline.sort(sortDate);
    slider.max = dateArray.length-1;
    slider.value = 0;
    update(slider.value);
    //console.log("works0");
});

slider.addEventListener("mousedown", function(){
    update(slider.value);
    //console.log("works1");
});
slider.addEventListener("mousemove", function(){
    update(slider.value);
    //console.log("works2");
});
slider.addEventListener("mouseup", function(){
    update(slider.value);
    //console.log("works3");
});
