var slidenum = 0;
var slider = document.getElementById("slider");
var label = document.getElementById("dateLabel");
var dateArray = dates
var mapArray = maps
var tagArray = tags
var map = document.getElementById("map");
var timeline = [];
var transitioning = false;
var button = document.getElementById("transition");
var slideshow;
var title = document.getElementById("title");

function struct(date,map,tag){
    this.date = date;
    this.map = map;
    this.tag = tag;
}

function sortDate(a,b){
    return a.date - b.date;
}
var update = function(slide){
    //

    if(dateArray.length == 0){
	return;
    }
    else if(slide > dateArray.length - 1|| slide < 0){
	update(slidenum);
    }
    else{
	slidenum = slide;
	map.src = timeline[slidenum].map;
	if(isNaN(timeline[slidenum].date)){
	    label.innerHTML = "Input error, the date you put in was not a date";
	}
	else if(timeline[slidenum].date > 0){
	    label.innerHTML = timeline[slidenum].date + " C.E. - " + timeline[slidenum].tag;
	}
	else{
	    label.innerHTML = timeline[slidenum].date * -1 + " B.C.E. - " + timeline[slidenum].tag;
	}
    }
};

var transition = function(){
    if(slidenum == dateArray.length -1){
	slidenum = 0;
	update(slidenum);
    }
    else{
	slidenum ++;
	update(slidenum);
    }
    slider.value = slidenum;
};
//console.log(dates);
//console.log(maps);

window.addEventListener("load",function(){
    var i;
    for(i = 0; i < dateArray.length; i ++){
        //console.log(dateArray[i])
	dateArray[i] = parseInt(dateArray[i]);
	timeline.push(new struct(dateArray[i],mapArray[i],tagArray[i]));
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
button.addEventListener("click",function(){
    clearInterval(slideshow);
    transitioning = !transitioning;
    if(transitioning){
	button.value = "Autoplay: On";
    }
    else{
	button.value = "Autoplay: Off";
    }
    var changeMap = function(){
	if(transitioning){
	    if(slidenum != dateArray.length - 1){
		slidenum ++;
	    }
	    else{
		slidenum = 0;
	    }
	    slider.value = slidenum;
	    update(slidenum);
            speeds = document.getElementsByName("speed");
    //console.log(speeds);
    for(var i = 0; i < speeds.length; i++){
        if(speeds[i].checked){
            clearInterval(slideshow);
            slideshow=setInterval(changeMap,1000*speeds[i].value);
            //console.log(speeds[i].value);
        }
    }
	}
    }
    speeds = document.getElementsByName("speed");
    //console.log(speeds);
    for(var i = 0; i < speeds.length; i++){
        if(speeds[i].checked){
            clearInterval(slideshow);
            slideshow=setInterval(changeMap,1000*speeds[i].value);
            //console.log(speeds[i].value);
        }
    }
});

window.addEventListener("keydown",function(e){
    if(e.keyCode == 39 && slidenum != dateArray.length - 1){
	slidenum ++;
	update(slidenum);
    }
    else if(e.keyCode == 37 && slidenum != 0){
	slidenum --;
	update(slidenum);
    }
    slider.value = slidenum;
});
