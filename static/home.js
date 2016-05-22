//dict of continents, will connect them with mongodb

Conts = {};
Conts["AF"]=[];
Conts["AS"]=[];
Conts["EU"]=[];
Conts["NA"]=[];
Conts["OC"]=[];
Conts["SA"]=[];

var popup = document.getElementById("container");
var currCont = null;
d3.selectAll("g").on("click", function() {
    var newCont = this;
    console.log(this);
    if(currCont == newCont){
	container.innerHTML="";
	currCont = null;
    }
    else{
	currCont = newCont;
	createPop(currCont.className);
    }
});

//creates the popup screen when a continent is clicked
function createPop(c){
    popup.innerHTML = "";
}


