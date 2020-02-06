function askWatson() {
    var question = $("#question").val();
    question = question.toLowerCase();
    
    var chart = new CanvasJS.Chart("chartContainer", {
      title: {
        text: "Sentiment for " + question
      },
      axisY: {
        title: "Sentiment"
      },
      axisX: {
        title: "Time",
        valueFormatString: "MMM",
        interval: 1,
        intervalType: "month"
      },
      data: [
      {
        type: "line",
        toolTipContent: "<a href = {url}> {title}</a><hr/>Sentiment: {y}",                
  
        dataPoints: bob[question]
      } 
      ]
    });
  
    chart.render();
}