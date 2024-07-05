
var closesttrindex;
$(document).on("click", ".casing_size" , function() {  
    closesttrindex=$(this).closest('tr').index();
    var casing_type = $(this).closest('tr').find('.casing_type').val(); 
    if(casing_type != 13){
    $('.casingmaster-popup').modal('show');
    }
})
$('.start_date').on('change',function(){
  var currentelement=$(this)
  var closestndex=$(this).closest('tr').index()
  var selected_date=$(this).val()
  var selected_time=$('#wellphasesaddtable tbody tr:eq('+closestndex+')').find('.start_time').val()
  previousindex=closestndex-1
  if(closestndex>0){
   var previous_date=$('#wellphasesaddtable tbody tr:eq('+previousindex+')').find('.start_date').val()
   var previous_time=$('#wellphasesaddtable tbody tr:eq('+previousindex+')').find('.start_time').val()
  }
  else{
    var previous_date=""
    var previous_time=""
  }
  if(selected_date!='' && selected_time!=''){
      getmdtvd(selected_date,selected_time,previous_date,previous_time,currentelement)
  }
})
$('.start_time').on('change',function(){
  var currentelement=$(this)
  var closestndex=$(this).closest('tr').index()
  var selected_time=$(this).val()
  var selected_date=$('#wellphasesaddtable tbody tr:eq('+closestndex+')').find('.start_date').val()
  previousindex=closestndex-1
  if(closestndex>0){
   var previous_date=$('#wellphasesaddtable tbody tr:eq('+previousindex+')').find('.start_date').val()
   var previous_time=$('#wellphasesaddtable tbody tr:eq('+previousindex+')').find('.start_time').val()
  }
  else{
    var previous_date=""
    var previous_time=""
  }
  if(selected_date!='' && selected_time!=''){
      getmdtvd(selected_date,selected_time,previous_date,previous_time,currentelement)
  }
})

