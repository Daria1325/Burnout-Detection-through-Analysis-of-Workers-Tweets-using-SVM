// Get results data to JSON
const url_emp = document.getElementsByClassName('container')[0].getAttribute('data-url');

var data_string = document.getElementsByClassName('container')[0].getAttribute('data-js-vars').replace(/'/g, '"');
var string_split = data_string.slice(1, data_string.length-1).split('},').map(s=> s+'}');

string_split[string_split.length-1] = string_split[string_split.length-1].slice(0,string_split[string_split.length-1].length-1);

var results = [];
for (let i = 0; i< string_split.length; i++){
    results.push(JSON.parse(string_split[i]) || '{}');
}

function fill_all_employees_table(){
    var table = document.getElementById('myTable');

for (emp of results){
    var tr = document.createElement('tr');   

    var td = document.createElement('td');
    td.classList.add("col-11", "border-bottom-0", "border-top-0", "border-left-0", "pb-0");
    td.setAttribute('style', "border-width: 10px;");
    if (emp.state == "L"){
        td.classList.add( "border-success");
    }
    if (emp.state == "M"){
        td.classList.add( "border-warning");
    }
    if (emp.state == "H"){
        td.classList.add( "border-danger");
    }
    if (emp.state == "N"){
        td.classList.add( "border-dark");
    }

    var link = document.createElement("a");
    link.setAttribute('href', url_emp.replace('0',emp.id));
    link.setAttribute('class', "text-decoration-none link-dark");

    var note = document.createElement('p');
    note.textContent = emp.note;
    note.setAttribute("class","mb-1");

    var name_emp = document.createElement('h4');
    name_emp.textContent=emp.name;
    name_emp.setAttribute("class","mb-0");

    link.appendChild(name_emp);
    link.appendChild(note);
    
    td.appendChild(link);
    tr.appendChild(td);

    table.appendChild(tr);
}
}
function fill_grouped_employees_table(category){
    var table = document.getElementById('myTable_'+category);
    table.innerHTML="";
for (const emp of results){
    
    if (emp.state==category || emp.progress==category){
        var tr = document.createElement('tr');   

        var td = document.createElement('td');
        td.classList.add("col-11", "border-bottom-0", "border-top-0", "border-left-0", "pb-0");
        td.setAttribute('style', "border-width: 10px;");
        if (emp.state == "L"){
            td.classList.add( "border-success");
        }
        if (emp.state == "M"){
            td.classList.add( "border-warning");
        }
        if (emp.state == "H"){
            td.classList.add( "border-danger");
        }
        if (emp.state == "N"){
            td.classList.add( "border-dark");
        }
    
        var link = document.createElement("a");
        link.setAttribute('href', url_emp.replace('0',emp.id));
        link.setAttribute('class', "text-decoration-none link-dark");
    
        var note = document.createElement('p');
        note.textContent = emp.note;
        note.setAttribute("class","mb-1");
    
        var name_emp = document.createElement('h4');
        name_emp.textContent=emp.name;
        name_emp.setAttribute("class","mb-0");
    
        link.appendChild(name_emp);
        link.appendChild(note);
        
        td.appendChild(link);
        tr.appendChild(td);
    
        table.appendChild(tr);
    }
}
}

$(function(){  
    const tabElems = document.querySelectorAll('button[data-bs-toggle="tab"]')
    tabElems.forEach(function (tabElem) {
      tabElem.addEventListener('shown.bs.tab', function (e) {
        fill_grouped_employees_table(e.target.getAttribute('category'));
      })
    })
  })

if (location.pathname == '/'){
    fill_all_employees_table()
}
if (location.pathname == '/grouped/'){
    fill_grouped_employees_table("H");
}


