$(function() {
$(document).on("keyup",".pump_speed",function() {  
   var trindex=$(this).closest('tr').index();
   var pump_speed=$(this).val();
   var unit=$('#unit').val();
   var types=$('#types').val();
   var stroke_length=$( "#stroke_length").val();
   var roddiameter=$( "#roddiameter").val();
   if(types=='Duplex'){
      var length=roddiameter;
   }else{
      var length=stroke_length;
   }
   flowratecalculation(trindex,pump_speed,unit,types,length);
})
$(document).on("keyup",".linear_size",function() {  
   var unit=$('#unit').val();
   var types=$('#types').val();
   var stroke_length=$( "#stroke_length").val();
   var roddiameter=$( "#roddiameter").val();
   if(types=='Duplex'){
      var length=roddiameter;
   }else{
      var length=stroke_length;
   }
   $('#mudpumptable tbody tr').each(function(index){
      if(index!=0){
         var pump_speed=$('.mudpumptable tbody tr:eq('+index+') th').find('.pump_speed').val();
         flowratecalculation(index,pump_speed,unit,types,length);
      }
   })
})
function flowratecalculation(trindex,pump_speed,unit,types,length){
   $('#mudpumptable tbody tr:eq('+trindex+') td').each(function(index){
      var curren_ele=$(this);
      var corresponding_linearsize=$('.mudpumpdata tbody tr td:eq('+index+')').find('.linear_size').val();
      var csrf =$('[name="csrfmiddlewaretoken"]').val();
      if(corresponding_linearsize!='' && length!='' && unit!='' && types!='' && pump_speed!=''){
         $.ajax({
            type: "GET",
            url:"/wells/mud/flowratecalculation",
            contentType: 'application/json',  
            data: {
               'linear_size' : corresponding_linearsize,
               'length' : length,
               'pump_speed' :  pump_speed,
               'type' : types,
               'unit' : unit
            },
            dataType: "json",
            beforeSend: function(xhr){
               xhr.setRequestHeader('X-CSRFToken', csrf);
            },
            success: function(data) { 
               curren_ele.find("input[name='flowrate']").val(data);
            }
         });
      }



   })

}
});