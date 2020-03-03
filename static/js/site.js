// var text = '{ "results": [' +
//     '{ "year":"2020", "month":"01", "day":"01", "y":0.5, "url":"google.com", "title":"google"},' +
//     '{ "year":"2020", "month":"01", "day":"02", "y":0.7, "url":"google.com", "title":"amazon"},' +
//     '{ "year":"2020", "month":"01", "day":"03", "y":0.3, "url":"google.com", "title":"firefox"},' +
//     '{ "year":"2020", "month":"01", "day":"04", "y":-0.2, "url":"google.com", "title":"explorer"}]}';
//
// var chartData = JSON.parse(text).results;
//
// for (var i = 0; i < 4; i++) {
//     chartData[i].x = new Date(chartData[i].year, chartData[i].month, chartData[i].day);
// }
//
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
    $.get(query, function (err, req, resp) {
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
            // chart.options.data[0].dataPoints = results
            $('#chartContainer').css({
                'border': 'solid black 5px'
            });
            document.getElementById("chartContainer").style.display = ""
            document.getElementById("placeholder").style.display = "none"
            chart.render();
        }
    });
}

var fields = 1;
var max_fields = 4;

// function removeEntry(e) {
//     // window.alert("REMOVE");
//     e.preventDefault();
//     console.log($(this));
//     fields--;
// }

$(".form-wrapper").on("click", ".remove-entry", function(e) {
    e.preventDefault();
    $(this).parent().parent().remove();
    if (fields == max_fields) {
        $(".create-entry").prop("disabled", false);
    }
    fields--;
});

function createEntry(e) {
    // window.alert("CREATE");
    e.preventDefault();
    if (fields < max_fields) {
        fields++;
        $(".form-wrapper").append(
            '<div class="form-row">'+
                '<div class="form-group col-md-9">'+
                    '<label for="topic">Topic</label>'+
                    '<input type="string" class="form-control" id="topic" placeholder="Enter a topic here...">'+
                '</div>'+
                '<div class="form-group col-md-2">'+
                    '<label for="relevancy-threshold">RT</label>'+
                    '<select type="number" class="form-control 1-100" id="relevancy-threshold"></select>'+
                    '<script>'+
                        '$(function(){'+
                            'var $select = $(".1-100");'+
                            'for (i=1;i<=100;i++){'+
                                '$select.append($("<option></option>").val(i).html(i))'+
                            '}'+
                        '});'+
                    '</script>'+
                '</div>'+
                '<div class="form-group col-md-1">'+
                    '<label for="inputPassword4">&nbsp;</label>'+
                    '<button class="remove-entry btn btn-block btn-link">&#10060;</button>'+
                '</div>'+
            '</div>'
        );
        if (fields == max_fields) {
            // $(".create-entry").hide();
            $(".create-entry").prop("disabled", true);
        }
    } else {
        window.alert("You have reached the maximum number of search fields.")
    }
}
