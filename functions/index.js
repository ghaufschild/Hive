const functions = require('firebase-functions');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

function performDailyUpdate() {
	var today = new Date();
	var queryDateString = today.toISOString().substring(0,10);

	console.log("Should be 2020-03-03: " + queryDateString);

	var xhttp = new XMLHttpRequest();

	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	       console.log(xhttp.responseText);
	       console.log("HTTP request called successfully")
	    }
	};

	xhttp.open('GET', "https://ipinfo.io/json", true);
	xhttp.send();

}

exports.scheduledFunctionCrontab = functions.pubsub.schedule('55 11 * * *')
  .timeZone('America/New_York')
  .onRun((context) => {
  console.log('This will be run every day at 11:55 AM Eastern!');
  performDailyUpdate();
  return null;
});

performDailyUpdate();