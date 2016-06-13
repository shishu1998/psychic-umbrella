var popup = document.getElementById("popup");
var selected = false;
d3.select("#empires").on("click",function(){
	if(selected){
		popup.innerHTML="";
		selected = false;
	}
	else{
		selected = true;
		createPop();
	}
})
var container = d3.select("#popup")
function createPop(){
	popup.innerHTML="";
	console.log("WORKS");
	    //set up return button
    container.append("div")
    .attr("class","empReturn")
    .append("label")
    .attr("class","unselectable")
    .text("Return");
    d3.select(".empReturn").on("click", function(){
    popup.innerHTML="";
    selected = false;
    container.style("pointer-events","none");
    });

    var emps = container.selectAll("a").data(empires).enter()
    emps.append("a")
    .attr("href",function(d){return "/map/" + d;})
    .style("color","inherit")
    .append("div")
    .attr("class","empSelect")
    .append("label")
    .attr("class","unselectable")
    .text(function(d){return d;});
    container.style("pointer-events","auto");

    if(empires.length<15){
        container.style("height",45+26*empires.length+"px");
        container.style("overflow","hidden");
    }
    else
        container.style("height",45+26*15+"px");
}