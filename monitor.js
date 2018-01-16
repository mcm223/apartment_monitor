// Self-invoking function
(function() {
	window.onload = function() {
		function loadJSON(callback){
			var xobj = new XMLHttpRequest();
			xobj.overrideMimeType("application/json");
			xobj.open('GET', 'js/output.json', true);
			xobj.onreadystatechange = function() {
				if (xobj.readyState == 4 && xobj.status == "200") {
					callback(xobj.responseText);
				}
			};
		xobj.send(null);
		}

	// More stuff
	loadJSON(function(response) {
		var result = JSON.parse(response);
		// Get spans in html
		var temp = document.getElementById('temp');
		var high = document.getElementById('high');
		var low = document.getElementById('low');
		var hum = document.getElementById('hum');
		
		// Populate json data into html
		temp.textContent = result.currentTemp.toFixed(1) + '*F.';
		high.textContent = result.todaysHigh.toFixed(1) + '*F.';
		low.textContent = result.todaysLow.toFixed(1) + '*F.';
		hum.textContent = result.currentHumidity.toFixed(1) + '%.';
	});
	}
})();