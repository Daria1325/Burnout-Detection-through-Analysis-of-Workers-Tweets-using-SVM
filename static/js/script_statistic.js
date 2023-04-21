// Get results data to JSON
var data_string = document.getElementsByClassName('container')[0].getAttribute('data-js-vars').replace(/'/g, '"');
var dataForChart = JSON.parse(data_string);


document.getElementById('end_date').value = dataForChart['end_date'];
document.getElementById('start_date').value = dataForChart['start_date'];
var now = new Date(), maxDate = now.toISOString().substring(0,10);
document.getElementById('end_date').setAttribute('max',maxDate);
document.getElementById('start_date').setAttribute('max',maxDate);

$(document).ready(function() {
  $('#select_chart').select2({
    theme: "bootstrap-5",
    width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
    placeholder: $( this ).data( 'placeholder' ),
    closeOnSelect: false,
    minimumResultsForSearch: Infinity
  });
});

$(document).ready(function() {
  $('#select_group').select2({
    theme: "bootstrap-5",
    width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
    placeholder: $( this ).data( 'placeholder' ),
    closeOnSelect: false,
    minimumResultsForSearch: Infinity
  });
});


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
if (dataForChart['chart']== 'Line' && dataForChart['group']!='Position'){
    chart = createLineChartDate(dataForChart);
}
if (dataForChart['chart']== 'Line' && dataForChart['group']=='Position'){
  chart = createLineChartPosition(dataForChart);
  //uncheck all exept first position
  for (var i = 1; i< dataForChart['positions'].length;i++){
    document.getElementById(dataForChart['positions'][i]+"_Low").checked=false;
    document.getElementById(dataForChart['positions'][i]+"_High").checked=false;
    document.getElementById(dataForChart['positions'][i]+"_No Data").checked=false;
    document.getElementById(dataForChart['positions'][i]+"_Moderate").checked=false;
  }
}
if (dataForChart['chart']== 'Pie' && dataForChart['group']=='Date'){
  chart = createPieChartDate(dataForChart);
}
if (dataForChart['chart']== 'Pie' && dataForChart['group']!='Date'){
  createPieChartPosition(dataForChart);
}
if (dataForChart['chart']== 'Column' || dataForChart['chart']== 'Stucked'){
  chart = createBarChart(dataForChart);
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
    var config
    if (dataForChart['group']=='Time'){
      config = {
        type: 'line',
        data: data,
        
        options: {
          maintainAspectRatio: false,         
          scales: {
                y: {
                    suggestedMin: 0
                }
            },
          plugins: [ChartDataLabels]
        }
    };
    }else{
      config = {
        type: 'line',
        data: data,
        
        options: {
          maintainAspectRatio: false,         
            scales: {
                y: {
                    suggestedMin: 0
                }
            }
        }
    };
    }


    
    
    chart = new Chart(ctx, config);
    return chart;
}

function changeDiagramLine(id){
  var index=null;
    for (var j = 0; j < chart.data.datasets.length;j++){
      if (chart.data.datasets[j].label===id){
        index= j;
        break;
      }
    }
    if (index != null){
      const visibilityData = chart.isDatasetVisible(index);
      if (visibilityData === true){
        chart.hide(index);
      }

      if (visibilityData === false){
        chart.show(index);
      }   
    }
}

$(':checkbox').change(function() {
    const position = this.id;
    changeDiagramLine(position);
     
});

function createLineChartPosition(dataForChart){

  var legendBox = document.getElementById("legendBox");

  for (var i = 0; i< dataForChart['positions'].length;i++){

    var div_position = document.createElement('div');
    div_position.classList.add("col-sm-3", "col-md-12", "p-0");

    var btn = document.createElement('button');
    btn.id = "label_"+ dataForChart['positions'][i];
    btn.textContent = dataForChart['positions'][i];
    btn.setAttribute("data-toggle","collapse");
    btn.setAttribute("data-target",'#collapse'+i);
    btn.classList.add("btn", "w-100","text-md-left", "text-sm-center", "shadow-none", "border-0");

    var check_div = document.createElement('div');
    check_div.id = 'collapse'+i;
    check_div.classList.add("collapse", i.toString(), "text-left", "ms-5");
    check_div.setAttribute("data-parent",'#legendBox');

    var input = document.createElement('input');
    input.type="checkbox";
    input.value = "Low";
    input.checked = true;
    input.classList.add("form-check-input");
    input.id = dataForChart['positions'][i]+"_Low";
    check_div.appendChild(input);

    var label = document.createElement('label')
    label.htmlFor = dataForChart['positions'][i]+"_Low";
    label.appendChild(document.createTextNode('Low'));
    label.classList.add("m-0");
    check_div.appendChild(label);
    check_div.appendChild(document.createElement('br'));

    var input = document.createElement('input');
    input.type="checkbox";
    input.value = "Moderate";
    input.id = dataForChart['positions'][i]+"_Moderate";
    input.classList.add("form-check-input");
    input.checked = true;
    check_div.appendChild(input);
    var label = document.createElement('label')
    label.htmlFor = dataForChart['positions'][i]+"_Moderate";
    label.appendChild(document.createTextNode('Moderate'));
    label.classList.add("m-0");
    check_div.appendChild(label);
    check_div.appendChild(document.createElement('br'));

    var input = document.createElement('input');
    input.type="checkbox";
    input.value = "High";
    input.id=dataForChart['positions'][i]+"_High";
    input.classList.add("form-check-input");
    input.checked = true;
    check_div.appendChild(input);
    
    var label = document.createElement('label')
    label.htmlFor = dataForChart['positions'][i]+"_High";
    label.appendChild(document.createTextNode('High'));
    label.classList.add("m-0");
    check_div.appendChild(label);
    check_div.appendChild(document.createElement('br'));

    var input = document.createElement('input');
    input.type="checkbox";
    input.value = "No data";
    input.id=dataForChart['positions'][i]+"_No Data";
    input.classList.add("form-check-input");
    input.checked = true;
    check_div.appendChild(input);
    var label = document.createElement('label')
    label.htmlFor = dataForChart['positions'][i]+"_No Data";
    label.appendChild(document.createTextNode('N/D'));
    label.classList.add("m-0");
    check_div.appendChild(label);
    check_div.appendChild(document.createElement('br'));

    div_position.appendChild(btn);
    div_position.appendChild(check_div);  
    legendBox.appendChild(div_position);  
  }

  const ctx = document.getElementById('myChart');
  var labels = dataForChart['labels'];

  var dataset = [{
    label: dataForChart['positions'][0]+'_Low',
    data: dataForChart['L'][0],
    fill: false,
    borderColor: '#25BE4B',
    tension: 0.5
  }]
  for (var i = 1; i< dataForChart['positions'].length;i++){
    dataset.push({
      label: dataForChart['positions'][i]+'_Low',
      data: dataForChart['L'][i],
      fill: false,
      borderColor: '#25BE4B',
      hidden: true,
      tension: 0.5
    })
  }

  for (var i = 1; i< dataForChart['positions'].length;i++){
    dataset.push({
      label: dataForChart['positions'][i]+'_Moderate',
      data: dataForChart['M'][i],
      fill: false,
      hidden: true,
      borderColor: '#FFA550',
      tension: 0.5
    })
  }

  dataset.push({
    label: dataForChart['positions'][0]+'_Moderate',
    data: dataForChart['M'][0],
    fill: false,
    borderColor: '#FFA550',
    tension: 0.5
  })

  for (var i = 1; i< dataForChart['positions'].length;i++){
    dataset.push({
      label: dataForChart['positions'][i]+'_High',
      data: dataForChart['H'][i],
      fill: false,
      hidden: true,
      borderColor: '#BE253A',
      tension: 0.5
    })
  }

  dataset.push({
    label: dataForChart['positions'][0]+'_High',
    data: dataForChart['H'][0],
    fill: false,
    borderColor: '#BE253A',
    tension: 0.5
  })

  for (var i = 1; i< dataForChart['positions'].length;i++){
    dataset.push({
      label: dataForChart['positions'][i]+'_No Data',
      data: dataForChart['N'][i],
      fill: false,
      hidden: true,
      borderColor: '#282E30',
      tension: 0.5
    })
  }

  dataset.push({
    label: dataForChart['positions'][0]+'_No Data',
    data: dataForChart['N'][0],
    fill: false,
    borderColor: '#282E30',
    tension: 0.5
  })
  
  const data = {
    labels: labels,
    datasets: dataset
  };
  
  const config = {
      type: 'line',
      data: data,
      options: {
        maintainAspectRatio: false,
        plugins:{
          legend: {
            display: false
          }
        },
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
  document.getElementById('chartContainer').classList.add('col-lg-5');
  
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
    options: {
      plugins: {
          title:{
            display: true,
           text:  'The results of all employees in this time period',
          },
          legend: {
              display: true,
              position: 'right'
          },
          tooltip:{
            enabled: false
          }
      },
      plugins: dataForChart['labels'],
      maintainAspectRatio: false,
      
  }
  };
  
  chart = new Chart(ctx, config);
  return chart;
}

function createPieChartPosition(dataForChart){
  
  document.getElementById('chartContainer').classList.remove("chart_lg");

  const ctx1 = document.getElementById('myChart');
  const ctx2 = document.getElementById('myChart1');
  const ctx3 = document.getElementById('myChart2');
  const ctx4 = document.getElementById('myChart3');
  const dataForCharts = dataForChart['chartData'];
  
  var count = 1;
  for (const item in dataForCharts){
    var data = {
      labels: dataForCharts[item]['labels'],
      datasets: [{
        data: dataForCharts[item]['count'],
        backgroundColor: dataForCharts[item]['backgroundColor'],
        hoverOffset: 4
      }]
    };

    var title = "";
    if (count==1){
      title = "Low";
    }else if (count==2){
      title = "Medium";
    }else if (count==3){
      title = "High";
    }else{
      title = "No Data";
    }
    
    var config = {
      type: 'pie',
      data: data,
      options: {
        plugins: {
            title:{
              display: true,
             text:  title
            },
            legend: {
                display: true,
                position: 'right'
            }
        },
        maintainAspectRatio: false,
        
    }
    };
    if (count==1){
      new Chart(ctx1, config);
    }
    if (count==2){
      new Chart(ctx2, config);
    }
    if (count==3){
      new Chart(ctx3, config);
    }
    if (count==4){
      new Chart(ctx4, config);
    }
    count+=1;
    
  }
}

function createBarChart(dataForChart){
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
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  };

  if (dataForChart['chart']=='Stucked'){
      config['options'] = {
        maintainAspectRatio: false,
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
