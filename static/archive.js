var links = document.getElementsByClassName("date")
var pic = document.getElementById("pic")
for(var i = 0; i < links.length; i ++){
	console.log(links[i].innerHTML)
	links[i].addEventListener("mouseover", function(e){
		pic.src = dates[this.innerHTML];
		console.log(pic.src);
		console.log("works");
	});
}