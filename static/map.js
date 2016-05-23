var slidenum = 0;
var h2 = document.getElementsByTagName("h2")[0].innerHTML;
var slider = document.getElementById("slider");
var label = document.getElementById("dateLabel");
var elements = h2.split(";");
var dates = elements[0].split(" ");
var maps = elements[1].split(" ");
var map = document.getElementById("map");

var update = function(slide){
    slidenum = slide;
    map.src = maps[slidenum];
    label.innerHTML = dates[slidenum];
};

console.log(dates);
console.log(maps);
window.addEventListener("load",update(0));
slider.addEventListener("mousemove",update(slider.value));
slider.addEventListener("mouseup",update(slider.value));
slider.addEventListener("mousedown",update(slider.value));
