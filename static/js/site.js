var chartData = "";

function titleCase(str) {
    var splitStr = str.toLowerCase().split(' ');
    for (var i = 0; i < splitStr.length; i++) { // You do not need to check if i is larger than splitStr length, as your for does that for you
        // Assign it back to the array
        splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
    }
    // Directly return the joined string
    return splitStr.join(' ');
}

function getTrending() {
    var query = "/trending";
    $.get(query, function (err, req,
        resp) {
        if (req == "success") {
            console.log(resp);
            var trending = resp.responseJSON.results;
            var defaultTopic = "";
            var html = "";
            for (var topic in trending) {
                var currTopic = trending[topic];
                var title = currTopic.query_string;
                var change = Math.round(currTopic.change * 100) / 100;
                if (change == 0) {
                    change = 0.00;
                }
                for (var i = 0; i < currTopic.articles.length; i++) {
                    currTopic.articles[i].x = new Date(currTopic.articles[i].year, currTopic.articles[i].month - 1, currTopic.articles[i].day); // console.log(results[i].x);
                }
                html += '<hr><div class="row ';
                if (change > 0) {
                    html += 'up';
                } else if (change < 0) {
                    html += 'down';
                } else {
                    html += 'flat';
                }

                if (currTopic.articles.length > 1) {
                    html += ' hasData " onclick="askBob(\'' + title + '\')';
                        defaultTopic = title;
                        bob[title] = currTopic.articles;
                } else {
                    html += ' noData';
                }
                html += '">';

                html += '<div class="col-9 text-left">'
                html += '<h4>' + titleCase(title) + ' ' + change + '</h4>'
                html += '</div><div class="col-3 text-left"></div></div>'
            }
            $(html).appendTo("#trending");


            /*if (trendingHasData) {
                askBob(defaultTopic);
            }*/

        } else {
            html = "No data found";
            $("#trending").html(html);
        }
    });
}

getTrending();

function askWatson() {
    document.getElementById("chartContainer").style.display = "none";
    document.getElementById("placeholder").style.display = "";
    var question = $("#question").val();
    question = question.toLowerCase();
 
    var base = '/search?query=';
    var query = base.concat(question);
    query = query.concat("&articles=50");
    var chart = createChart();
    chart.options.title.text = "Sentiment for " + question;
    console.log(query);

    var results = {};

    // HTTP GET request to Flask server
    $.get(query, function (err, req, resp) {
        if (req == "success") {
            console.log('I AM HERE')
            var results = resp.responseJSON.average_sentiment;
            var scatter = resp.responseJSON.articles

            for (var i = 0; i < results.length; i++) {
                results[i].x = new Date(results[i].year, results[i].month - 1, results[i].day);
                // console.log(results[i].x);
            }

            for (var i = 0; i < scatter.length; i++) {
                scatter[i].x = new Date(scatter[i].year, scatter[i].month - 1, scatter[i].day);
                // console.log(results[i].x);
            }

            if(results.length == 0) {
                document.getElementById("chartContainer").style.display = ""
                document.getElementById("placeholder").style.display = "none"
                $('#chartContainer').html("No data found.")
            } else {
                console.log(results)
                chart.options.data[0].dataPoints = results
                $('#chartContainer').css({
                    'border': 'solid black 5px'
                });
                document.getElementById("chartContainer").style.display = ""
                document.getElementById("placeholder").style.display = "none"
                var data = {
                    type: "scatter",
                    toolTipContent: "<a href = {url} target='_blank'> {title}</a><hr/>Sentiment: {y}",
                    dataPoints: scatter
                }
                chart.options.data.push(data);
                chart.render();
            }
        } else {
            chart.options.data[0].dataPoints = bob["default"];
            // chart.options.data[0].dataPoints = results;
            $('#chartContainer').css({
                'border': 'solid black 5px'
            });
            document.getElementById("chartContainer").style.display = "";
            document.getElementById("placeholder").style.display = "none";
            chart.render();
        }
    });
}

function addScatter(chart) {
    var data = {
        type: "scatter",
        toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}",
        dataPoints: bullshit()
    }
    //chart.options.data.push(data);
}

