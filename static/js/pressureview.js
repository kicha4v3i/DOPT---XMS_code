$(document).ready( function () {
    $('.table_css').DataTable();
    
    var tvdunit=$("#tvdunit").val();
    var csrf =$('[name="csrfmiddlewaretoken"]').val();
    var pressureunit=$("#pressureunit").val();
    var well_id=$('#well_id').val();
    var pore_pressure_list=[];
    var fracture_pressure_list=[];
    var muddatachart=[];
    var tvd_array=[];
    $.ajax({
      type: "POST",
      data:{'well_id':well_id,'pressureunit':pressureunit},
      url:"/wells/pressure/getinterpolatedata",
      beforeSend: function(xhr){
        xhr.setRequestHeader('X-CSRFToken', csrf);
      },
      success: function(data) {
        for(var i=0;i<data.tvd.length;i++){
        pore_pressure_list.push([data.tvd[i],data.pore_pressure[i]])
        fracture_pressure_list.push([data.tvd[i],data.fraction_pressure[i]]);
        }
        for(var i=0;i<data.muddatamd.length;i++){
          muddatachart.push([parseFloat(data.mudtvd[i]),data.mudweight[i]])
        }
        if(pore_pressure_list.length>0)
        {
          $('.charts').show();
  
  
          chart(pore_pressure_list,fracture_pressure_list,muddatachart)  
        }
      }
    });
});