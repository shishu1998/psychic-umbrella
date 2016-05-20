var date = document.getElementById("date");
var map = document.getElementById("map");
var update = function(slidenum){
    date.innerHTML = data[slidenum];
    map.src = data[slidenum];
};

