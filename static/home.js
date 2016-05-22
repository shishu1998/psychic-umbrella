//dict of continents, will connect them with mongodb

Conts = {};
Conts["AF"]=["Libya","Kenya","South Africa"];
Conts["AS"]=["China","Korea","Japan","Vietnam"];
Conts["EU"]=["Britain","France","Germany"];
Conts["NA"]=["United States","Canada","Mexico","a","b","c","d","e","a","b","c","d","e","a","b","c","d","e"];
Conts["OC"]=["Australia","Philippines"];
Conts["SA"]=["Maya","Inca","Brazil"];

var popup = document.getElementById("container");
var currCont = null;
d3.selectAll("g").on("click", function() {
    var newCont = this;
    if(currCont == newCont){
	popup.innerHTML="";
	currCont = null;
    popup.style.pointerEvents="none";
    }
    else{
	currCont = newCont;
	createPop(currCont.className.baseVal);
    }
});


//creates the popup screen when a continent is clicked
var container = d3.select("#container");
function createPop(c){
    //resets container
    popup.innerHTML = "";

    //set up return button
    container.append("div")
    .attr("class","empReturn")
    .append("label")
    .attr("class","unselectable")
    .text("Return");
    d3.select(".empReturn").on("click", function(){
    popup.innerHTML="";
    currCont = null;
    container.style("pointer-events","none");
    });

    //set up empire list
    var empires = container.selectAll("a")
    .data(Conts[c]).enter()
    .append("a")
    .attr("href",function(d){return "/map/" + d;})
    .style("color","inherit")
    .append("div")
    .attr("class","empSelect")
    .append("label")
    .attr("class","unselectable")
    .text(function(d){return d;});
    container.style("pointer-events","auto");

}
