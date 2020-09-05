Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var canvasChardId = 'statistic';
var chart_labels = ["Решено", "Не решено"]
var backgroundColor = ['#1cc88a', '#E7494C'];
var hoverBackgroundColor = ['#17a673', '#B84144'];

function init_chart(group_id, topic_id){
    var topic = statistic_for_group[group_id]['topics'][topic_id];
    var ctx = document.getElementById(`${canvasChardId}-${group_id}-${topic_id}`);
    var newChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: chart_labels,
        datasets: [{
          data: [topic.solved, topic.unsolved],
          backgroundColor: backgroundColor,
          hoverBackgroundColor: hoverBackgroundColor,
          hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
        },
        legend: {
          position:'bottom',
          display: true
        },
        cutoutPercentage: 80,
      },
    });

}

$(document).ready(function(){
    for(group_id in statistic_for_group){
        for (topic_id in statistic_for_group[group_id].topics){
            init_chart(group_id, topic_id);
        }
    }
})