function bullshit() {
    var data = [
        {
            "x": new Date(2012, 00, 1),
            "title": "Fuck",
            "url": "https://en.wikinews.org/wiki/Family_of_Four_Found_Dead_in_Disney_Community,_Suspect_in_Custody",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 00, 1),
            "title": "Fuck",
            "url": "https://en.wikinews.org/wiki/Family_of_Four_Found_Dead_in_Disney_Community,_Suspect_in_Custody",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 00, 1),
            "title": "Fuck",
            "url": "https://en.wikinews.org/wiki/Family_of_Four_Found_Dead_in_Disney_Community,_Suspect_in_Custody",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 00, 1),
            "title": "Fuck",
            "url": "https://en.wikinews.org/wiki/Family_of_Four_Found_Dead_in_Disney_Community,_Suspect_in_Custody",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 01, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/Senator_Ted_Cruz_proposes_amendment_to_U.S._Constitution_setting_Congressional_term_limits",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 01, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/Senator_Ted_Cruz_proposes_amendment_to_U.S._Constitution_setting_Congressional_term_limits",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 01, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/Senator_Ted_Cruz_proposes_amendment_to_U.S._Constitution_setting_Congressional_term_limits",
            "y": betweenValue()
        },      
        {
            "x": new Date(2012, 01, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/Senator_Ted_Cruz_proposes_amendment_to_U.S._Constitution_setting_Congressional_term_limits",
            "y": betweenValue()
        },    
        {
            "x": new Date(2012, 02, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/State-run_bus_crashes_in_Cuba_en_route_to_Havana,_killing_seven",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 02, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/State-run_bus_crashes_in_Cuba_en_route_to_Havana,_killing_seven",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 02, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/State-run_bus_crashes_in_Cuba_en_route_to_Havana,_killing_seven",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 02, 1),
            "title": "You",
            "url": "https://en.wikinews.org/wiki/State-run_bus_crashes_in_Cuba_en_route_to_Havana,_killing_seven",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 03, 1),
            "title": "Piece",
            "url": "https://en.wikinews.org/wiki/NASA%27s_TESS_spacecraft_reports_its_first_exoplanet",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 03, 1),
            "title": "Piece",
            "url": "https://en.wikinews.org/wiki/NASA%27s_TESS_spacecraft_reports_its_first_exoplanet",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 03, 1),
            "title": "Piece",
            "url": "https://en.wikinews.org/wiki/NASA%27s_TESS_spacecraft_reports_its_first_exoplanet",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 03, 1),
            "title": "Piece",
            "url": "https://en.wikinews.org/wiki/NASA%27s_TESS_spacecraft_reports_its_first_exoplanet",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 04, 1),
            "title": "Of",
            "url": "https://en.wikinews.org/wiki/Category:Space_Shuttle_Discovery",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 04, 1),
            "title": "Of",
            "url": "https://en.wikinews.org/wiki/Category:Space_Shuttle_Discovery",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 04, 1),
            "title": "Of",
            "url": "https://en.wikinews.org/wiki/Category:Space_Shuttle_Discovery",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 04, 1),
            "title": "Of",
            "url": "https://en.wikinews.org/wiki/Category:Space_Shuttle_Discovery",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 05, 1),
            "title": "Shit",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 05, 1),
            "title": "Shit",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 05, 1),
            "title": "Shit",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 05, 1),
            "title": "Shit",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 06, 1),
            "title": "Yeet",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 06, 1),
            "title": "Yeet",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 06, 1),
            "title": "Yeet",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        },
        {
            "x": new Date(2012, 06, 1),
            "title": "Yeet",
            "url": "https://en.wikinews.org/wiki/Slow-cooking_dinosaur_eggs_may_have_contributed_to_extinction,_say_scientists",
            "y": betweenValue()
        }
    ]

    return data;
}

function betweenValue() {
    if(Math.random() > 0.5) {
        return Math.round(Math.random()*100)/100*-1;
    } else {
        return Math.round(Math.random()*100)/100
    }
}

