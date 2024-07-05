// $(document).on("change", ".no_of_nozzle" , function() {
//     var nozzle_size=$(this).val();
//     var dataid=$(this).attr('dataid')
//     var html=''
//     html +='<table class="table bordered" style="border: 1px solid #f8f8f8;">' 
//     for(var i=0;i<nozzle_size;i++){
//         html +='<tr>'
//         html +='<td><input type="text" name="nozzle_size'+dataid+'" class="form-control nozzle_size" dataid='+dataid+'></td>'
//         html +='</tr>'
//     }
//     html +='</table>' 
//     $('#nozzle_table'+dataid+'').append(html)
// })
$(document).on("change", ".no_of_nozzle" , function() {
    var nozzle_size=$(this).val();
    var dataid=$(this).attr('dataid')
    var rowCounts = $('#nozzlestable_actual'+dataid+' tr').length;
    var uppendrow= nozzle_size-(rowCounts)
    var rows = "";
    if(uppendrow >=0){
      for(var i=0;i<uppendrow;i++){
        rows +='<tr><td><input type="number" data-id="actual_nozzle_size" name="nozzle_size'+dataid+'" class="form-control nozzle_size noz-mar-bot" dataid='+dataid+'><span class="nozzle_size_error"></span></td></tr>'
        }
        $('#nozzlestable_actual'+dataid+'').append(rows);
    }
    else{
      for(var i=uppendrow;i<0;i++){
        $('#nozzlestable_actual'+dataid+' tr:last').remove();
    }
    } 
    var max=[];
    var values = 0;
    $(".nozzle_size").each(function(){
      values += parseFloat(Math.pow($(this).val(),2));
    });
    var unit = document.getElementById('project_unit').value;
    if(unit == 'API'){
      var property_value = Math.PI/4096*(values)
      $("#tfa"+dataid+"").val(property_value.toFixed(2));
    }
    else{
      var property_value = Math.PI/4*(values)
      $("#tfa"+dataid+"").val(property_value.toFixed(2));
    }
})
$(document).on("blur", ".nozzle_size" , function() {
    var unit = document.getElementById('project_unit').value;
    var dataid=$(this).attr('dataid')
    var max=[];
    var values = 0;
    $(".nozzle_size").each(function(){
      values += parseFloat(Math.pow($(this).val(),2));
    });
    if(unit == 'API'){
      var property_value = Math.PI/4096*(values)
      $("#tfa"+dataid+"").val(property_value.toFixed(2));
    }
    else{
      var property_value = Math.PI/4*(values)
      $("#tfa"+dataid+"").val(property_value.toFixed(2));
    }
});
$(document).on("click", "#add_drillbit" , function() {
  var panel_count = $('.panel').length
  var panel_html=$('.panel').html()
  var type=$('#type').val();
  var new_panel_html='<div class="panel panel-default">'+panel_html+'</div>'
  $('#accordion').append(new_panel_html)
  $('.panel:last').find('.expand-btn').attr('href','#collapseOne'+panel_count+'')
  $('.panel:last').find('.collapse').attr('id','collapseOne'+panel_count+'')
  $('.panel:last').find('.no_of_nozzle').attr('dataid',panel_count)
  $('.panel:last').find('.nozzle_table').attr('id','nozzle_table'+panel_count+'')
  $('.panel:last').find('.nozzle_size').attr('name','nozzle_size'+panel_count+'')
  $('.panel:last').find('.nozzle_size').attr('dataid',panel_count)
  $('.panel:last').find('.tfa').attr('id','tfa'+panel_count+'')
  $('.panel:last').find('.nozzle_table').html("")
  if(type == 'edit'){
    $('.panel:last').find('.start_date').val("")
    $('.panel:last').find('.start_time').val("")
    $('.panel:last').find('.serial_no').val("")
    $('.panel:last').find('.bit_type').val("")
    $('.panel:last').find('.bhaname').val("")
    $('.panel:last').find('.manufacture').val("")
    $('.panel:last').find('.idac_code').val("")
    $('.panel:last').find('.no_of_nozzle').val("")
    $('.panel:last').find('.nozzle_size').val("")
    $('.panel:last').find('.tfa').val("")
    $('.panel:last').find('.drill_id').val("")
  }
})
$(document).on("click", ".remove_drillbit" , function() {
  $(this).closest('.panel').remove()
})

