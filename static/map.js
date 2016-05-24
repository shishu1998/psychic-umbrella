var slidenum = 0;
var slider = document.getElementById("slider");
var label = document.getElementById("dateLabel");
var dateArray = dates.split(" ");
var mapArray = maps.split(" ");
var map = document.getElementById("map");

var update = function(slide){
    //
    if(slide > dateArray.length - 2 || slide < 0){
	update(slidenum);
    }
    else{
	slidenum = slide;
	map.src = mapArray[slidenum];
	label.innerHTML = dateArray[slidenum];
    }
};

//console.log(dates);
//console.log(maps);

window.addEventListener("load",function(){
    slider.max = dateArray.length-2;
    update(slider.value);
});

slider.addEventListener("mousedown",update(slider.value));
slider.addEventListener("mousemove",update(slider.value));
slider.addEventListener("mouseup",update(slider.value));
