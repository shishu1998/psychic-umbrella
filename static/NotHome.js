/*var slidenum = 0;
var body = document.body;
var elements = document.body.innerHTML.split("/");

var dates = elements[0].split(" ");
var maps = elements[1].split(" ");

var update = function(slide){
    slidenum = slide;
    body.innerHTML = maps[slidenum] + "<br>" + dates[slidenum];
};

console.log(dates);
console.log(maps);
window.addEventListener("load",update(0));
*/
var slider = document.getElementById("slider");

var UDS = function updateSlider(val) {//changes label on slider
	var date = document.getElementById("dateLabel");
	var empire = document.getElementById("empireLabel");
	var map = document.getElementById("map");
	if(val < 200){
		date.innerHTML = "3,500 - 1,500 B.C.";
		empire.innerHTML = "Neolithic China";
		map.src = "http://data.chinahighlights.com/image/map/ancient/neolithic-map-china1.gif";
	}
	else if(val < 400){
		date.innerHTML = "1,766 - 1,122 B.C.";
		empire.innerHTML = "Shang Dynasty";
		map.src = "http://www.chinahighlights.com/image/map/ancient/shang-dynasty-map1.gif";
	}
	else if(val < 600){
		date.innerHTML = "1,122 - 771 B.C.";
		empire.innerHTML = "Eastern Zhou Dynasty";
		map.src = "http://www.chinahighlights.com/image/map/ancient/map-western-zhou-dynasty-fu.gif";
	}
	else if(val < 800){
		date.innerHTML = "770 - 256 B.C.";
		empire.innerHTML = "Western Zhou Dynasty";
		map.src = "http://www.chinahighlights.com/image/map/ancient/eastern-zhou-dynasty-map1.gif";
	}
	else{
		date.innerHTML = "221 - 207 B.C.";
		empire.innerHTML = "Qin Dynasty";
		map.src = "http://www.chinahighlights.com/image/map/ancient/qin-dynasty-map1.gif";
	}
}

slider.addEventListener('mouseup',function(){
	UDS(slider.value);
})
slider.addEventListener('mousedown',function(){
	UDS(slider.value);
})
slider.addEventListener('mousemove',function(){
	UDS(slider.value);
})
UDS(slider.value);