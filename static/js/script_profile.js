$( '#multiple-select-field' ).select2( {
    theme: "bootstrap-5",
    width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
    placeholder: $( this ).data( 'placeholder' ),
    closeOnSelect: false,
} );


// Get results data to JSON
var data_string = document.getElementsByClassName('container')[0].getAttribute('data-js-vars').replace(/'/g, '"');
var string_split = data_string.slice(1, data_string.length-1).split('},').map(s=> s+'}');
string_split[string_split.length-1] = string_split[string_split.length-1].slice(0,string_split[string_split.length-1].length-1);
var results = [];
for (let i = 0; i< string_split.length; i++){
    results.push(JSON.parse(string_split[i]) || '{}');
}

var props = ["N"];
var filtered_results = [];

document.getElementById('end_date').value = moment().format('YYYY-MM-DD');
document.getElementById('start_date').value = moment().subtract(6, 'months').format('YYYY-MM-DD');

filtered_results = filter_results_by_date("","", results);

var chart = createChart(results, props)

function filter_results_by_date(start, end, results){
    if (end===""){
        document.getElementById('end_date').value = moment().format('YYYY-MM-DD');
        end = document.getElementById('end_date').value;
    }
    if (start===""){
        document.getElementById('start_date').value = moment().subtract(6, 'months').format('YYYY-MM-DD');
        start = document.getElementById('start_date').value;
    }
    
    end = Date.parse(end);
    start = Date.parse(start);

    filtered_results = [];
    for (let i = 0; i < results.length; i++){
        var result_date = Date.parse(results[i].scan_date);
        
        if (end >= result_date && start <= result_date){
            filtered_results.push(results[i]);
        }
    }
    return filtered_results
}


$('#start_date').on('change', function (e) {
    var start_date = document.getElementById('start_date').value;
    var end_date = document.getElementById('end_date').value;
    
    filtered_results = filter_results_by_date(start_date, end_date, results)
    chart.destroy();
    chart = createChart(filtered_results,props);
  });

  $('#end_date').on('change', function (e) {
    var start_date = document.getElementById('start_date').value;
    var end_date = document.getElementById('end_date').value;
    
    filtered_results = filter_results_by_date(start_date, end_date, results)
    chart.destroy();
    chart = createChart(filtered_results,props);
  });



function getProperties(data){
    var props = [];
    for (let i = 0; i < data.length; i++){
        props.push(data[i].id);
    }
    return props;
}

$('#multiple-select-field').on('change', function (e) {
    var data = $('#multiple-select-field').select2('data');
    props = getProperties(data);
    chart.destroy();
    chart = createChart(filtered_results,props);
  });



function createChart(results, properties){
    const ctx = document.getElementById('myChart');
    var labels = [];
    var data_normal = [];
    var data_lonely = [];
    var data_stressed = [];
    var data_count = [];
    for (let i = 0; i < results.length; i++){
        labels.push(results[i].scan_date);
        data_normal.push(results[i].percent_N);
        data_lonely.push(results[i].percent_L);
        data_stressed.push(results[i].percent_S);
        const sum_count = results[i].count_N + results[i].count_L +results[i].count_S;
        data_count.push(sum_count);
    }

    var datasets = [];
    for (let i = 0; i < properties.length; i++){
        if (properties[i]=="N"){
            datasets.push({
                label: 'Normal',
                data: data_normal,
                fill: false,
                borderColor: '#25BE4B',
                tension: 0.5
              })
        }
        if (properties[i]=="L"){
            datasets.push({
                label: 'Lonely',
                data: data_lonely,
                fill: false,
                borderColor: '#2585BE',
                tension: 0.5
              })
        }
        if (properties[i]=="S"){
            datasets.push({
                label: 'Stressed',
                data: data_stressed,
                fill: false,
                borderColor: '#BE253A',
                tension: 0.5
              })
        }
        if (properties[i]=="C"){
            datasets.push({
                label: 'Count',
                data: data_count,
                fill: false,
                borderColor: '#282E30',
                tension: 0.5
              })
        }

    }

    
    
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
                    suggestedMin: 0,
                    suggestedMax: 1
                }
            }
        }
    };
    
    chart = new Chart(ctx, config);
    return chart;
}


