function page_url(page_num){
	var final_location = "";
	var wlh = window.location.href;
	console.log("WLH = "+wlh);
	if (wlh.includes("/page=")){
		console.log("'/page= ' in "+wlh)
		var page_location = wlh.indexOf("/page=");
		if (page_location == wlh.lastIndexOf("/")){
			final_location = wlh.substring(0,page_location);
			final_location += "/page="+page_num;
			console.log("Final Location: "+ final_location);
			window.location.href = final_location;
		}
		else{
			console.log("Last '/' = "+wlh.lastIndexOf("/"));
			console.log("'/page=' at "+wlh.indexOf("/page="));
		}
	}
	else{
		window.location.href = wlh + "/page="+page_num
	}
}

