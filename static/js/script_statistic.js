// Get results data to JSON
var data_string = document.getElementsByClassName('container')[0].getAttribute('data-js-vars').replace(/'/g, '"');
var dataForChart = JSON.parse(data_string);


document.getElementById('end_date').value = dataForChart['end_date'];
document.getElementById('start_date').value = dataForChart['start_date'];
$("#select_chart").val(dataForChart['chart']).trigger('change.select2');
$("#select_group").val(dataForChart['group']).trigger('change.select2');

function formLink(){
    var start_date = document.getElementById('start_date').value;
    var end_date = document.getElementById('end_date').value;
    var chart = document.getElementById('select_chart').value;
    var group = document.getElementById('select_group').value;
    var link = `/statistic/${start_date}/${end_date}/${group}/${chart}/`;
    return (link)
}

$('#start_date').on('change', function (e) {
    const link = formLink();
    window.location.assign(link);
  });

$('#end_date').on('change', function (e) {
    const link = formLink();
    window.location.assign(link);
  });
$('#select_chart').on('change', function (e) {
    const link = formLink();
    window.location.assign(link);
  });
$('#select_group').on('change', function (e) {
    const link = formLink();
    window.location.assign(link);
  });

var chart;
if (dataForChart['chart']== 'Line'){
    chart = createLineChartDate(dataForChart);
}
if (dataForChart['chart']== 'Pie'){
  chart = createPieChartDate(dataForChart);
}
if (dataForChart['chart']== 'Column' || dataForChart['chart']== 'Stucked'){
  chart = createBarChartDate(dataForChart);
}

function createLineChartDate(dataForChart){
    const ctx = document.getElementById('myChart');
    var labels = dataForChart['labels'];

    var datasets = [{
      label: 'Low',
      data: dataForChart['L'],
      fill: false,
      borderColor: '#25BE4B',
      tension: 0.5
    },{
      label: 'Moderate',
      data: dataForChart['M'],
      fill: false,
      borderColor: '#FFA550',
      tension: 0.5
    },{
      label: 'High',
      data: dataForChart['H'],
      fill: false,
      borderColor: '#BE253A',
      tension: 0.5
    },{
      label: 'No data',
      data: dataForChart['N'],
      fill: false,
      borderColor: '#282E30',
      tension: 0.5
    },];
    
    const data = {
      labels: labels,
      datasets: datasets
    };
    
    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    suggestedMin: 0
                }
            }
        }
    };
    
    chart = new Chart(ctx, config);
    return chart;
}

function createPieChartDate(dataForChart){
  const ctx = document.getElementById('myChart');
  
  const data = {
    labels: dataForChart['labels'],
    datasets: [{
      data: dataForChart['count'],
      backgroundColor: dataForChart['backgroundColor'],
      hoverOffset: 4
    }]
  };
  
  const config = {
    type: 'pie',
    data: data,
  };
  
  chart = new Chart(ctx, config);
  return chart;
}

function createBarChartDate(dataForChart){
  const ctx = document.getElementById('myChart');
  
  const labels = dataForChart['labels'];
  const data = {
  labels: labels,
  datasets: [{
    label: 'Low',
    data: dataForChart['L'],
    backgroundColor:'#25BE4B'
  },
  {
    label: 'Moderate',
    data: dataForChart['M'],
    backgroundColor:'#FFA550'
  },
  {
    label: 'High',
    data: dataForChart['H'],
    backgroundColor:'#BE253A'
  },
  {
    label: 'No data',
    data: dataForChart['N'],
    backgroundColor:'#282E30'
  }]
  };
  
  var config = {
    type: 'bar',
    data: data,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };

  if (dataForChart['chart']=='Stucked'){
      config['options'] = {
        responsive: true,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true
          }
        }
      }
  }
  
  chart = new Chart(ctx, config);
  return chart;
}
