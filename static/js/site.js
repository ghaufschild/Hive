var text = '{ "results": [' +
'{ "year":"2020", "month":"01", "day":"01", "y":0.5, "url":"google.com", "title":"google"},' +
'{ "year":"2020", "month":"01", "day":"02", "y":0.7, "url":"google.com", "title":"amazon"},' +
'{ "year":"2020", "month":"01", "day":"03", "y":0.3, "url":"google.com", "title":"firefox"},' +
'{ "year":"2020", "month":"01", "day":"04", "y":-0.2, "url":"google.com", "title":"explorer"}]}';

var chartData = JSON.parse(text).results;

for (var i = 0; i < 4; i++) {
    chartData[i].x = new Date(chartData[i].year, chartData[i].month, chartData[i].day);
}

var chart = new CanvasJS.Chart("chartContainer", {
    animationEnabled: true,
    title: {
        text: "Sentiment Graph"
    },
    axisY: {
        maximum: 1,
        minimum: -1,
        title: "Sentiment"
    },
    axisX: {
        title: "Time",
        valueFormatString: "MMM DD",
        interval: 1
    },
    data: [{
        type: "line",
        toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}",

        // dataPoints: bob[question] || bob["default"]

        dataPoints: chartData
    }]
});

function askWatson() {
    document.getElementById("chartContainer").style.display = "none"
    document.getElementById("placeholder").style.display = ""
    var question = $("#question").val();
    question = question.toLowerCase();

    var base = '/search/';
    var query = base.concat(question);

    chart.options.title.text = "Sentiment for " + question

    // HTTP GET request to Flask server
    $.get(query, function(err, req, resp){
        if (req == "success") {
            console.log('I AM HERE')
            results = resp.responseJSON.results;

            for (var i = 0; i < results.length; i++) {
                results[i].x = new Date(results[i].year, results[i].month - 1, results[i].day);
                // console.log(results[i].x);

            }
            console.log(results)
            chart.options.data[0].dataPoints = results
            $('#chartContainer').css({
                'border': 'solid black 5px'
            });
            document.getElementById("chartContainer").style.display = ""
            document.getElementById("placeholder").style.display = "none"
            chart.render();

        } else {
            chart.options.data[0].dataPoints = bob["default"];
            $('#chartContainer').css({
                'border': 'solid black 5px'
            });
            document.getElementById("chartContainer").style.display = ""
            document.getElementById("placeholder").style.display = "none"
            chart.render();
        }
    });
}
