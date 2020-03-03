var chartData = ""; function titleCase(str) { var splitStr = str.toLowerCase().split(' '); for (var i = 0; i
    < splitStr.length;
        i++) { // You do not need to check if i is larger than splitStr length, as your for does that for you // Assign it back
        to the array splitStr[i]=s plitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1); } // Directly return the joined
        string return splitStr.join( ' '); } function getTrending() { var query="/trending" ; $.get(query, function (err, req,
        resp) { if (req=="success" ) { var trending=r esp.responseJSON.results; var trendingHasData=f alse; var defaultTopic=""
        ; var html="" ; for (var topic in trending) { var currTopic=t rending[topic]; var title=c urrTopic.query_string; var
        change=c urrTopic.change; if(change==0 ) { change=0 .00; } for (var i=0 ; i < currTopic.results.length; i++) { currTopic.results[i].x=n
        ew Date(currTopic.results[i].year, currTopic.results[i].month - 1, currTopic.results[i].day); // console.log(results[i].x);
        } html +='<hr><div class="row ' ; if (change> 0) {
                        html += 'up';
                    } else if (change < 0) {
                        html += 'down';
                    } else {
                        html += 'flat';
                    }

                    if (currTopic.results.length > 1) {
                        html += ' hasData " onclick="askBob(\'' + title + '\')';
                        if (!trendingHasData) {
                            trendingHasData = true;
                            defaultTopic = title;
                            bob.push(currTopic);
                        }
                    } else {
                        html += ' noData';
                    }
                    html += '">';

                    html += '<div class="col-9 text-left">'
                    html += '<h4>' + titleCase(title) + ' ' + currTopic.change + '</h4>'
                    html += '</div><div class="col-3 text-left"></div></div>'
                }
                $(html).appendTo("#trending");


                if (trendingHasData) {
                    askBob(defaultTopic);
                }

            } else {
                html = "No data found";
                $("#trending").html(html);
            }
        });
    }

    getTrending();

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
                chart.options.data[0].dataPoints = results
                $('#chartContainer').css({
                    'border': 'solid black 5px'
                });
                document.getElementById("chartContainer").style.display = ""
                document.getElementById("placeholder").style.display = "none"
                chart.render();
            }
        });
    }

    function askBob(topic) {
        document.getElementById("chartContainer").style.display = "none"
        document.getElementById("placeholder").style.display = ""
        $("#chartContainer").empty();
        var chart = createChart();
        chart.options.title.text = "Sentiment for " + topic

        console.log(topic);
        chart.options.data[0].dataPoints = bob[topic];
        $('#chartContainer').css({
            'border': 'solid black 5px'
        });
        document.getElementById("chartContainer").style.display = ""
        document.getElementById("placeholder").style.display = "none"
        chart.render();
    }


    function createChart(chartData) {
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
            }]
        });
        return chart;
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
