const accountSid = 'AC564dda9224e183521c28d931d65cb6d9';
const authToken = '6e39de7cbae0f589ade80d3454ce4edc';

const client = require('twilio')(accountSid, authToken);

const functions = require('firebase-functions');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;


function sendMessage() {
	client.messages
	  .create({
	     body: 'This is a test message',
	     from: '+16093373229',
	     to: '+15714390820'
	   })
	  .then(message => {
	  	console.log(message.sid); 
	  	return null}).catch(() => null);
	 //return null;
}


function performDailyUpdate() {
	var today = new Date();
	var queryDateString = today.toISOString().substring(0,10);

	console.log("Should be 2020-03-03: " + queryDateString);

	var xhttp = new XMLHttpRequest();

	xhttp.onreadystatechange = function() {
	    if (this.readyState === 4 && this.status === 200) {
	       console.log(xhttp.responseText);
	       console.log("HTTP request called successfully")
	    }
	};

	xhttp.open('GET', "https://ipinfo.io/json", true);
	xhttp.send();
	return null;
}

//exports.scheduledFunctionCrontab = functions.pubsub.schedule('55 11 * * *')
exports.scheduledFunctionCrontab = functions.pubsub.schedule('every 15 minutes')
  .timeZone('America/New_York')
  .onRun((context) => {
  console.log('This will be run every day at 11:55 AM Eastern!');
  performDailyUpdate();
  sendMessage();
  return null;
});

console.log("Hello");
sendMessage();
performDailyUpdate();
