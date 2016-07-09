$(function() {
    $( ".button" ).button();
})

$(function() {
    $( "#radio_severity" ).buttonset();
});

$(function() {
    $( "#radio_area" ).buttonset();
});
$(function() {
    $( "#radio_cost_func" ).buttonset();
});

$(document).ready(function(){
    $('#resultTable').dataTable({
        "iDisplayLength": 50,
        "bJQueryUI": true
    });
});

$(document).ready(function(){
    $('#resultTable2').dataTable({
        "iDisplayLength": 50,
        "bJQueryUI": true
    });
});

$(document).ready(function(){
    $('#detailTable').dataTable({
        "bPaginate": false,
        "bJQueryUI": true
    });
});