$(".casing_nominal_od").change(function () { 
  var nominal_od_val = $(this).val();
  var nominal_od = $(this).find(':selected').attr('databasevalue');
  var well_id=$('#well').val();
  var hole_size=$('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.hole_size').val();
  var casing_type=$('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.casing_type').val();
  if(parseFloat(hole_size) < parseFloat(nominal_od_val)){
  if(casing_type!=2){
      alert("Hole size is greater then casing size");
      $(this).val("");
      return false;
  }
  
  }else{
  
  $.ajax({ 
  type: "GET",                      
  url: "/wells/wellphases/getcasingweight",                    
  data: {
      nominal_od:nominal_od,
      well_id:well_id
  },
  dataType: "json",
  success: function (data) {  
      $(".casing_weight option").remove();
      $('.casing_weight').append('<option value="">Weight</option>');
      for(i=0;i<data.data.length;i++){
      $('.casing_weight').append('<option databasevalue ="'+data.data[i].databasevalue+'" value="'+data.data[i].weight +'">'+ data.data[i].weight+'</option>');
      }
      $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.casing_size').val(nominal_od_val);
      $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.nominal_od').val(nominal_od_val);
  }
  });
  }
});
$("#casing_weight").change(function () { 
  var casing_weight = $('#casing_weight').find(':selected').attr('databasevalue');  
  let weight_val = $(this).val();
  var well_id=$('#well').val();
  var nominal_od = $('.nominal_od').find(':selected').attr('databasevalue');
  $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.weight').val(weight_val);

 //  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(collar_weight);
  $.ajax({ 
    type: "GET",                      
    url: "/wells/wellphases/getcasing_connection_type",                    
    data: {
     casing_weight:casing_weight,
     nominal_od:nominal_od,
     well_id:well_id
    },
    dataType: "json",
    success: function (data) {   
     $(".connection_type option").remove();
     $('.connection_type').append('<option value="">Connection Type</option>');
     for(i=0;i<data.data.length;i++){
       $('.connection_type').append('<option value="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</option>');
     }
  }

  });
});
$(document).on("click", ".popup-close" , function() { 
  $('.casing_nominal_od').val('');
  $('.casing_weight').val('');
  $('.grade').val('');
  $('.connection_type').val('');
  $('.casing_range').val('');
  $('.casingmaster-popup').modal('hide');
});
$(document).ready(function() {
    $('body').on('change',".wellphase_startdate", function(){
       var selecteddate=$(this).val()
       var closestndex=$(this).closest('tr').index()
       previousindex=closestndex-1
       console.log(previousindex)
       var current_element=$(this)
       if(closestndex>0){
        var previous_date=$('#wellphasesaddtable tbody tr:eq('+previousindex+')').find('.wellphase_startdate').val()
        console.log(previous_date)
       }
       else{
        var previous_date="" 
       }
       var data=[{'selecteddate':selecteddate,'previous_date':previous_date}];
       $.ajax({
          type: "POST",
          url:"/wells/wellphases/getmdtvd_actualwell",
          data: {
            selecteddate:selecteddate,
            previous_date:previous_date,
            well_id:well_id,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
          },
          success: function(data) { 
            console.log(data)
            console.log(data.md)
            console.log(data.tvd)

            current_element.closest('tr').find('.measured_depth').val(data.md)
            current_element.closest('tr').find('.true_vertical_depth').val(data.tvd)

          }
      });
    });

    $('.linertop').hide();
    var storedArray = JSON.parse(sessionStorage.getItem("items"));
    if(well_id == storedArray[1]){
      $('.warning').show();
    }else{
      $('.warning').hide();
    }

    $('.collapsed').on('click', function(){
        let collapsedcont = $(this).attr('href');
        $(collapsedcont).toggle();
    });
    
    // $("#wellphasesform").validate({
    //   rules: {
    //     phase_name:"required",
    //     casing_type:"required",
    //     hole_size:"required",
    //     casing_size:"required",
    //     measured_depth:"required",
    //     true_vertical_depth:"required",
    //     //lineartop:"required",
    //   },
    //   messages: {
    //     phase_name:"Please enter the Phase Name",
    //     casing_type:"please select the  Casing Type",
    //     hole_size:"Please enter the Hole Size",
    //     casing_size:"Please enter the Casing Size",
    //     measured_depth:"Please enter the MD",
    //     true_vertical_depth:"Please enter the TVD",
    //     //lineartop:"Please enter the Linear Top",
    //   }
    // });
    $(document).on("blur", ".measured_depth" , function() {  
        measured_depth = $(this).val();
        var current_element=$(this);
        $.ajax({
            type: "GET",
            url:"/wells/wellphases/getmdtvd",
            data: {
              data : measured_depth,
              type :"md",
              well_id:well_id
      
            },
            success: function(data) { 
              current_element.closest('tr').find('.true_vertical_depth').val(data.toFixed(2));
            }
        });
    });
    $(document).on("blur", ".true_vertical_depth" , function() {  
        true_vertical_depth = $(this).val();
        var current_element=$(this);
        $.ajax({
            type: "GET",
            url:"/wells/wellphases/getmdtvd",
            data: {
              data : true_vertical_depth,
              type :"tvd",
              well_id:well_id
            },
            success: function(data) { 
              current_element.closest('tr').find('.measured_depth').val(data.toFixed(2));
            }
        });
        
    });




    $("#grade").change(function () { 
        var grade = $(this).val();  
        $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.wellphase_grade').val(grade);
    });
    $("#connection_type").change(function () { 
    var grade = $(this).val();  
    
    $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.wellphase_connection_type').val(grade);
    });
    $("#casing_range").change(function () { 
    var grade = $(this).val();  
    $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.wellphase_range').val(grade);
    });
    $("#drift_id").blur(function () { 
    var drift_id = $(this).val();  
    $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.driftid').val(drift_id);
    });
    $(document).on("blur", ".others_range" , function() { 
        others_range=$(this).val();
        var current_element=$(this);
        if(others_range!=''){
        $.ajax({ 
           type: "GET",                      
           url: "/wells/wellphases/insertrange",                    
           data: {
            range:others_range,
           },
           dataType: "json",
           success: function (data) {   
             if(data.status=="true"){
                if(current_element.closest('td').find('.casing_range option[value="'+others_range+'"]').length==0){
                  current_element.closest('td').find('.casing_range option').eq(3).before($("<option selected></option>").val(others_range).text(others_range));
                  $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.wellphase_range').val(others_range);
                }
             }
          }
         });
        }
      });
      $(document).on("blur", ".others_grade" , function() { 
        var csrf =$('.getcsrf').val();
        others_grade=$(this).val();
        var current_element=$(this);
        if(others_grade!=''){
        $.ajax({ 
           type: "POST",                      
           url: "/wells/wellphases/insertgrade",                    
           data: {
            grade:others_grade,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
           },
           dataType: "json",
           success: function (data) {   
             console.log(data.status);
             if(data.status=="true"){
              if(current_element.closest('td').find('.grade option[value="'+others_grade+'"]').length==0){
                current_element.closest('td').find('.grade option').eq(3).before($("<option selected></option>").val(others_grade).text(others_grade));
                $('#wellphasesaddtable tbody tr:eq('+closesttrindex+')').find('.wellphase_grade').val(others_grade);
      
              }
             }
          }
         });
        }
      });
      $(document).on('click','#modal-close',function() {
        $('#nominal_od').val('');
        $('#casing_weight').val('');
        $('#grade').val('');
        $('#connection_type').val('');
        $('#casing_range').val('');
        $('.casingmaster-popup').modal('hide');
      });


 
      

   
})
function getmdtvd(selected_date,selected_time,previous_date,previous_time,currentelement){
  $.ajax({
    type: "GET",
    url:"/wells/wellphases/getmdtvd_actualwell",
    data: {
      selected_date:selected_date,
      selected_time:selected_time,
      well_id:well_id,
      previous_date:previous_date,
      previous_time:previous_time
    },
    success: function(data) { 
      currentelement.closest('tr').find('.measured_depth').val(data.md)
      currentelement.closest('tr').find('.true_vertical_depth').val(data.tvd)

    }
});
}
