
if(window.location.pathname.includes("grouped")){
  document.getElementById("grouped_tab").classList.add("active");
}
if(window.location.pathname=="/"){
  document.getElementById("all_employees_tab").classList.add("active");
}
if(window.location.pathname.includes("statistic")){
  document.getElementById("statistic_tab").classList.add("active");
}

$(document).ready(function() {
  $('#id_position').select2({
    theme: "bootstrap-5",
    // width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
    placeholder: $( this ).data( 'placeholder' ),
    closeOnSelect: false,
    minimumResultsForSearch: Infinity
  });
});


// FIlter anything
$(document).ready(function(){
    $("#anythingSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myDIV *").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });

  // Filter table

$(document).ready(function(){
  $("#tableSearch").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$(function(){
  var dtToday = new Date();

  var month = dtToday.getMonth() + 1;
  var day = dtToday.getDate();
  var year = dtToday.getFullYear();

  if(month < 10)
      month = '0' + month.toString();
  if(day < 10)
      day = '0' + day.toString();

  var maxDate = year + '-' + month + '-' + day;    
  $('#txtDate').attr('max', maxDate);
});