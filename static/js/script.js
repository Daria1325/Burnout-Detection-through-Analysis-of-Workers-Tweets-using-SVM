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