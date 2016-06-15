var links = document.getElementsByClassName("date")
var pic = document.getElementById("pic")
for(var i = 0; i < links.length; i ++){
	links[i].addEventListener("mouseover", function(e){
		for(j = 0; j < dates.length; j++)
			if(dates[j]['date']==this.innerHTML)
				pic.src = dates[j]['image'];
	});
}