function advSearch() {
    document.getElementById("chartContainer").style.display = "none";
    document.getElementById("placeholder").style.display = "";

    var chart = createChart();
    chart.options.title.text = "Sentiment for Advanced Search";

    var topics = document.getElementsByClassName("topic-input");
    var terms = [];
    var queries = [];
    for (i = 0; i < topics.length; i++) {
        if ((topics[i].value).length != 0) {
            var base = '/search?';
            var term = (topics[i].value).toLowerCase();
            terms.push(term);
            var query = base.concat('query=', term, '&articles=1');
            queries.push(query);
        }
    }

    console.log(queries);

    if (queries.length == 0) {
        window.alert("Please enter at least one topic to search.");
    }

    for (i = 0; i < queries.length; i++) {
        var results = {};

        // HTTP GET request to Flask server
        $.get(queries[i], function (err, req, resp) {
            if (req == "success") {
                results = resp.responseJSON.articles;
                var search = resp.responseJSON.query_string;

                for (var j = 0; j < results.length; j++) {
                    results[j].x = new Date(results[j].year, results[j].month - 1, results[j].day);
                }
                console.log(results);

                if (i != 0) {
                    chart.options.data.push({type: "line", toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}", dataPoints: results, showInLegend: "true", legendText: search});
                }
                // chart.options.data[i].dataPoints = results;
                // chart.options.data[i].showInLegend = "true";
                // chart.options.data[i].legendText = term;

                $('#chartContainer').css({
                    'border': 'solid black 5px'
                });
                document.getElementById("chartContainer").style.display = "";
                document.getElementById("placeholder").style.display = "none";
                chart.render();
            } else {
                results = bob["default"];

                if (i != 0) {
                    chart.options.data.push({type: "line", toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}", dataPoints: {}});
                }
                chart.options.data[i].dataPoints = results;
                chart.options.data[i].showInLegend = "true";
                chart.options.data[i].legendText = term;

                $('#chartContainer').css({
                    'border': 'solid black 5px'
                });
                document.getElementById("chartContainer").style.display = "";
                document.getElementById("placeholder").style.display = "none";
                chart.render();
            }
        });

        // FOR TESTING LOCALLY
        // if (i != 0) {
        //     chart.options.data.push({type: "line", toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}", dataPoints: {}});
        // }
        // chart.options.data[i].dataPoints = bob[topics[i].value];
        // chart.options.data[i].showInLegend = "true";
        // chart.options.data[i].legendText = (topics[i].value).toLowerCase();
    }
}

function askTrending(question) {
    document.getElementById("chartContainer").style.display = "none"
    document.getElementById("placeholder").style.display = ""

    question = question.toLowerCase();
 
    var base = '/search?query=';
    var query = base.concat(question);
    query = query.concat("&articles=50");
    var chart = createChart();
    chart.options.title.text = "Sentiment for " + question

    // HTTP GET request to Flask server
    $.get(query, function (err, req, resp) {
        if (req == "success") {
            console.log('I AM HERE')
            results = resp.responseJSON.articles;

            for (var i = 0; i < results.length; i++) {
                results[i].x = new Date(results[i].year, results[i].month - 1, results[i].day);
                // console.log(results[i].x);

            }
            if(results.length == 0) {
                document.getElementById("chartContainer").style.display = ""
                document.getElementById("placeholder").style.display = "none"
                $('#chartContainer').html("No data found.")
            } else {
                console.log(results)
                chart.options.data[0].dataPoints = results
                $('#chartContainer').css({
                    'border': 'solid black 5px'
                });
                document.getElementById("chartContainer").style.display = ""
                document.getElementById("placeholder").style.display = "none"
                addScatter(chart)
                chart.render();
            }

        } else {
            chart.options.data[0].dataPoints = bob["default"];
            chart.options.data[0].dataPoints = results
            $('#chartContainer').css({
                'border': 'solid black 5px'
            });
            document.getElementById("chartContainer").style.display = ""
            document.getElementById("placeholder").style.display = "none"
            addScatter(chart);
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
    addScatter(chart);
    chart.render();
}

function askBobTest() {
    var topic = "patriots";
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
    addScatter(chart);
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
            intervalType: "day",
            interval: 1
        },
        data: [{
            type: "line",
            toolTipContent: "<a href = {url}, target='_blank'>{title}</a><hr/>Sentiment: {y}",

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

$(".form-wrapper").on("click", ".remove-entry", function (e) {
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
            '<div class="form-row">' +
            '<div class="form-group col-md-11">' +
            '<label for="topic">Topic</label>' +
            '<input type="string" class="form-control topic-input" id="topic" placeholder="Enter a topic here...">' +
            '</div>' +
            '<div class="form-group col-md-1">' +
            '<label for="inputPassword4">&nbsp;</label>' +
            '<button class="remove-entry btn btn-block btn-link">&#10060;</button>' +
            '</div>' +
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
