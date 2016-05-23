var slidenum = 0;
var body = document.body;
var elements = document.body.innerHTML.split("/");
var dates = elements[0].split(" ");
var maps = elements[1].split(" ");
var map = document.getElementById("map");
var slider = document.getElementById("slider");
var label = document.getElementById("dateLabel");

var update = function(slide){
    slidenum = slide;
    map.src = maps[slidenum];
    label.innerHTML = dates[slidenum];
    body.innerHTML = label + label;
};

console.log(dates);
console.log(maps);
window.addEventListener("load",update(0));
slider.addEventListener("mousemove",update(slider.value));
slider.addEventListener("mouseup",update(slider.value));
slider.addEventListener("mousedown",update(slider.value));
