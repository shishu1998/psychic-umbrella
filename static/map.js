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
