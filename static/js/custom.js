
var mdLastData = mdLastData;
console.log('ssssmmm',mdLastData)
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"

  $("form[name='adduserform']").validate({
    // Specify validation rules
    rules: {
      name: "required",
      // email: {
      //   required: true,
      //   email: true
      // },
      email: {
        required: true,
        email: true,
        remote:{
                    url: '../usermailexists',
                    type: "get",
                    data:
                    {
                        email: function()
                        {
                            return $('#email').val();
                        },      
                        id: function()
                        {
                            return $('#id').val();
                        }
                    },
                    dataFilter: function(data) {
                      var json = JSON.parse(data);
                      return !json.email;
                  }
                  }
      },
      password: {
            required: true,
            // password_regex: true,
            // minlength: 8,

      },
      confirmpassword : {
        required: function(){
          return $("#id").val()==""?true:false;
    },
    minlength : 5,
          equalTo : "#password"
      },
      group: "required",

    },

    messages: {
      name: "Please enter your name",
      password: {
        required: "Please provide a password",
        // minlength: "Your password must be at least 8 characters long",
        // password_regex: "Password should have minimum 8 letters consisting atleast one from A-Z, a-z, 0-9 and special characters",
      },
      confirmpassword: {
          required: "Please provide a password",
          minlength: "Your password must be at least 8 characters long",
          equalTo: "Your passwords doesnot match"
        },
      // email: "Please enter a valid email address",
      email:{
        required: "Please provide a email",
        email: "Please provide a valid email",
        remote: jQuery.validator.format("{0} is already taken.")
      },
      group: "Please Select a Role",
      
    },
    submitHandler: function(form) {
      form.submit();
    }
  });
  $.validator.addMethod("password_regex", function(value) {
    return /^.*(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).*$/.test(value);
});
  $("form[name='edituserform']").validate({
    // Specify validation rules
    rules: {
      name: "required",
      email: {
        required: true,
        email: true,
      },
    },
    messages: {
      name: "Please enter your name",
      // email: "Please enter a valid email address",
      email:{
        required: "Please provide a email",
        email: "Please provide a valid email",
      },      
    },
    submitHandler: function(form) {
      form.submit();
    }
  });
  $("#pressureunit").change(function (obj) {
    $(".pressureunit").html("("+this.value+")");
  });
  
  $("#unit").change(function (obj) {
  if(this.value=="API")
  {
    $("#strokelengthunit").html("(in)");

    $("#linearsizeunit").html("(in)");
    $("#pressureunit").html("(Psi)");
    $("#flowrateunit").html("(GPM)");

  }
  else
  {
    $("#strokelengthunit").html("(mm)");
    $("#linearsizeunit").html("(mm)");
    $("#pressureunit").html("(MPa)");
    $("#flowrateunit").html("(LPM)");

  }
});
  $("#environment").change(function () {
  $(".environment-fields").hide(); 
  $("#environment_sub_type").empty(); 
 
    if(this.value=="Onshore")
    {
      $(".onshore").show(); 

      $('#environment_sub_type').append("<option value='standalone'>STANDALONE</option>","<option value='padtype'>PADTYPE</option>");
    }
    else if(this.value=="Offshore")
    {
      $(".offshore").show(); 

      $('#environment_sub_type').append("<option value='standalone'>STANDALONE</option>","<option value='platform'>PLATFORM</option>","<option value='subsea'>SUBSEA</option>","<option value='swamp'>SWAMP</option>");
    }
  });
  $('#projectwell').change(function(){
    $('.well_fields').show();
  })
  

  $("#environment_sub_type").change(function () {
    $(".sub-environment-fields").hide(); 
 
    if(this.value=="padtype" && $("#environment").val()=="Onshore") 
    {
      $(".onshore-pad").show(); 
    }
    else if((this.value=="platform"||this.value=='swamp') && $("#environment").val()=="Offshore")
    {
      if(this.value=="swamp")
      {
        $(".offshore-swamp").show(); 

      }
      else
      {
        $(".offshore-swamp").show(); 
        $(".offshore-platform").show(); 

      }

    }
    else if(this.value=="subsea" && $("#environment").val()=="Offshore") 
    {
      $(".offshore-subsea").show(); 

    }
  });

});
function tags_value(val){
  var environment_type = val.type;
  $('#environment_sub_type').val(environment_type);
  if (environment_type =='platform'){
    $(".offshore-platform").show(); 
  }
  else{
    $(".offshore-platform").hide();
  }
 } 
$("#projection").change(function(){
  $("#zone").hide();
   if ($("#projection").val()==56)
   {
     $("#zone").show();
   }
 });
$(function(){
  $("#zone").hide();
   if ($("#projection").val()==56)
   {
     $("#zone").show();
   }

  $('#eye').click(function(){
       
        if($(this).closest('span').find('i').hasClass('icon-eye-off')){
           
          $(this).closest('span').find('i').removeClass('icon-eye-off');
          
          $(this).closest('span').find('i').addClass('icon-eye');
          
          $('.passwordfield').attr('type','text');
          // $('.conformpasswordfield').attr('type','text');
            
        }else{
         
          $(this).closest('span').find('i').removeClass('icon-eye');
          
          $(this).closest('span').find('i').addClass('icon-eye-off');  
          
          $('.passwordfield').attr('type','password');
          // $('.conformpasswordfield').attr('type','confirmpassword');
        }
    });
    $('#eyes').click(function(){
      if($(this).closest('span').find('i').hasClass('icon-eye-off')){
         
        $(this).closest('span').find('i').removeClass('icon-eye-off');
        
        $(this).closest('span').find('i').addClass('icon-eye');
        
        $('.conformpasswordfield').attr('type','text');
          
      }else{
       
        $(this).closest('span').find('i').removeClass('icon-eye');
        
        $(this).closest('span').find('i').addClass('icon-eye-off');  
        
        $('.conformpasswordfield').attr('type','password');
      }
  });
});


setTimeout(function() {
  $('.messages').fadeOut('fast');
}, 5000); // <-- time in milliseconds


function format(item) {
if (!item.id) {
  return item.text;
}
// var url = "https://lipis.github.io/flag-icon-css/flags/4x3/";
var baseUrl = window.location.host;
var url = "http://"+baseUrl+"/static/images/flags/icon/";

var img = $("<img>", {
  class: "img-flag",
  width: 26,
  src: url + item.element.getAttribute('data-code').toLowerCase() + ".svg"
});
var span = $("<span>", {
  text: " " + item.text
});
span.prepend(img);
return span;
}
$(document).ready(function() {
$("#inputCountryid").select2({
  templateResult: function(item) {
    return format(item);
  }
});
coords.init( 'input[type="coords"]' );

$(".addmudpumpcolumn").click(function(){
  $('.linearsize').append('<td><input type="number" class="form-control linear_size" id="linear_size" name="linear_size" ><span class="linersize_error"></span></td>');
  $('.pressure').append('<td><input type="number" step="any" class="form-control max_discharge_pressure" name="max_discharge_pressure" ><span class="max_discharge_error"></span></td>');
  $('.flowrate').append('<td><input type="number" step="any" class="form-control flowrate" id="flowrate" name="flowrate" ><span class="flowrate_error"></span></td>');
});

$(".addmudpumprow").click(function(){

  $(".flowrateth").attr('colspan',5);
  var boxold='';
  boxold +='<tr class="flowrate">';
  boxold +='<th><input type="number" class="form-control pump_speed" name="pump_speed" id="pump_speed" ><span class="pump_speed_error"></span></th>';
  $(".mudpumptable tbody tr:last td").each(function(index) {
      boxold +='<td><input type="number" class="form-control flowrate" id="flowrate" name="flowrate" ><span class="flowrate_error"></span></td>';
  });
  boxold +='</tr>';
  $('#mudpumptable tbody').append(boxold);
});

$('.removemudpumprow-master').click(function(){
  $('.mudpumptable tr:last').remove();
})
$('.removemudpumpcolumn-master').click(function(){
  $(".mudpumpdata tbody tr td:last-child").remove();
  $(".mudpumptable tbody tr td:last-child").remove(); 
})

// remove row and column in mud

// $( ".mudpumptable tbody tr" ).each( function(){
//   this.parentNode.removeChild( this ); 
// });
// $( ".mudlineartable tbody tr" ).each( function(){
//   this.parentNode.removeChild( this ); 
// });
// $(".addsurfacepiperow").click(function(){
//     $("#surfacepipeaddtable tr:last").clone().find('input').val('').end().insertAfter("#surfacepipeaddtable tr:last");
// });

//   $(".addpressurerow").click(function(){
//     $("#pressureaddtable tr:last").clone().find('input').val('').end().insertAfter("#pressureaddtable tr:last");
// });


//Append row for Pore Pressure
// $("#pressureaddtable").on("click",".pressureaddrows" , function() {
    
// $("<tr id='pressurerow '>"+ $('#pressurerow2').html()+" </tr>").insertAfter($(this).closest('tr'));
// $('#presssureaddtable > tbody > tr:gt(0)').find(".pressureremoverows").show();
 
//  });
//  $("#pressureaddtable").on("click", ".pressureremoverows" , function() 
//  {    
//   var rowCounts = $('#pressureaddtable >tbody >tr').length;
//   if(rowCounts<5)
//   {
//     $('#pressureaddtable > tbody > tr:gt(0)').find(".pressureremoverows").hide();
//   }  
//  var whichtr =$(this).closest("tr");
//  whichtr.remove();
// });

$("#pressureaddtable").on("click",".pressureaddrows" , function() {
  $("<tr id='pressurerow'>"+ $('#pressurerow2').html()+" </tr>").insertAfter($(this).closest('tr'));
  $('#pressureaddtable > tbody > tr:gt(0)').find(".pressureremoverows").show();
  
  });
  $("#pressureaddtable").on("click", ".pressureremoverows" , function() 
  {   
    var rowCounts = $('#pressureaddtable >tbody >tr').length;
    if(rowCounts<5)
    {
      $('#pressureaddtable > tbody > tr:gt(0)').find(".pressureremoverows").hide();
    }   
  var whichtr =$(this).closest("tr");
  whichtr.remove();
  });
  


// $(".addwellphasesrow").click(function(){
// $("#wellphasesaddtable tr:last").clone().find('input').val('').end().insertAfter("#wellphasesaddtable tr:last");
// });

// $(".addwelltrajectoryrow").click(function(){
//   $("#welltrajectoryaddtable tr:last").clone().find('input').val('').end().insertAfter("#welltrajectoryaddtable tr:last");
// });

//Append row for wellTrajectory
$("#welltrajectoryaddtable").on("click",".welltrajectoryaddrows" , function() {
  $("<tr id='welltrajectorytableRow '>"+ $('#welltrajectorytableRow2').html()+" </tr>").insertAfter($(this).closest('tr'));
  $('#welltrajectoryaddtable > tbody > tr:gt(0)').find(".welltrajectoryremoverows").show();
 
 });
 $("#welltrajectoryaddtable").on("click", ".welltrajectoryremoverows" , function() 
 {    
  var rowCounts = $('#welltrajectoryaddtable >tbody >tr').length;
  if(rowCounts<4)
  {
    $('#welltrajectoryaddtable > tbody > tr:gt(0)').find(".welltrajectoryremoverows").hide();
  }  
 var whichtr =$(this).closest("tr");
 whichtr.remove();
});
});

// wellphases row append
$("#wellphasesaddtable").on("click",".addwellphasesrows" , function() {
$("<tr id='wellphasetableRow' class='wellphase_row' >"+ $('#wellphasetableRow2').html()+" </tr>").insertAfter($(this).closest('tr'));
$('#wellphasesaddtable > tbody > tr:gt(0)').find(".deletewellphasesrow").show();
 });
 $("#wellphasesaddtable").on("click", ".deletewellphasesrow" , function() 
 {    
  var rowCounts = $('#wellphasesaddtable >tbody >tr').length;
  if(rowCounts<4)
  {
    $('#wellphasesaddtable > tbody > tr:gt(0)').find(".deletewellphasesrow").hide();
  }  
 var whichtr =$(this).closest("tr");
 whichtr.remove();
});

// $("#wellphasesaddtable").on("click", ".addwellphasesrows" , function() {
//   $("<tr>"+ $('#wellphasetableRow').html()+" </tr>").insertAfter($(this).closest('tr'));

//   $('#wellphasesaddtable > tbody > tr:gt(0)').find(".deletewellphasesrow").show();
  
//   });

// $("#wellphasesaddtable").on("click", ".deletewellphasesrow" , function()
//   {
//   var whichtr =$(this).closest("tr");
//   whichtr.remove();
// });-
// surfacepiping row append
$("#surfacepipeaddtable").on("click",".surfaceaddrows" , function() {
// $("<tr id='surfacepipingrow'>"+ $('#surfacepipingrow2').html()+" </tr>").insertAfter($(this).closest('tr'));
// $('#surfacepipeaddtable > tbody > tr:gt(0)').find(".surfaceremoverows").show();
$(this).closest('tr').after(`<tr id="surfacepipingrow2">
<td><input type="text" id="name" class="form-control edit-sur-face text-left" name="name" placeholder="Name"><span class="surface_name"></span></td>
<td class="edit-sur-td"><input type="number" step="any" id="length" class="form-control edit-sur-face" name="length"
    placeholder="Length"><span class="surface_length"></span></td>
<td class="edit-sur-td"><input type="number" step="any" id="identity" class="form-control edit-sur-face" name="identity"
    placeholder="ID"><span class="surface_id"></span></td>
<td>
  <button type="button" name="add" class="surfaceaddrows iconaction" ><i class="fa fa-plus"></i></button>
  <button type="button" name="removerow" class="surfaceremoverows iconaction" ><i class="fa fa-trash"></i></button>
</td>
</tr>`)
 
 });
 $("#surfacepipeaddtable").on("click", ".surfaceremoverows" , function() 
 {    
  var rowCounts = $('#surfacepipeaddtable >tbody >tr').length;
  if(rowCounts<4)
  {
    $('#surfacepipeaddtable > tbody > tr:gt(0)').find(".surfaceremoverows").hide();
  }  
 var whichtr =$(this).closest("tr");
 whichtr.remove();
});

// Drillbitdata row append
$("#drillbittable").on("click",".drillbitadd" , function() {
    
$("<tr id='drillbitrow'>"+ $('#drillbitrow1').html()+" </tr>").insertAfter($(this).closest('tr'));
$('#drillbittable > tbody > tr:gt(0)').find(".drillbitremove").show();
 
 });
 $("#drillbittable").on("click", ".drillbitremove" , function() 
 {
  var rowCounts = $('#drillbittable >tbody >tr').length;
  if(rowCounts<5)
  {
    $('#drillbittable > tbody > tr:gt(0)').find(".drillbitremove").hide();
  }  
 var whichtr =$(this).closest("tr");
 whichtr.remove();
});

//BHA data row append
$(document.body).on("click",".addbhadatarows" , function() {
  var current_index=$(this).closest('tr').index();
  var type=$('#type').val()
  var currentpage=$('#currentpage').val();
  // console.log(currentpage)


  if(well_type=='PLAN'){
    var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();
    cumulative_total=0;
    if(currentpage=="editbha"){
      $('.length_edit').each(function(index){
        // console.log($(this).val())
        if($(this).val()!='' && index<current_index){
          cumulative_total =cumulative_total+parseFloat($(this).val());
        }
      });
    }else{
      $('.length').each(function(index){
        if($(this).val()!='' && index<current_index){
          cumulative_total =cumulative_total+parseFloat($(this).val());
        }
      });
    }

    // console.log(cumulative_total)
    // console.log(currentpage)
    var remaining=total_measured_depth-cumulative_total;
    // console.log(remaining)
    // console.log(total_measured_depth)

    if(parseFloat(cumulative_total)<total_measured_depth){
      $("<tr id='bhadatarow'>"+ $('#bhadatarow1').html()+" </tr>").insertAfter($(this).closest('tr'));
      var newindex=current_index+1;
      if(currentpage=="editbha"){
        $('#bhadatatable tbody tr:eq('+newindex+')').find('.length_edit').val(remaining.toFixed(2));
      }else{
        $('#bhadatatable tbody tr:eq('+newindex+')').find('.length').val(remaining.toFixed(2));
      }
      $('#bhadatatable tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
    }
  $('#bhadatatable > tbody > tr:gt(0)').find(".deletebhadatarow").show();
  }else{
    var data_id=$(this).attr('dataid')
    var rowCount = $('#bhadatatable'+data_id+' >tbody >tr').length;
    var newindex=rowCount-1
    $("<tr id='bhadatarow'>"+ $('#bhadatarow1').html()+" </tr>").insertAfter($(this).closest('tr'));
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#element').attr('name','element'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#type_name').attr('name','type_name'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#type_name').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.rss_button').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.mudmotor_button').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#od').attr('name','od'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#od').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#database_od').attr('name','database_od'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#weight').attr('name','weight'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#pipe_type').attr('name','pipe_type'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#connection_type').attr('name','connection_type'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#tool_od').attr('name','tool_od'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#tool_id').attr('name','tool_id'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#classtype').attr('name','classtype'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#grade').attr('name','grade'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#onejoint_length').attr('name','onejoint_length'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#box_tj_length').attr('name','box_tj_length'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#pin_tj_length').attr('name','pin_tj_length'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#identity').attr('name','identity'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#length').attr('name','length'+data_id+'');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('#length').addClass('actual_length');
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.addbhadatarows ').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.deletebhadatarow ').attr('dataid',data_id);
    $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.cumulative-length').attr('name','length_onejoint'+data_id+'');
    var total_measured_depth=$('#bhadatatable'+data_id+' tbody tr:eq(0)').find('.measured_depth').val();
    if(type='edit'){
      $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.bhaelement_id ').attr('name','bhaelement_id'+data_id+'');

    }
    var cumulative_total=0;
    $('#bhadatatable'+data_id+' tbody tr').each(function(index,tr){
      // console.log(tr)
      // console.log($(tr).find('td input.actual_length').val())
        if($(tr).find('td input.actual_length').val()!=undefined && $(tr).find('td input.actual_length').val()!=''){
            cumulative_total =cumulative_total+parseFloat($(tr).find('td input.actual_length').val());
        }
    });
    console.log(cumulative_total)
    var remaining=total_measured_depth-cumulative_total;

    if(parseFloat(cumulative_total)<total_measured_depth){
      var newindex=current_index+1;
      $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.actual_length').val(remaining);
      $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
    }
  }


 });
 $("#bhadatatable").on("click", ".deletebhadatarow" , function() 
 {   
  var rowCounts = $('#bhadatatable >tbody >tr').length;
  if(rowCounts<5)
  {
    $('#bhadatatable > tbody > tr:gt(0)').find(".deletebhadatarow").hide();
  }   
 var whichtr =$(this).closest("tr");
 whichtr.remove();
});


//Casing data row append
$(document).on("click",".addcasingrows" , function() {
  $("<tr id='casingrow'>"+ $('#casingrow1').html()+" </tr>").insertAfter($(this).closest('tr'));
  $('#casingtable > tbody > tr:gt(0)').find(".deletecasingrow").show();
   
   });
   $("#casingtable").on("click", ".deletecasingrow" , function() 
   {   
    var rowCounts = $('#casingtable >tbody >tr').length;
    if(rowCounts<5)
    {
      $('#casingtable > tbody > tr:gt(0)').find(".deletecasingrow").hide();
    }   
   var whichtr =$(this).closest("tr");
   whichtr.remove();
  });
  

$("#rheogramtable").on("click",".addrheogram" , function() {
var index=$(this).closest('tbody').index()-1;
var html='<td><input type="text" id="rpm" class="form-control valid" name="rpm'+index+'" placeholder="Rpm" aria-invalid="false"></td><td><input type="text" id="dial" class="form-control" name="dial'+index+'" placeholder="Dial" value=""></td><td><button type="button" name="add" class="addrheogram iconaction"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove iconaction"><i class="fa fa-trash"></i></button></td>';
$("<tr>"+ html+" </tr>").insertAfter($(this).closest('tr'));
// $('#rheogramtable > tbody > tr:gt(0)').find(".rheogramremove").show();
});
$("#rheogramtable").on("click", ".rheogramremove" , function() 
{ 
  var rowCounts = $('#rheogramtable >tbody >tr').length;
  if(rowCounts<5)
  {
    $('#rheogramtable > tbody > tr:gt(0)').find(".rheogramremove").hide();
  }   
var whichtr =$(this).closest("tr");
whichtr.remove();
});


$( document ).ready(function() {
var csrf =$('.getcsrf').val();
$("#basicDate").flatpickr({
dateFormat: "Y-m-d"
});
});

$(".roddiameter").hide();
$(".listplanwell").hide();


$(".well_types").click(function () {
  $('.well_types').next('label').removeClass('active');
  $(this).next('label').addClass('active');
  var projectwell=$('#projectwell').val();
  var csrf =$('.getcsrf').val();
  if(this.value=="ACTUAL")
  {
    $(".listplanwell").show();
    // getplanwells(projectwell,csrf)
  }
  else if(this.value=="PLAN")
  {
    $(".listplanwell").hide();
  }
});


$("#projectwell").change(function () {
  var project_id=$(this).val();
  // alert(project_id);
  $.ajax({ 
    type: "GET",                                         
    data: {
      project_id:project_id
    },
    dataType: "json",
    url: "/wells/selectedunit", 
    success: function (data) { 
        if(data.data=='SI'){
          $("label[for='air_gap']").text('Airgap(ft)');
          $("label[for='wellhead_to_datum']").text('Wellhead To Datum(ft)');
          $("label[for='rkb_wellhead']").text('RKB to Wellhead(ft)');
          $("label[for='rkb_datum']").text('RKB to Datum(ft)');
          $("label[for='water_depth']").text('Water Depth(ft)');
          $("label[for='ground_elevation']").text('Ground Elevation(ft)');
        }
        else{
          $("label[for='air_gap']").text('Airgap(m)');
          $("label[for='wellhead_to_datum']").text('Wellhead To Datum(m)');
          $("label[for='rkb_wellhead']").text('RKB to Wellhead(m)');
          $("label[for='rkb_datum']").text('RKB to Datum(m)');
          $("label[for='water_depth']").text('Water Depth(m)');
          $("label[for='ground_elevation']").text('Ground Elevation(m)');
        }
  }

  });

  // });
  var csrf =$('.getcsrf').val();
  getplanwells(this.value,csrf)
});





$( "#pump_name_select" ).change(function() {
  var csrf =$('.getcsrf').val();
    $.ajax({
      type: "GET",
      url:"/wells/mud/getpump",
      contentType: 'application/json',  
      data: {'id':this.value},
      dataType: "json",
      beforeSend: function(xhr){
        xhr.setRequestHeader('X-CSRFToken', csrf);
      },
      success: function(data) {
        // if(data.current_unit == 'API'){
        //   // $(".linersize").html('line')
        //   $('.linersize').html($('.linersize').html().replace($('.linersize').text("Liner Size(mm)")));
        // }
        $(".linearsize").find('th:gt(0)').remove();
        $(".pressure").find('th:gt(0)').remove();
        $('.flowrateth').html($('.flowrateth').html().replace($('.flowrateth').text(),''));
          // var data = JSON.parse(data);
          $('#pump_name').val(data.datas[0].name);
          og_unit=$('#unit').val();
          ig_unit=data.datas[0].unit;
          if(og_unit==ig_unit)
          {
            $('#stroke_length').val(data.datas[0].stroke_length);
            $("#types").val(data.datas[0].type);  
          }
          else if(og_unit=="SI"&&ig_unit=="API")
          {
            $('#stroke_length').val((data.datas[0].stroke_length*25.4).toFixed());
            $("#types").val(data.datas[0].type);  
          }
          else if(og_unit=="API"&&ig_unit=="SI")
          {

            $('#stroke_length').val((data.datas[0].stroke_length/25.4).toFixed());
            $("#types").val(data.datas[0].type);  
          }
          $('.linearsize').html('');
          $('.pressure').html('');
          if(data.current_unit=="API"&&og_unit=="API"){
            $('.linearsize').append('<th class="label">Liner Size(in)</th>');
            $('.pressure').append('<th class="label">Max Discharge Pressure(psi)</th>');
            $('.flowrateth').html($('.flowrateth').html().replace($('.flowrateth').text(),'Flowrate(GPM)'));

          }
          else{
          $('.linearsize').append('<th class="label">Liner Size(mm)</th>');
          $('.pressure').append('<th class="label">Max Discharge Pressure(MPa)</th>');
          $('.flowrateth').html($('.flowrateth').html().replace($('.flowrateth').text(),'Flowrate(LPM)'));
          }
          
          data.datas[0].mud_pump_data.forEach(function (arrayItem) {
            if(og_unit==ig_unit)
            {
              linear_sizedisp= arrayItem.linear_size;
              max_discharge_pressuredisp= arrayItem.max_discharge_pressure;

            }
            else if(og_unit=="SI"&&ig_unit=="API")
            {
              linear_sizedisp= (arrayItem.linear_size*25.4).toFixed(2);
              max_discharge_pressuredisp= (arrayItem.max_discharge_pressure/0.000145038/1000000).toFixed(2);
              
            }
            else if(og_unit=="API"&&ig_unit=="SI")
            {
              linear_sizedisp= (arrayItem.linear_size/25.4).toFixed(2);
              max_discharge_pressuredisp= (arrayItem.max_discharge_pressure*0.000145038*1000000).toFixed(2);
            }
         
              $('.linearsize').append('<td><input type="number" step="any" class="form-control linear_size" name="linear_size" value="'+linear_sizedisp+'" ><span class="linersize_error"></span></td>');
              $('.pressure').append('<td><input type="number" step="any" class="form-control" name="max_discharge_pressure" value="'+max_discharge_pressuredisp+'" ><span class="max_discharge_error"></span></td>');
        });
        box='';
        $('.flowrate').remove();

        data.datas[0].mud_pump_master_speed.forEach(function (arrayItem) {

          var box='<tr class="flowrate"><th><input type="number" class="form-control pump_speed" name="pump_speed" value="'+arrayItem.pump_speed+'"><span class="pump_speed_error"></span></th>'
          arrayItem.mud_pump_flowrate.forEach(function (flow) {
            if(og_unit==ig_unit)
            {
              flowratedisp=flow.flowrate;
            }
            else if(og_unit=="API"&&ig_unit=="SI")
            {
              flowratedisp=(flow.flowrate/3.7854117839).toFixed(2);
            }
            else if(og_unit=="SI"&&ig_unit=="API")
            {
              flowratedisp=(flow.flowrate*3.7854117839).toFixed(2);
            }
            box+='<td><input type="number" step="any" class="form-control" name="flowrate"  value="'+flowratedisp+'"><span class="flowrate_error"></span></td>';
          });
          box+='</tr>';
          $('.mudpumptable').append(box);

        });

      }
    });

// all field only numeric
  

$(document.body).on('keyup','.numeric',function(){
  var $this = $(this);
  $this.val($this.val().replace(/[^\d.]/g, ''));        
});  


// $(document.body).on('blur', '#casing_size ', function(obj) {
//   var current=$(this).closest('tr');
//   var col = current.find('#hole_size').val();
//   var col2 = current.find('#casing_size').val();
//   if (col <= col2) {
//     alert("Hole size is greater then casing size");
//     var col2 = current.find('#casing_size').val("");
//   }
//  /* var col3 = $(this).closest("tr").index();
//   var col4 = $('#wellphasesaddtable > tr:gt("col3")').find('#hole_size').val();
//   //var col4 = $(this).closest('tr').prev("tr[id^='hole_size']").text();
//   alert(col4);*/

// });
$(document.body).on('blur', '#true_vertical_depth ', function(obj) {
  var current=$(this).closest('tr');
  var md=current.find('#measured_depth').val();
  var tvd=current.find('#true_vertical_depth').val();
  if (md <  tvd){
    alert("MD is grater are equel to TVD");
    var tvd=current.find('#true_vertical_depth').val("");
  }
});
});


// Delete Conformation
function confirmation(ev)  {
  ev.preventDefault();
  var value= ev.currentTarget.getAttribute('href');       
  Swal.fire({
    title: 'Are you sure?',
    text: "You won't be able to revert this!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, delete it!'
  }).then((result ) => {
    if (result.value) {
      console.log(value)
      window.location.href=value
    }
    
  })
}

// ADD Well Conformation
function allwell(ev)  {
  var project_id = $('.prj-list-side').find('.project-list.active').attr('project_data');
  var blocks=$('.prj-list-side').find('.block-list.active').attr('block_data');
  var fields=$('.prj-list-side').find('.field-list.active').attr('field_data');
  ev.preventDefault();
  var value= ev.currentTarget.getAttribute('href'); 
  Swal.fire({
    title: 'Do you want to create a well?', 
    showCancelButton: true,
    confirmButtonText: `Create`,
}).then((result) => {
if (result.isConfirmed) {
        localStorage.setItem('block', blocks);
        localStorage.setItem('field', fields);
        window.location.href=value;
      } else if (result.isDenied) {
        Swal.fire('Changes are not saved', '', 'info')
    }
})
}


function getplanwells(project_id,csrf)  {
  var csrf =$('.getcsrf').val();
  $.ajax({
    type: "GET",
    url:"/wells/create/getplanwells",
    contentType: 'application/json',  
    data: {'plan_well_list_id':project_id},
    dataType: "json",
    beforeSend: function(xhr){
      xhr.setRequestHeader('X-CSRFToken', csrf);
    },
    success: function(data) {
      // console.log(data);
      $('#plan_well_list').empty();
      $('#plan_well_list')
      .append($("<option></option>")
      .attr("value", '')
      .text("-- Plan Well List --")); 
  $.each(JSON.parse(data), function(key, value) {   
$('#plan_well_list').append($("<option></option>")
              .attr("value", value.pk)
              .text(value.fields.name)); 
            });
  }
});
}


// $(document).on("keyup",".linear_size",function() {  
//   var liner_size_ele = $(this).val();
//   var main_index=$(this).parent().index();
//   flowratecalculation(liner_size_ele,main_index)
// });


// $(document).on("keyup",".stroke_length",function() {
//   $('.linear_size').each(function(){
//     var liner_size_ele = $(this).val();
//     var main_index=$(this).parent().index();
//     flowratecalculation(liner_size_ele,main_index)
//   });
//   var liner_size_ele = $(this).val();
//   var main_index=$(this).parent().index();
//   flowratecalculation(liner_size_ele,main_index)
// });


// $(document).on("keyup",".roddiameter",function() {
//   $('.linear_size').each(function(){
//     var liner_size_ele = $(this).val();
//     var main_index=$(this).parent().index();
//     flowratecalculation(liner_size_ele,main_index)
//   });
//   var liner_size_ele = $(this).val();
//   var main_index=$(this).parent().index();
//   flowratecalculation(liner_size_ele,main_index)
// });


// $(document).on("keyup",".pump_speed",function() {  
//   $('.linear_size').each(function(){
//     var liner_size_ele = $(this).val();
//     var main_index=$(this).parent().index();
//     flowratecalculation(liner_size_ele,main_index)
//   });
// });


// function flowratecalculation(liner_size_ele,main_index){
//  $('.mudpumptable tr.flowrate').each(function(){
//   var csrf =$('[name="csrfmiddlewaretoken"]').val();
//   var curren_ele = $(this)
//   var pump_speed_ele = $(this).find("th:eq(0) input[name='pump_speed']").val();
//   var pumptypes_ele =$('#types').val() || $('#pump_type').val();
//   var pump_unit = $('#unit').val();
//   $.ajax({
//     type: "GET",
//     url:"/wells/mud/flowratecalculation",
//     contentType: 'application/json',  
//     data: {
//       'linear_size' : liner_size_ele,
//       'stroke_length' : $( "#stroke_length").val(),
//       'roddiameter' : $( "#roddiameter").val(),
//       'pump_speed' :  pump_speed_ele,
//       'type' : pumptypes_ele,
//       'unit' : pump_unit
//     },
//     dataType: "json",
//     beforeSend: function(xhr){
//       xhr.setRequestHeader('X-CSRFToken', csrf);
//     },
//     success: function(data) { 
//       console.log(data);
//       curren_ele.find("th:eq("+main_index+") input[name='flowrate']").val(data);
//     }
// });
// });
// }



//Admin Drillcollar
$("#drillcollerstable").on("click",".drillcollersaddrow" , function() {
  $("<tr id='drillcollersrow'>"+ $('#drillcollersrow2').html()+" </tr>").insertAfter($(this).closest('tr'));
  $('#drillcollerstable > tbody > tr:gt(0)').find(".drillcollerremoverows").show();
   
   });
   $("#drillcollerstable").on("click", ".drillcollerremoverows" , function() 
   {   
    var rowCounts = $('#drillcollerstable >tbody >tr').length;
    if(rowCounts<5)
    {
      $('#drillcollerstable > tbody > tr:gt(0)').find(".drillcollerremoverows").hide();
    }   
   var whichtr =$(this).closest("tr");
   whichtr.remove();
  });



  // Drillpipe
  $("#drillpipetable").on("click",".drillpipeaddrow" , function() {
    $("<tr id='drillcollersrow'>"+ $('#drillpiperow2').html()+" </tr>").insertAfter($(this).closest('tr'));
    $('#drillpipetable > tbody > tr:gt(0)').find(".drillpiperemoverows").show();
     });
     $("#drillpipetable").on("click", ".drillpiperemoverows" , function() {   
      var rowCounts = $('#drillpipetable >tbody >tr').length;
      if(rowCounts<5)
      {
        $('#drillpipetable > tbody > tr:gt(0)').find(".drillpiperemoverows").hide();
      }   
     var whichtr =$(this).closest("tr");
     whichtr.remove();
    });




// Drillpipe HWDP
$("#drillHWDPtable").on("click",".drillHWDPaddrow" , function() {
$("<tr id='drillHWDProw'>"+ $('#drillHWDProw2').html()+" </tr>").insertAfter($(this).closest('tr'));
$('#drillHWDPtable > tbody > tr:gt(0)').find(".drillHWDPremoverows").show();
  
  });
  $("#drillHWDPtable").on("click", ".drillHWDPremoverows" , function() 
  {   
  var rowCounts = $('#drillHWDPtable >tbody >tr').length;
  if(rowCounts<5)
  {
    $('#drillHWDPtable > tbody > tr:gt(0)').find(".drillHWDPremoverows").hide();
  }   
  var whichtr =$(this).closest("tr");
  whichtr.remove();
});

// Type Dropdown change
var parentRow;
// $(document).on("change", ".type_name" , function() {
//   var types=$(this).val();
//   $(".od").click(function(){
//     parentRow = $(this).closest('tr'); 
//     $('input[type="radio"]').prop('checked', false); 
//     if( types == 'Drill Collar')
//     {
//       $('.myModal123').modal('show');
//     }
//     else if( types == 'Drill Pipe')
//     {
//       $('.drillpipebha').modal('show');
//     }
//     else if( types == 'Heavy Weight Drill Pipe')
//     {
//       $('.drillpipehwdp').modal('show');
//     }
   
//   });
  
// });
var closesttrindex;
var indexid
$(document).on("click",".od",function(){
  var type_name = $(this).closest('tr').find('.type_name').val(); 
  closesttrindex=$(this).closest('tr').index();
  indexid=$(this).attr('dataid')
  $('input[type="radio"]').prop('checked', false); 
  if( type_name == 'Drill Collar')
  {
    $('.myModal1234').modal('show');
  }
  else if( type_name == 'Drill Pipe')
  {
    $('.drillpipebha').modal('show');
  }
  else if( type_name == 'Heavy Weight Drill Pipe')
  {
    $('.drillpipehwdp').modal('show');
  }
 
});
$(document).on("click","#modal-close",function(){
  $('.myModal1234').modal('hide');
  $('.drillpipebha').modal('hide');
  $('.drillpipehwdp').modal('hide');
  
  $('.nominal_od_val li.active').removeClass('active');
  $('.weight_val li.active').removeClass('active');
  $('.pipetype_val li.active').removeClass('active');
  $('.connectiontype_val li.active').removeClass('active');
  $('.tool_od_val li.active').removeClass('active');
  $('.one_joint_length').val('');

  $('.drillpipe_nod li.active').removeClass('active');
  $('.drillpipe_weight li.active').removeClass('active');
  $('.drillpipe_grade li.active').removeClass('active');
  $('.drillpipe_jointtype li.active').removeClass('active');
  $('.drillpipe_jointod li.active').removeClass('active');
  $('.drillpipe_class li.active').removeClass('active');
  $('.drillpipe_onejoint_length').val('');

  $('.hwdp_nod li.active').removeClass('active');
  $('.hwdp_weight li.active').removeClass('active');
  $('.hwdp_jointtype li.active').removeClass('active');
  $('.hwdp_jointod li.active').removeClass('active');
  $('.hwdp_class li.active').removeClass('active');
  $('.hwdp_one_joint_length').val('');

});

// POPUP 
$(document).ready(function() {
// Drill Colors Radio select
var normal_od;
var normal_id;
var weight;
$(document).on("change", ".drillcoll" , function() {
  normal_od = $(this).attr("data-id");
  normal_id = $(this).val();
  parentRow.find('.od').val(normal_od);
  parentRow.find('.identity').val();  
  $('.drillcollers .form-check').remove();
  $('.myModal1234').modal('hide');
});
$(document).on("change", ".drillweight" , function() {
  weight=$(this).attr("data-id");
  $('.coll_weight').modal('hide');
});
$(".rss_button").hide();
$(".mudmotor_button").hide();
$(document).on("change", ".type_name" , function() {
  var closestindex;
  closestindex=$(this).closest('tr').index();
  if(well_type=='PLAN'){
    if(($(this).val()=='RSS')||($(this).val()=='LWD')||($(this).val()=='MWD')||($(this).val()=='Others')){
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".rss_button").show();
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".mudmotor_button").hide();
    }
    else if($(this).val()=='Mud Motor'){
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".mudmotor_button").show();
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".rss_button").hide();
    }
    else{
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".rss_button").hide();
      $('#bhadatatable tbody tr:eq('+closestindex+')').find(".mudmotor_button").hide();
    }
  }
  else{
    var dataid=$(this).attr('dataid')
    if(($(this).val()=='RSS')||($(this).val()=='LWD')||($(this).val()=='MWD')||($(this).val()=='Others')){
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".rss_button").show();
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".mudmotor_button").hide();
    }
    else if($(this).val()=='Mud Motor'){
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".mudmotor_button").show();
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".rss_button").hide();
    }
    else{
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".rss_button").hide();
      $('#bhadatatable'+dataid+' tbody tr:eq('+closestindex+')').find(".mudmotor_button").hide();
    }
  }

  });
});
var closestindex
$(document).on("click",".rss_button",function(){
  var index=$(this).closest('tr').index();
  if(well_type=='PLAN'){
    var type_name=$(this).closest('tr').find('#type_name').val();
    var od=$(this).closest('tr').find('.od').val();
    var id=$(this).closest('tr').find('.identity').val();
    var length=$(this).closest('tr').find('.length').val();
    var unit=$('.unit').val();
    modalid=type_name+index
    var checkmodalexist=$('#'+modalid).length
    closestindex=index-1;
    if(checkmodalexist==0){
    $(".modal-backdrop").show();
    var html = '';
      html +='<div class="modal" id='+modalid+'>'
      html +='<div class="modal-dialog">'
      html +='<div class="modal-content">'
      html +='<div class="modal-header">'
      html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations7</h4>'
      html +='</div>'
      html += '<h2 style="text-align: center;">'+type_name+'</h2>'
      html +='<div class="modal-body">'
      html +='<div class="table-responsive formgroup_b0">'
      html +='<div class="row">'
      html +='<div class="col-6">'
      html +='<h3 style="text-align: center;">Specifications</h3>'
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+closestindex+'" placeholder="Name" value='+type_name+'></div></div></div>';
      if (unit =='API'){
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(in)</label></div><div class="col"><input type="text" id="specification_od'+closestindex+'" class="form-control" name="specification_od'+closestindex+'" placeholder="OD" value='+od+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(in)</label></div><div class="col"><input type="text" id="specification_id'+closestindex+'" class="form-control" name="specification_id'+closestindex+'" placeholder="ID" value='+id+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(ft)</label></div><div class="col"><input type="text" id="specification_length'+closestindex+'" class="form-control" name="specification_length'+closestindex+'" placeholder="Length" value='+length+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate"></div></div></div>';
      }
      else{
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(mm)</label></div><div class="col"><input type="text" id="specification_od'+closestindex+'" class="form-control" name="specification_od'+closestindex+'" placeholder="OD" value='+od+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(mm)</label></div><div class="col"><input type="text" id="specification_id'+closestindex+'" class="form-control" name="specification_id'+closestindex+'" placeholder="ID" value='+id+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(m)</label></div><div class="col"><input type="text" id="specification_length'+closestindex+'" class="form-control" name="specification_length'+closestindex+'" placeholder="Length" value='+length+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate (LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate"></div></div></div>';
      }
      html += '</div>'
      html += '<div  class="col-6">'
      html += '<h3 style="text-align: center;">Pressure Drop across Tool</h3>'
      html += '<ul class="nav nav-tabs" role="tablist">'
      html += '<li class="nav-item">'
      html += '<a class="nav-link active" onclick="test(1)" data-toggle="tab" href="#flowrate_tab'+closestindex+'" role="tab" aria-selected="true">Flow Test</a>'
      html += '</li>'
      html += '<li class="nav-item">'
      html += '<a class="nav-link" onclick="test(2)" data-toggle="tab" href="#empirical_tab'+closestindex+'" role="tab">Empirical</a>'
      html += '</li>'
      html += '</ul>'
      html += '<div class="tab-content">'
      html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
      html += '<table class="table flowratetable" id="flowratetable">'
      if (unit =='API'){
        html += '<thead><tr><th>Flowrate(GPM)</th><th>Pressure Drop(psi)</th><th>Action</th></tr></thead>'
      }
      else{
        html += '<thead><tr><th>Flowrate(LPM)</th><th>Pressure Drop(kPa)</th><th>Action</th></tr></thead>'
      }
      html += '<tbody><tr id="flowraterow">'
      html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate"></td>'
      html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop"></td>'
      html += '<td><button type="button" name="add" class="addflowtestrows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr>'
      html += '<tr id="flowraterow2" style="display:none">'
      html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate"></td>'
      html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop"></td>'
      html += '<td><button type="button" name="add" class="addflowtestrows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr></tbody>'
      html +='</table>'
      html += '</div>'
      html += '<div class="tab-pane empirical_tab fade show" id=empirical_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
      html += '<h4>Variables</h4>'
      html += '<ul class="parameters_list">'
      html +='<li class="parameters">Mud Weight</li>'
      html +='<li class="parameters">Flowrate</li>'
      html +='<li class="parameters">Inner Diameter</li>'
      // html +='<li class="parameters">Constant</li>'
      html +='</ul>'

      html += '<h4>Operators</h4>'
      html += '<ul class="parameters_list">'
      html +='<li class="parameters">+</li>'
      html +='<li class="parameters">-</li>'
      html +='<li class="parameters">*</li>'
      html +='<li class="parameters">/</li>'
      html +='<li class="parameters">Power</li>'
      html +='<li class="parameters">Square</li>'
      html +='<li class="parameters">Cube</li>'
      html +='<li class="parameters">Square Root</li>'
      html +='<li class="parameters">Cube Root</li>'
      html +='</ul>'
      // html +='<div id=formula'+closestindex+' contenteditable="true" style="width: 400px;height: 100px;background-color: #0302020f;"></div>
      html +='<input type="hidden" name=formulatests id=formulatexts>'
      html +='<input type="hidden" name=formulatext'+closestindex+' id=formulatext'+closestindex+'><input type="hidden" id=formula_python_text'+closestindex+' name=formula_python_text'+closestindex+'>'
      html +='<textarea id="text_formula'+closestindex+'" class="form-control text_formula" value="" data-role="tagsinput" ></textarea>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      
      html += '<div class="modal-footer"><button type="button" class="btn btn-danger rss-close" data-id='+closestindex+' data-modal='+modalid+' data-dismiss="rss_inputs" id="modalclose" >Close</button></div> '
      html += '</div>'
      html += '</div>'
      html +='</div>'
      $('#flowratemodal').append(html);
      $('#flowratemodal').show();

      $('#'+modalid).modal('show');
    }else{
      $(".modal-backdrop").show();
      $('#flowratemodal').show();
      $('#'+modalid).modal('show');
    }
  }
  else{
    var dataid=$(this).attr('dataid')
    var type_name=$(this).closest('tr').find('#type_name').val();
    var od=$(this).closest('tr').find('.od').val();
    var id=$(this).closest('tr').find('.identity').val();
    var length=$(this).closest('tr').find('.actual_length').val();
    var unit=$('.unit').val();
    modalid=type_name+dataid+'_'+index
    var checkmodalexist=$('#'+modalid).length
    if(checkmodalexist==0){
      $(".modal-backdrop").show();
      var html = '';
      html +='<div class="modal" id='+modalid+'>'
      html +='<div class="modal-dialog">'
      html +='<div class="modal-content">'
      html +='<div class="modal-header">'
      html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations8</h4>'
      html +='</div>'
      html += '<h2 style="text-align: center;">'+type_name+'</h2>'
      html +='<div class="modal-body">'
      html +='<div class="table-responsive formgroup_b0">'
      html +='<div class="row">'
      html +='<div class="col-6">'
      html +='<h3 style="text-align: center;">Specifications</h3>'
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+dataid+'_'+index+'" placeholder="Name" value='+type_name+'></div></div></div>';
      if (unit =='API'){
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(in)</label></div><div class="col"><input type="text" id="specification_od'+dataid+'_'+index+'" class="form-control" name="specification_od'+dataid+'_'+index+'" placeholder="OD" value='+od+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(in)</label></div><div class="col"><input type="text" id="specification_id'+dataid+'_'+index+'" class="form-control" name="specification_id'+dataid+'_'+index+'" placeholder="ID" value='+id+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(ft)</label></div><div class="col"><input type="text" id="specification_length'+dataid+'_'+index+'" class="form-control" name="specification_length'+dataid+'_'+index+'" placeholder="Length" value='+length+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate"></div></div></div>';
      }
      else{
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(mm)</label></div><div class="col"><input type="text" id="specification_od'+dataid+'_'+index+'" class="form-control" name="specification_od'+dataid+'_'+index+'" placeholder="OD" value='+od+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(mm)</label></div><div class="col"><input type="text" id="specification_id'+dataid+'_'+index+'" class="form-control" name="specification_id'+dataid+'_'+index+'" placeholder="ID" value='+id+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(m)</label></div><div class="col"><input type="text" id="specification_length'+dataid+'_'+index+'" class="form-control" name="specification_length'+dataid+'_'+index+'" placeholder="Length" value='+length+'></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate (LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate"></div></div></div>';
      }
      html += '</div>'
      html += '<div  class="col-6">'
      html += '<h3 style="text-align: center;">Pressure Drop across Tool</h3>'
      html += '<ul class="nav nav-tabs" role="tablist">'
      html += '<li class="nav-item">'
      html += '<a class="nav-link active" onclick="test(1)" data-toggle="tab" href="#flowrate_tab'+dataid+'_'+index+'" role="tab" aria-selected="true">Flow Test</a>'
      html += '</li>'
      html += '<li class="nav-item">'
      html += '<a class="nav-link" onclick="test(2)" data-toggle="tab" href="#empirical_tab'+dataid+'_'+index+'" role="tab">Empirical</a>'
      html += '</li>'
      html += '</ul>'
      html += '<div class="tab-content">'
      html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+dataid+'_'+index+' role="tabpanel" aria-labelledby="home-tab">'
      html += '<table class="table flowratetable" id="flowratetable">'
      if (unit =='API'){
        html += '<thead><tr><th>Flowrate(GPM)</th><th>Pressure Drop(psi)</th><th>Action</th></tr></thead>'
      }
      else{
        html += '<thead><tr><th>Flowrate(LPM)</th><th>Pressure Drop(kPa)</th><th>Action</th></tr></thead>'
      }
      html += '<tbody><tr id="flowraterow">'
      html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+dataid+'_'+index+'" placeholder="Flowrate"></td>'
      html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'_'+index+'" placeholder="Pressure Drop"></td>'
      html += '<td><button type="button" name="add" class="addflowtestrows iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr>'
      html += '<tr id="flowraterow2" style="display:none">'
      html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+dataid+'_'+index+'" placeholder="Flowrate"></td>'
      html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'_'+index+'" placeholder="Pressure Drop"></td>'
      html += '<td><button type="button" name="add" class="addflowtestrows iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr></tbody>'
      html +='</table>'
      html += '</div>'
      html += '<div class="tab-pane empirical_tab fade show" id=empirical_tab'+dataid+'_'+index+' role="tabpanel" aria-labelledby="home-tab">'
      html += '<h4>Variables</h4>'
      html += '<ul class="parameters_list">'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Mud Weight</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Flowrate</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Inner Diameter</li>'
      html +='</ul>'
  
      html += '<h4>Operators</h4>'
      html += '<ul class="parameters_list">'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>+</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>-</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>*</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>/</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Power</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Square</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Cube</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Square Root</li>'
      html +='<li class="parameters" dataid='+dataid+'_'+index+'>Cube Root</li>'
      html +='</ul>'

      html +='<input type="hidden" name=formulatests id=formulatexts>'
      html +='<input type="hidden" name=formulatext'+dataid+'_'+index+' id=formulatext'+dataid+'_'+index+'><input type="hidden" id=formula_python_text'+dataid+'_'+index+' name=formula_python_text'+dataid+'_'+index+'>'
      html +='<textarea id="text_formula'+dataid+'_'+index+'" class="form-control text_formula" data-role="tagsinput" ></textarea>'

  
      html += '</div>'
      html += '</div>'
  
      html += '</div>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      
      html += '<div class="modal-footer"><button type="button" class="btn btn-danger rss-close" data-id='+dataid+'_'+index+' data-modal='+modalid+' data-dismiss="rss_inputs" id="modalclose" >Close</button></div> '
      html += '</div>'
      html += '</div>'
      html +='</div>'
      $('#flowratemodal').append(html);
      $('#flowratemodal').show();
  
      $('#'+modalid).modal('show');
    }else{
      $(".modal-backdrop").show();
      $('#flowratemodal').show();
      $('#'+modalid).modal('show');
    }
  }
  


});
function test(val){
  var calculate_type=val;
  $('.calculation_type').val(calculate_type);
 } 

$(document).on("click",".mudmotor_button",function(){
  var index=$(this).closest('tr').index();
  if(well_type=='PLAN'){
    var type_name=$(this).closest('tr').find('#type_name').val();
  var od=$(this).closest('tr').find('.od').val();
  var id=$(this).closest('tr').find('.identity').val();
  var length=$(this).closest('tr').find('.length').val();
  var unit=$('.unit').val();
  modalid='mud_motor'+index
  var checkmodalexist=$('#'+modalid).length
  closestindex=index-1;
    var html = '';
    html +='<div class="modal" id='+modalid+'>'
    html +='<div class="modal-dialog">'
    html +='<div class="modal-content">'
    html +='<div class="modal-header">'
    html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations9</h4>'
    html +='</div>'
    html += '<h2 style="text-align: center;">'+type_name+'</h2>'
    html +='<div class="modal-body">'
    html +='<div class="row">'
    html +='<div class="col-6">'
    html +='<h3 style="text-align: center;">Specifications</h3>'
    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+closestindex+'" placeholder="Name" value="'+type_name+'"></div></div></div>';
    if(unit == 'API'){
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate (GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM (rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+closestindex+'" placeholder="Maximum RPM"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM (rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+closestindex+'" placeholder="Minimum RPM"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(psi) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+closestindex+'" placeholder="No load diff_pressure"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(psi)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+closestindex+'" placeholder="maximun DP"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(psi)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+closestindex+'" placeholder="Recom DP"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB(lbf)</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+closestindex+'" placeholder="Max WOB"></div></div></div>';
    }else{
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+closestindex+'" placeholder="Maximum RPM"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+closestindex+'" placeholder="Minimum RPM"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(kPa) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+closestindex+'" placeholder="No load diff_pressure"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(kPa)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+closestindex+'" placeholder="maximun DP"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(kPa)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+closestindex+'" placeholder="Recom DP"></div></div></div>';
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+closestindex+'" placeholder="Max WOB"></div></div></div>';
    }
    html += '</div>'
    html += '<div class="tab-content">'
    html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
    html +='<h3 style="text-align: center;">Differential Pressure Table</h3>'
    html += '<table class="table diff_pressure_table" id="diff_pressure_table">'
    html += '<thead><tr><th>Torque</th><th>Differential Pressure</th><th>Action</th></tr></thead>'
    html += '<tbody><tr id="pressure_row">'
    html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" placeholder="Torque"></td>'
    html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" placeholder="Differential Pressure"></td>'
    html += '<td><button type="button" name="add" class="addpressurerows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
    html += '</tr>'
    html += '<tr id="pressure_row2" style="display:none">'
    html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" placeholder="Torque"></td>'
    html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" placeholder="Differential Pressure"></td>'
    html += '<td><button type="button" name="add" class="addpressurerows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
    html += '</tr></tbody>'
    html +='</table>'
    html += '</div>'
    html += '</div>'
    html += '</div>'
    html += '</div>'
    
    html += '<div class="modal-footer"><button type="button" class="btn btn-danger" data-modal='+modalid+' data-dismiss="mudmotor_input" id="modal-mud_motor-close" >Close</button></div> '
    html += '</div>'
    html +='</div>'
    html +='</div>'
    html +='</div>'
    $('#mud_motor').append(html);
    $('#mud_motor').show();
    $('#'+modalid).modal('show');
  }else{
    var dataid=$(this).attr('dataid')
    var type_name=$(this).closest('tr').find('#type_name').val();
    var od=$(this).closest('tr').find('.od').val();
    var id=$(this).closest('tr').find('.identity').val();
    var length=$(this).closest('tr').find('.length').val();
    var unit=$('.unit').val();
    modalid='mud_motor'+dataid+'_'+index
    var checkmodalexist=$('#'+modalid).length
    closestindex=index-1;
      var html = '';
      html +='<div class="modal" id='+modalid+'>'
      html +='<div class="modal-dialog">'
      html +='<div class="modal-content">'
      html +='<div class="modal-header">'
      html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations10</h4>'
      html +='</div>'
      html += '<h2 style="text-align: center;">'+type_name+'</h2>'
      html +='<div class="modal-body">'
      html +='<div class="row">'
      html +='<div class="col-6">'
      html +='<h3 style="text-align: center;">Specifications</h3>'
      html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+dataid+'_'+index+'" placeholder="Name" value="'+type_name+'"></div></div></div>';
      if(unit == 'API'){
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate (GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM (rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+dataid+'_'+index+'" placeholder="Maximum RPM"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM (rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+dataid+'_'+index+'" placeholder="Minimum RPM"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(psi) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+dataid+'_'+index+'" placeholder="No load diff_pressure"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(psi)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+dataid+'_'+index+'" placeholder="maximun DP"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(psi)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+dataid+'_'+index+'" placeholder="Recom DP"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB(lbf)</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+dataid+'_'+index+'" placeholder="Max WOB"></div></div></div>';
      }else{
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+dataid+'_'+index+'" placeholder="Maximum RPM"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+dataid+'_'+index+'" placeholder="Minimum RPM"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(kPa) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+dataid+'_'+index+'" placeholder="No load diff_pressure"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(kPa)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+dataid+'_'+index+'" placeholder="maximun DP"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(kPa)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+dataid+'_'+index+'" placeholder="Recom DP"></div></div></div>';
        html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+dataid+'_'+index+'" placeholder="Max WOB"></div></div></div>';
      }
      html += '</div>'
      html += '<div class="tab-content">'
      html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
      html +='<h3 style="text-align: center;">Differential Pressure Table</h3>'
      html += '<table class="table diff_pressure_table" id="diff_pressure_table">'
      html += '<thead><tr><th>Torque</th><th>Differential Pressure</th><th>Action</th></tr></thead>'
      html += '<tbody><tr id="pressure_row">'
      html += '<td><input type="hidden" name="differntial_pressure'+dataid+'_'+index+'"><input type="text" id=" torque" class="form-control torque" name="torque'+dataid+'_'+index+'" placeholder="Torque"></td>'
      html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+dataid+'_'+index+'" placeholder="Differential Pressure"></td>'
      html += '<td><button type="button" name="add" class="addpressurerows iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr>'
      html += '<tr id="pressure_row2" style="display:none">'
      html += '<td><input type="hidden" name="differntial_pressure'+dataid+'_'+index+'"><input type="text" id=" torque" class="form-control torque" name="torque'+dataid+'_'+index+'" placeholder="Torque"></td>'
      html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+dataid+'_'+index+'" placeholder="Differential Pressure"></td>'
      html += '<td><button type="button" name="add" class="addpressurerows iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
      html += '</tr></tbody>'
      html +='</table>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      html += '</div>'
      
      html += '<div class="modal-footer"><button type="button" class="btn btn-danger" data-modal='+modalid+' data-dismiss="mudmotor_input" id="modal-mud_motor-close" >Close</button></div> '
      html += '</div>'
      html +='</div>'
      html +='</div>'
      html +='</div>'
      $('#mud_motor').append(html);
      $('#mud_motor').show();
      $('#'+modalid).modal('show');
  }
  
})

$('body').on('click', '#modal-mud_motor-close' ,function(){
  var modal=$(this).attr('data-modal');
  $('#'+modal).modal('hide');
});

$('body').on('click', '#modalclose' ,function(){
  alert(well_type)
  if(well_type=='PLAN'){
    var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();
    var cumulative_total=0;
    var index=$(this).attr('data-id');
    var modal=$(this).attr('data-modal');
    var od=$('#specification_od'+index).val()
    alert(od)
    var id=$('#specification_id'+index).val()
    var length=$('#specification_length'+index).val()
    alert(length)

    var trindex=parseInt(index)+1
    var formula=$('#formulatext'+index).val()
    var pressure_drop=$('#pressure_drop').val();
    if(formula == '' && pressure_drop==''){
      alert('Flowtest and Empirical are empty!');
    }
  
  
    $('.length').each(function(index){

      if($(this).val()!='' && index<trindex-1){
        cumulative_total =cumulative_total+parseFloat($(this).val());
      }
    });
    console.log(cumulative_total)
  
    cumulative_total=parseFloat(cumulative_total)+parseFloat(length)
  
    var remaining=total_measured_depth-cumulative_total;
  
  
    if(parseFloat(cumulative_total)<total_measured_depth){
      $('#bhadatatable tbody tr:eq('+trindex+')').find('.cumulative-length').val(cumulative_total.toFixed(2))
      var newindex=parseInt(trindex)+1;
      $('#bhadatatable tbody tr:eq('+newindex+')').find('.length').val(remaining);
      $('#bhadatatable tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
    
    }else{
      $(this).closest('tr').find('.cumulative-length').val(total_measured_depth);
      $(this).val('')
    }
  
    $('#bhadatatable tbody tr:eq('+trindex+')').find('.od').val(od)
    $('#bhadatatable tbody tr:eq('+trindex+')').find('.identity').val(id)
    $('#bhadatatable tbody tr:eq('+trindex+')').find('.length').val(length)
  
    if(formula!=''){
      if(formula.search("flowrate")!=-1){
        $("#flowratemodal").hide();
        $('#'+modal).modal('hide');
        if($('.modal-backdrop.show').length > 0){
          $(".modal-backdrop").remove();
      
          $("body").removeClass("modal-open");
        }
      }else{
        alert("formula must contain flowrate")
      }
    }
    else{
      $('#'+modal).modal('hide');
    
    }
  }
  else{
    // alert(indexid)
    var dataid=$(this).attr('data-id')
    // alert(dataid)
    var dataid_split=dataid.split("_");
    var total_measured_depth=$('#bhadatatable'+dataid_split[0]+' tbody tr:eq(0)').find('.measured_depth').val();
    var modal=$(this).attr('data-modal');
    var cumulative_total=0;
    var od=$('#specification_od'+dataid).val()
    var id=$('#specification_id'+dataid).val()
    var length=$('#specification_length'+dataid).val()
    var formula=$('#formulatext'+dataid).val()
    var pressure_drop=$('#pressure_drop').val();
    var cumulative_total=0;
    console.log(dataid_split[1])

    $('#bhadatatable'+dataid_split[0]+' tbody tr').each(function(index,tr){
      if($(tr).find('td input.actual_length').val()!=undefined && $(tr).find('td input.actual_length').val()!='' && index<dataid_split[1]){
        console.log(typeof(index))
        if(index<=parseInt(dataid_split[1])){
          console.log($(tr).find('td input.actual_length').val())
          cumulative_total =cumulative_total+parseFloat($(tr).find('td input.actual_length').val());
        }
      }
    });
    console.log(length)
    console.log(cumulative_total)

    cumulative_total=parseFloat(cumulative_total)+parseFloat(length)
    cumulative_total=cumulative_total.toFixed(2)
    console.log(cumulative_total)
  
    var remaining=total_measured_depth-cumulative_total;

    if(parseFloat(cumulative_total)<total_measured_depth){
      $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+dataid_split[1]+')').find('.cumulative-length').val(cumulative_total)
      var newindex=parseInt(dataid_split[1])+1;
      $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+newindex+')').find('.actual_length').val(remaining);
      $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
    
    }else{
      $(this).closest('tr').find('.cumulative-length').val(total_measured_depth);
      $(this).val('')
    }

    $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+dataid_split[1]+')').find('.od').val(od)
    $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+dataid_split[1]+')').find('.identity').val(id)
    $('#bhadatatable'+dataid_split[0]+' tbody tr:eq('+dataid_split[1]+')').find('.actual_length').val(length)

    if(formula!=''){
      if(formula.search("flowrate")!=-1){
        $("#flowratemodal").hide();
        $('#'+modal).modal('hide');
        if($('.modal-backdrop.show').length > 0){
          $(".modal-backdrop").remove();
      
          $("body").removeClass("modal-open");
        }
      }else{
        alert("formula must contain flowrate")
      }
    }
    else{
      $('#'+modal).modal('hide');
    
    }
  


  }

});
$(document).ready(function(){        
  var tagInputEle = $('#tags-input');
  tagInputEle.tagsinput();
});
$(document).on("click",".addflowtestrows" , function() {
  if(well_type=='PLAN'){
    var html="";
    html +='<tr id="flowraterow">'
    html +='<td><input type="text" id="florate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate"></td>'
    html +='<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop"></td>'
    html +='<td><button type="button" name="add" class="addflowtestrows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
    html +="</tr>"
    $(this).closest('tr').after(html);
    $('#flowratetable > tbody > tr:gt(0)').find(".deleteflowtestrow").show();
  }else{
    var dataid=$(this).attr('dataid')
    var html="";
    html +='<tr id="flowraterow">'
    html +='<td><input type="text" id="florate" class="form-control flowrate" name="flowrate'+dataid+'" placeholder="Flowrate"></td>'
    html +='<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'" placeholder="Pressure Drop"></td>'
    html +='<td><button type="button" name="add" class="addflowtestrows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
    html +="</tr>"
    $(this).closest('tr').after(html);
    $('#flowratetable > tbody > tr:gt(0)').find(".deleteflowtestrow").show();
  }

});
$(document).on("click", ".deleteflowtestrow" , function(){   
  var rowCounts = $('#flowratetable >tbody >tr').length;
  if(rowCounts<2)
  {
    $('#flowratetable > tbody > tr:gt(0)').find(".deleteflowtestrow").hide();
  }   
var whichtr =$(this).closest("tr");
whichtr.remove();
});
$(document).on("click",".addpressurerows" , function() {
  if(well_type=='PLAN'){
    var html="";
    html +='<tr id="flowraterow">'
    html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" placeholder="Torque"></td>'
    html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" placeholder="Differential Pressure"></td>'
    html +='<td><button type="button" name="add" class="addpressurerows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
    html +="</tr>"
    $(this).closest('tr').after(html);
    $('#diff_pressure_table > tbody > tr:gt(0)').find(".deletepressurerows").show();
  }else{
    var dataid=$(this).attr('dataid')
    var html="";
    html +='<tr id="flowraterow">'
    html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+dataid+'" placeholder="Torque"></td>'
    html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+dataid+'" placeholder="Differential Pressure"></td>'
    html +='<td><button type="button" name="add" class="addpressurerows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows iconaction"><i class="fa fa-trash"></i></button></td>'
    html +="</tr>"
    $(this).closest('tr').after(html);
    $('#diff_pressure_table > tbody > tr:gt(0)').find(".deletepressurerows").show();
  }

});
$(document).on("click", ".deletepressurerows" , function(){   
  var rowCounts = $('#diff_pressure_table >tbody >tr').length;
  if(rowCounts<2)
  {
    $('#diff_pressure_table > tbody > tr:gt(0)').find(".deletepressurerows").hide();
  }   
var whichtr =$(this).closest("tr");
whichtr.remove();
});
var previous_operator
allvalues = [];
var previous_index
$('body').on('click','.parameters',function(){
  var parameter_name=$(this).text();
  if(previous_index!=closestindex){
    allvalues = [];
  }
  var parameter_list = {"Mud Weight": "mudweight", "Flowrate": "flowrate", "Inner Diameter": "ID","+":"+",'-':"-","*":"*",'/':"/"};
  if(well_type=='PLAN'){
    
    var currenttext=$('#formula'+closestindex).html();
    var currenttext_format= $('#formulatext'+closestindex).val()
    var formula_python_text= $('#formula_python_text'+closestindex).val()
    if(parameter_name=="Constant"){
      $( '<input type="text" name="constant_value" id="constant_value">').insertAfter($(this));
      previous_operator=parameter_name
    }
    else if(parameter_name=="Power"){
          $( '<input type="text" name="power_value" id="power_value">').insertAfter($(this));
    }
    else if(parameter_name=="Square"){
      var newformula=currenttext+"<sup>2</sup>"
      var tagInputEle = $('#text_formula'+closestindex)
      tagInputEle.tagsinput('add','²');
      var test= $('.empirical_label'+closestindex+' .label' ).text();
      $('#formulatexts').append('²');
      $('#formula'+closestindex).html(newformula)
      var newcurrenttext_format=currenttext_format+"<sup>2</sup>"
      var newformula_python_text=formula_python_text+'**2'
      allvalues.push('²');
      $('#formulatext'+closestindex).val(allvalues)
      $('#formula_python_text'+closestindex).val(test)
      previous_operator=parameter_name   
    }
    else if(parameter_name=="Cube"){
      var newformula=currenttext+"<sup>3</sup>"
      var test= $('.empirical_label'+closestindex+' .label' ).text();
      
      $('#formula'+closestindex).html(newformula)
      var newcurrenttext_format=currenttext_format+"<sup>3</sup>"
      allvalues.push('³');
      $('#formulatext'+closestindex).val(allvalues)
      var newformula_python_text=formula_python_text+'**3'
      $('#formula_python_text'+closestindex).val(test)
      previous_operator=parameter_name
      var tagInputEle =$('#text_formula'+closestindex) 
      tagInputEle.tagsinput('add','³');
      $('#formulatexts').append('³');
    }else if(parameter_name=="Square Root"){
      if(currenttext==''){
        $('#formula'+closestindex).html("<b>&#8730</b>")
        $('#formulatext'+closestindex).val("<b>&#8730</b>")
  
      }else{
          var newformula=currenttext+"<b>&#8730</b>"
          $('#formula'+closestindex).html(newformula)
          var newcurrenttext_format=currenttext_format+"<b>&#8730</b>"
          $('#formulatext'+closestindex).val(newcurrenttext_format)
          var newformula_python_text=formula_python_text+"sqrt"
          $('#formula_python_text'+closestindex).val(newformula_python_text)          
      }
      previous_operator=parameter_name
      var tagInputEle = $('#text_formula'+closestindex) 
      tagInputEle.tagsinput('add','√');
      var test= $('.empirical_label'+closestindex+' .label' ).text();
      $('#formulatexts').append('√');
    }
    else if(parameter_name=="Cube Root"){
      if(currenttext==''){
        $('#formula'+closestindex).html("<b>&#8731</b>")
  
      }else{
          var newformula=currenttext+"<b>&#8731</b>"
          $('#formula'+closestindex).html(newformula)
          var newcurrenttext_format=currenttext_format+"<b>&#8731</b>"
          $('#formulatext'+closestindex).val(newcurrenttext_format)  
      }
      previous_operator=parameter_name
      var tagInputEle = $('#text_formula'+closestindex)
      tagInputEle.tagsinput('add','∛');
      var test= $('.empirical_label'+closestindex+' .label' ).text();
      $('#formulatexts').append('∛');
    }
    else{
      if(currenttext==''){
          var symbol=parameter_list[parameter_name]
          $('#formula'+closestindex).html(symbol)
          var newcurrenttext_format=symbol
          $('#formulatext'+closestindex).val(newcurrenttext_format)
          var newformula_python_text=symbol
          $('#formula_python_text'+closestindex).val(newformula_python_text)
  
      }else{     
          var symbol=parameter_list[parameter_name]
          var newformula=currenttext+symbol
          $('#formula'+closestindex).html(newformula)
          if(previous_operator=='Square Root'){
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+"("+symbol+")"
            var tagInputEle = $('#text_formula'+closestindex)
            tagInputEle.tagsinput('add',symbol);
          }
          else if(previous_operator=='Cube Root'){
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+symbol+"**(1/3)"
            var tagInputEle = $('#text_formula'+closestindex)
            tagInputEle.tagsinput('add',symbol);
          }else{
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+symbol
            var tagInputEle = $('#text_formula'+closestindex)
             tagInputEle.tagsinput('add',symbol);
          }
          var tagInputEle = $('#text_formula'+closestindex)
          tagInputEle.tagsinput('add',symbol);
          allvalues.push(symbol);
          var test= $('.empirical_label'+closestindex+' .label' ).text();
          console.log(test)
          $('#formulatext'+closestindex).val(allvalues)
          $('#formula_python_text'+closestindex).val(test)
          $('#formulatexts').append(symbol);
        }
        console.log(allvalues);
        previous_operator=parameter_name
      }
      $('.bootstrap-tagsinput input').addClass('bootstrap_test');
      $(".bootstrap-tagsinput input").prop("type", "number");
      $(this).closest('div').find('.bootstrap-tagsinput').addClass('empirical_label'+closestindex+'');

      $('.bootstrap_test').on('blur',function(){
        var test= $('.empirical_label'+closestindex+' .label' ).text();
        $('#formulatext'+closestindex).val(allvalues)
        $('#formula_python_text'+closestindex).val(test)
    })
    previous_index=closestindex

  }
  else{
    var dataid=$(this).attr('dataid')
    var currenttext=$('#formula'+dataid).html();
    var currenttext_format= $('#formulatext'+dataid).val()
    var formula_python_text= $('#formula_python_text'+dataid).val()
    var tagInputEle = $('#text_formula'+dataid)

    if(parameter_name=="Constant"){
      $( '<input type="text" name="constant_value" id="constant_value">').insertAfter($(this));
      previous_operator=parameter_name
    }
    else if(parameter_name=="Power"){
          $( '<input type="text" name="power_value" id="power_value">').insertAfter($(this));
    }


    else if(parameter_name=="Square"){
      var newformula=currenttext+"<sup>2</sup>"
      tagInputEle.tagsinput('add','²');
      var test= $('.empirical_label'+dataid+' .label' ).text();
      $('#formula'+dataid).html(newformula)
      allvalues.push('²');
      $('#formulatext'+dataid).val(allvalues)
      $('#formula_python_text'+dataid).val(test)
      previous_operator=parameter_name

    }
    else if(parameter_name=="Cube"){
      var newformula=currenttext+"<sup>3</sup>"
      var test= $('.empirical_label'+dataid+' .label' ).text();
      $('#formula'+dataid).html(newformula)
      allvalues.push('³');
      $('#formulatext'+dataid).val(allvalues)
      $('#formula_python_text'+dataid).val(test)
      previous_operator=parameter_name
  
    }else if(parameter_name=="Square Root"){
      if(currenttext==''){
        $('#formula'+dataid).html("<b>&#8730</b>")
        $('#formulatext'+dataid).val("<b>&#8730</b>")
  
      }else{
          var newformula=currenttext+"<b>&#8730</b>"
          $('#formula'+dataid).html(newformula)
          var newcurrenttext_format=currenttext_format+"<b>&#8730</b>"
          $('#formulatext'+dataid).val(newcurrenttext_format)
          var newformula_python_text=formula_python_text+"sqrt"
          $('#formula_python_text'+dataid).val(newformula_python_text)
      }
      previous_operator=parameter_name
    }
    else if(parameter_name=="Cube Root"){
      if(currenttext==''){
        $('#formula'+dataid).html("<b>&#8731</b>")
  
      }else{
          var newformula=currenttext+"<b>&#8731</b>"
          $('#formula'+dataid).html(newformula)
          var newcurrenttext_format=currenttext_format+"<b>&#8731</b>"
          $('#formulatext'+dataid).val(newcurrenttext_format)
  
  
      }
      previous_operator=parameter_name
      tagInputEle.tagsinput('add','∛');
  
    }
    else{
      if(currenttext==''){
          var symbol=parameter_list[parameter_name]
          $('#formula'+dataid).html(symbol)
          var newcurrenttext_format=symbol
          $('#formulatext'+dataid).val(newcurrenttext_format)
          var newformula_python_text=symbol
          $('#formula_python_text'+dataid).val(newformula_python_text)
  
      }else{
          var symbol=parameter_list[parameter_name]
          var newformula=currenttext+symbol
          $('#formula'+dataid).html(newformula)
          if(previous_operator=='Square Root'){
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+"("+symbol+")"
            tagInputEle.tagsinput('add',symbol);
          }
          else if(previous_operator=='Cube Root'){
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+symbol+"**(1/3)"
            tagInputEle.tagsinput('add',symbol);
          }else{
            var newcurrenttext_format=currenttext_format+symbol
            var newformula_python_text=formula_python_text+symbol
            tagInputEle.tagsinput('add',symbol);
          }
          tagInputEle.tagsinput('add',symbol);
          allvalues.push(symbol);
          var test= $('.empirical_label'+dataid+' .label' ).text();


          $('#formulatext'+dataid).val(allvalues)
          $('#formula_python_text'+dataid).val(test)  
      }
      previous_operator=parameter_name
    }
    $('.bootstrap-tagsinput input').addClass('bootstrap_test');
    $(".bootstrap-tagsinput input").prop("type", "number");
    $(this).closest('div').find('.bootstrap-tagsinput').addClass('empirical_label'+dataid+'');

    $('.bootstrap_test').on('blur',function(){
        var test= $('.empirical_label'+dataid+' .label' ).text();
        $('#formulatext'+dataid).val(allvalues)
        $('#formula_python_text'+dataid).val(test)
    })

  }


})
$('body').on('blur', '#constant_value', function () {
  var currenttext=$('#formula'+closestindex).html();
  var currenttext_format= $('#formulatext'+closestindex).val()
  var formula_python_text= $('#formula_python_text'+closestindex).val()
  if(currenttext==''){
    $('#formula'+closestindex).html($(this).val())
    $('#formulatext'+closestindex).val($(this).val())

  }else{
      var newformula=currenttext+$(this).val()
      $('#formula'+closestindex).html(newformula)
      var newcurrenttext_format=currenttext_format+$(this).val()
      $('#formulatext'+closestindex).val(newcurrenttext_format)
      var newformula_python_text=formula_python_text+$(this).val()
      $('#formula_python_text'+closestindex).val(newformula_python_text)
  }
  $('#constant_value').remove() 

});
$('body').on('blur', '#power_value', function () {
  var operators_array={"+":"+",'-':"-","*":"*",'/':"/"};
  var currenttext=$('#formula'+closestindex).html();
  var currenttext_format= $('#formulatext'+closestindex).val()
  var formula_python_text= $('#formula_python_text'+closestindex).val()
  for (var key in operators_array) {
    index=formula_python_text.lastIndexOf(operators_array[key]);
    if(index!=-1){
      formula_python_text=formula_python_text.substring(0,index+1)

    }
  }
  var newformula=currenttext+"<sup>"+$(this).val()+"</sup>"
  $('#formula'+closestindex).html(newformula)
  var newcurrenttext_format=currenttext_format+"<sup>"+$(this).val()+"</sup>"
  $('#formulatext'+closestindex).val(newcurrenttext_format)
  var newformula_python_text=formula_python_text+"pow("+previous_operator+","+$(this).val()+")"
  $('#formula_python_text'+closestindex).val(newformula_python_text)
  var tagInputEle = $('#text_formula'); 
  var power_var=$(this).val();
  var tes=power_var.sup();
  document.getElementById('text_formula').innerHTML=tes;
  tagInputEle.tagsinput('add','<sup>'+$(this).val()+'</sup>');
  var test= $('.label').text();
  $('#formulatexts').append('<sup>'+$(this).val()+'</sup>');

  $('#power_value').remove() 
})



// $("#formula").droppable({
//   accept: '.parameters_list li',
//   drop: function(ev, ui) {
//   alert(ui.helper.text())
//   var currenttext=$('#formula').html();
//   if(ui.helper.text()=="Constant"){
//       $('#formula').focus()
//       $('#constant').append('<input type="text" name="contant_value" id="contant_value">')

//   }else if(ui.helper.text()=="Power"){
//       $('#formula').focus()
//       $('#power').append('<input type="text" name="power_value" id="power_value">')
//   }
//   else if(ui.helper.text()=="Square"){
//       $('#formula').append('<sup>2</sup>')
//   }
//   else if(ui.helper.text()=="Cube"){
//       $('#formula').append('<sup>3</sup>')
//   }else if(ui.helper.text()=="Square Root"){
//       $('#formula').append("<b>&#8730</b>")  
//   }
//   else if(ui.helper.text()=="Cube Root"){
//       $('#formula').append("<b>&#8731</b>")   
//   }
//   else{
//       if(currenttext==''){
//           var symbol=myArray[ui.helper.text()]
//           $('#formula').html(symbol)
//       }else{
//           var symbol=myArray[ui.helper.text()]
//           $('#formula').append(symbol)

//       }
//   }
//   }
// });


// $("#nod").change(function () { 
//  var ind = $(this).val();
// //  $('#od').val(ind);
//  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(ind);
//  var cloesttr_index=$(this).closest('tr').index(); 
//   var drillcoll = $(this).find(':selected').attr('databasevalue');
//   var current_element=$(this);
//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/bhacaluculation",                    
//     data: {
//       drillcoll:drillcoll
//     },
//     dataType: "json",
//     success: function (data) { 
//       $(".weight1 option").remove(); 
//       $('.weight1').append('<option value="">Weight</option>'); 
// for(i=0;i<data.data.length;i++){
//   //console.log(data.data[i].weight);
// $('.weight1').append('<option value="'+data.data[i].weight +'">'+ data.data[i].weight+'</option>');
//      }
//      $('.weight1').select2('open');
//   }

//   });
// });


//// test
var well_type=$('#well_type').val()









//new drill pipe
$(".drillpipe_class li").hide(); 










//new hwdp 
$(".hwdp_class li").hide(); 
$(document.body).on("click",".hwdp_nod > li",function () { 
  $(this).addClass('active').siblings().removeClass('active');
  var normal_od=$(this).attr('databasevalue');
  var well_id = $('#well').val();
   $.ajax({ 
     type: "GET",                      
     url: "/wells/bhadata/getweight_hwdpnod",                    
     data: {
      normal_od:normal_od,
      well_id:well_id
     },
     dataType: "json",
     success: function (data) {
       $(".hwdp_weight li").remove();
       $('#hwdp_weight_head').show();
       for(i=0;i<data.data.length;i++){
         $('.hwdp_weight').append('<li databasevalue ="'+data.data[i].databasevalue+'" hwdp_weight="'+data.data[i].weight +'">'+ data.data[i].weight+'</li>');
       }
       $(".hwdp_jointtype li").hide(); 
       $(".hwdp_jointod li").hide(); 
       $(".hwdp_class li").hide();
       $(".hwdp_one_joint_length").hide(); 
       $('#hwdp_type_head').hide();
     }
 
   });
 });
 $(document.body).on("click",".hwdp_weight > li",function () { 
  $(this).addClass('active').siblings().removeClass('active');
  var hwdp_weight_val = $(this).attr('hwdp_weight');  
  var hwdp_weight = $(this).attr('databasevalue'); 
  if(well_type=='PLAN'){
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(hwdp_weight);
  }else{
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(hwdp_weight);
  }
  var normal_od=$('ul.hwdp_nod').find('li.active').attr('databasevalue');
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getjointtype_hwdp",                    
    data: {
      hwdp_weight:hwdp_weight,
      normal_od:normal_od
    },
    dataType: "json",
    success: function (data) { 
      $(".hwdp_jointtype li").remove(); 
      $('#hwdp_type_head').show();
      for(i=0;i<data.data.length;i++){
        $('.hwdp_jointtype').append('<li hwdp_jointtype="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</li>');
     }
     $(".hwdp_jointod li").hide(); 
       $(".hwdp_class li").hide();
       $(".hwdp_one_joint_length").hide();
       $("#hwdp_jointod_head").hide();
       $("#hwdp_class_head").hide();
       $("#hwdp_one_joint_head").hide();
    }
  });
});

$(document.body).on("click",".hwdp_jointtype > li",function () { 
  // alert(indexid)
  $(this).addClass('active').siblings().removeClass('active');
  var hwdp_jointtype = $(this).attr('hwdp_jointtype');
  if(well_type=='PLAN'){
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(hwdp_jointtype);
  }else{
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.connection_type').val(hwdp_jointtype);
  }
  var normal_od=$('ul.hwdp_nod').find('li.active').attr('databasevalue');
  var nod=$('ul.hwdp_nod').find('li.active').attr('hwdp_nominal');
  var hwdp_weight=$('ul.hwdp_weight').find('li.active').attr('databasevalue');
  var well_id=$('#well').val();
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getjointod_hwdp",                    
    data: {
      hwdp_jointtype:hwdp_jointtype,
      normal_od:normal_od,
      hwdp_weight:hwdp_weight,
      well_id:well_id,
      nod:nod
    },
    dataType: "json",
    success: function (data) { 
      if(well_type=='PLAN'){
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.tool_id.data);
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od').val(normal_od);
        $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id.data);
      }else{
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.identity').val(data.tool_id.data);
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.database_od').val(normal_od);
        $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id.data);
      }

      $(".hwdp_jointod li").remove(); 
      $("#hwdp_jointod_head").show();
      for(i=0;i<data.data.length;i++){
      $('.hwdp_jointod').append('<li hwdp_jointod="'+data.data[i][0].data+'">'+data.data[i][0].data+'</li>');
    }
    $(".hwdp_class li").hide();
       $(".hwdp_one_joint_length").hide();
       $("#hwdp_class_head").hide();
       $("#hwdp_one_joint_head").hide();
  }
  });
});

$(document.body).on("click",".hwdp_jointod > li",function () { 
  $(this).addClass('active').siblings().removeClass('active');
  var hwdp_jointod = $(this).attr('hwdp_jointod');
  if(well_type=='PLAN'){
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(hwdp_jointod);
  }else{
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.tool_od').val(hwdp_jointod);
  }
  var hwdp_jointtype = $('ul.hwdp_jointtype').find('li.active').attr('hwdp_jointtype'); 
  var normal_od=$('ul.hwdp_nod').find('li.active').attr('databasevalue');
  var hwdp_weight=$('ul.hwdp_weight').find('li.active').attr('databasevalue');
  $(".hwdp_class li").removeClass('active');
  $("#hwdp_class_head").show();
  $(".hwdp_class li").show();
  $("#hwdp_one_joint_head").hide();
  $('.hwdp_one_joint_length').hide(); 
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getclass_hwdp",                    
    data: {
      hwdp_jointod:hwdp_jointod,
      normal_od:normal_od,
      hwdp_jointtype:hwdp_jointtype,
      hwdp_weight:hwdp_weight
    },
    dataType: "json",
    success: function (data) { 
      $(".hwdp_class li").remove(); 
      for(i=0;i<data.data.length;i++){
        $('.hwdp_class').append('<li value="'+data.data[i].class_type +'">'+ data.data[i].class_type+'</li>');
      }
      $(".hwdp_one_joint_length").hide();
    }
  });
});
$(document.body).on("click",".hwdp_class > li",function () { 
  $(this).addClass('active').siblings().removeClass('active');
  $('#hwdp_one_joint_head').show();
  var classtype=$(this).attr('value');
  if(well_type=='PLAN'){
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
  }else{
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
  }
  $('.hwdp_one_joint_length').show();
});

//call when drillpipe nod change
// $("#drillpipe_nod").change(function () { 
//  var normal_od=$(this).find(':selected').attr('databasevalue');
//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/getweight_drillpipe",                    
//     data: {
//       normal_od:normal_od
//     },
//     dataType: "json",
//     success: function (data) { 
//       $(".drillpipe_weight option").remove();
//       $('.drillpipe_weight').append('<option value="">Weight</option>');
//       for(i=0;i<data.data.length;i++){
//         $('.drillpipe_weight').append('<option value="'+data.data[i].weight +'">'+ data.data[i].weight+'</option>');
//       }
//       $('.drillpipe_weight').select2('open');
//     }

//   });
// });

$("#hwdp_nod").change(function () { 
  var normal_od=$(this).find(':selected').attr('databasevalue');
   $.ajax({ 
     type: "GET",                      
     url: "/wells/bhadata/getweight_hwdpnod",                    
     data: {
      normal_od:normal_od
     },
     dataType: "json",
     success: function (data) { 
       $(".hwdp_weight option").remove();
       $('.hwdp_weight').append('<option value="">Weight</option>');
       for(i=0;i<data.data.length;i++){
         $('.hwdp_weight').append('<option value="'+data.data[i].weight +'">'+ data.data[i].weight+'</option>');
       }
       $('.hwdp_weight').select2('open');
     }
 
   });
 });

//  $('.weight1').change(function(){
// $("#weight").val($(this).val());
// });


$("#weight1").change(function () { 
   var collar_weight = $(this).val();  
   $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(collar_weight);
   $.ajax({ 
     type: "GET",                      
     url: "/wells/bhadata/bha_pipe_calc",                    
     data: {
      collar_weight:collar_weight
     },
     dataType: "json",
     success: function (data) {   
      $(".pipe_type1 option").remove(); 
      $('.pipe_type1').append('<option value="">Type</option>');
      for(i=0;i<data.data.length;i++){
        $('.pipe_type1').append('<option value="'+data.data[i].pipe_type +'">'+ data.data[i].pipe_type+'</option>');
      }
      $('.pipe_type1').select2('open');
   }
 
   });
 });
 $("#drillpipe_weight").change(function () { 
  var drillpipe_weight = $(this).val();  
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(drillpipe_weight);
  var normal_od=$('.drillpipe_nod').find(':selected').attr('databasevalue');
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getgrade_drillpipe",                    
    data: {
      drillpipe_weight:drillpipe_weight,
      normal_od:normal_od
    },
    dataType: "json",
    success: function (data) { 
      $(".drillpipe_grade option").remove(); 
      $('.drillpipe_grade').append('<option value="">Grade</option>');
      for(i=0;i<data.data.length;i++){
        $('.drillpipe_grade').append('<option value="'+data.data[i].steel_grade +'">'+ data.data[i].steel_grade+'</option>');
     }
     $('.drillpipe_grade').select2('open');
    }
  });
});
// $("#hwdp_weight").change(function () { 
//   var hwdp_weight = $(this).val();  
//   $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(hwdp_weight);
//   var normal_od=$('.hwdp_nod').find(':selected').attr('databasevalue');
//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/getjointtype_hwdp",                    
//     data: {
//       hwdp_weight:hwdp_weight,
//       normal_od:normal_od
//     },
//     dataType: "json",
//     success: function (data) { 
//       $(".hwdp_jointtype option").remove(); 
//       $('.hwdp_jointtype').append('<option value="">Type</option>');
//       for(i=0;i<data.data.length;i++){
//         $('.hwdp_jointtype').append('<option value="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</option>');
//      }
//      $('.hwdp_jointtype').select2('open');
//     }
//   });
// });
$(".one_joint_length").keyup(function () { 
  var onejointlength=$(this).val();
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val(onejointlength);
});
var welltype=$('#well_type').val()




// $("#drillpipe_grade").change(function () { 
//   var drillpipe_grade = $(this).val();  
//   $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.grade').val(drillpipe_grade);
//   var normal_od=$('.drillpipe_nod').find(':selected').attr('databasevalue');
//   var drillpipe_weight=$(this).closest('tr').find('.drillpipe_weight').val();

//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/getjointtype_drillpipe",                    
//     data: {
//       drillpipe_weight:drillpipe_weight,
//       normal_od:normal_od,
//       drillpipe_grade:drillpipe_grade
//     },
//     dataType: "json",
//     success: function (data) { 
//       $(".drillpipe_jointtype option").remove(); 
//       $('.drillpipe_jointtype').append('<option value="">Type</option>');
//       for(i=0;i<data.data.length;i++){
//         $('.drillpipe_jointtype').append('<option value="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</option>');
//      }
//      $('.drillpipe_jointtype').select2('open');
//     }
//   });
// });
// $("#drillpipe_jointtype").change(function () { 
//   var drillpipe_jointtype = $(this).val();  
//   $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(drillpipe_jointtype);
//   var normal_od=$('.drillpipe_nod').find(':selected').attr('databasevalue');
//   var nod=$(this).closest('tr').find('.drillpipe_nod').val();
//   var drillpipe_weight=$(this).closest('tr').find('.drillpipe_weight').val();
//   var drillpipe_grade=$(this).closest('tr').find('.drillpipe_grade').val();
//   var well_id=$('#well').val();
//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/getjointod_drillpipe",                    
//     data: {
//       drillpipe_weight:drillpipe_weight,
//       normal_od:normal_od,
//       drillpipe_grade:drillpipe_grade,
//       drillpipe_jointtype:drillpipe_jointtype,
//       well_id:well_id,
//       nod:nod,
//     },
//     dataType: "json",
//     success: function (data) { 
//       $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.data[0][0].pipebody_id);
//       $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
//       $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id);
//       $(".drillpipe_jointod option").remove(); 
//       $('.drillpipe_jointod').append('<option value="">OD</option>');
//       for(i=0;i<data.data.length;i++){
//       $('.drillpipe_jointod').append('<option value="'+data.data[i][1].data+'">'+ data.data[i][1].data+'</option>');
//       }
//       $('.drillpipe_jointod').select2('open'); 
//     }
//   });
// });

$("#hwdp_jointtype").change(function () { 
  var hwdp_jointtype = $(this).val();  
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(hwdp_jointtype);
  var normal_od=$('.hwdp_nod').find(':selected').attr('databasevalue');
  var nod=$(this).closest('tr').find('.hwdp_nod').val();
  var hwdp_weight=$(this).closest('tr').find('.hwdp_weight').val();
  var well_id=$('#well').val();
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getjointod_hwdp",                    
    data: {
      hwdp_jointtype:hwdp_jointtype,
      normal_od:normal_od,
      hwdp_weight:hwdp_weight,
      well_id:well_id,
      nod:nod
    },
    dataType: "json",
    success: function (data) { 
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.data[0][1].tool_id);
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id);
      $(".hwdp_jointod option").remove(); 
      $('.hwdp_jointod').append('<option value="">OD</option>');
      for(i=0;i<data.data.length;i++){
      $('.hwdp_jointod').append('<option value="'+data.data[i][0].data+'">'+data.data[i][0].data+'</option>');
    }
    $('.hwdp_jointod').select2('open');
  }
  });
});

// $("#drillpipe_jointod").change(function () { 
//   var drillpipe_jointod = $(this).val();  
//   $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(drillpipe_jointod);
//   var normal_od=$('.drillpipe_nod').find(':selected').attr('databasevalue');
//   var drillpipe_weight=$(this).closest('tr').find('.drillpipe_weight').val();
//   var drillpipe_grade=$(this).closest('tr').find('.drillpipe_grade').val();
//   var drillpipe_jointtype=$(this).closest('tr').find('.drillpipe_jointtype').val();
//   $('.drillpipe_class').select2('open'); //default know
//   $.ajax({ 
//     type: "GET",                      
//     url: "/wells/bhadata/getclass_drillpipe",                    
//     data: {
//       drillpipe_weight:drillpipe_weight,
//       normal_od:normal_od,
//       drillpipe_grade:drillpipe_grade,
//       drillpipe_jointtype:drillpipe_jointtype,
//       drillpipe_jointod:drillpipe_jointod
//     },
//     dataType: "json",
//     success: function (data) { 
//       $(".drillpipe_class option").remove(); 
//       $('.drillpipe_class').append('<option value="">Class</option>');
//       for(i=0;i<data.data.length;i++){
//         $('.drillpipe_class').append('<option value="'+data.data[i].class_type +'">'+ data.data[i].class_type+'</option>');
//       }
//     }
//   });
// });

$("#drillpipe_class").change(function () { 
  var classtype=$(this).val();
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
});


$("#hwdp_class").change(function () { 
  var classtype=$(this).val();
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
});

$("#hwdp_jointod").change(function () { 
  var hwdp_jointod = $(this).val(); 
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(hwdp_jointod);
  var hwdp_jointtype = $(this).closest('tr').find('.hwdp_jointtype').val(); 
  var normal_od=$('.hwdp_nod').find(':selected').attr('databasevalue');
  var hwdp_weight=$(this).closest('tr').find('.hwdp_weight').val();
  $('.hwdp_class').select2('open'); //Default know
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/getclass_hwdp",                    
    data: {
      hwdp_jointod:hwdp_jointod,
      normal_od:normal_od,
      hwdp_jointtype:hwdp_jointtype,
      hwdp_weight:hwdp_weight
    },
    dataType: "json",
    success: function (data) { 
      $(".hwdp_class option").remove(); 
      $('.hwdp_class').append('<option value="">Class</option>');
      for(i=0;i<data.data.length;i++){
        $('.hwdp_class').append('<option value="'+data.data[i].class_type +'">'+ data.data[i].class_type+'</option>');
      }
    }
  });
});


$(document).on("blur",'.length_edit',function(){
  var current_index=$(this).closest('tr').index();
  var current_length=$(this).val();
  var pre_ind=current_index-1;
  var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();
  if(parseFloat(current_length) < total_measured_depth){
  var pre_val=$('#bhadatatable tbody tr:eq('+pre_ind+')').find('.cumulative-length').val();
  var current_len = $(this).closest('tr').find('.length_edit').val();
  var totals=parseFloat(current_len)+parseFloat(pre_val)
  $('#bhadatatable tbody tr:eq('+current_index+')').find('.cumulative-length').val(totals);
  $('.length_edit').each(function(index,val){
    if(index>current_index){
        var pre_index=index-1;
        var total_length=$('#bhadatatable tbody tr:eq('+index+')').find('.length_edit').val();
        var all_cumule=$('#bhadatatable tbody tr:eq('+pre_index+')').find('.cumulative-length').val();
        var cumulative = parseFloat(total_length) +parseFloat(all_cumule);
        if(cumulative <= total_measured_depth){
          $('#bhadatatable tbody tr:eq('+index+')').find('.cumulative-length').val(cumulative);
        }
        else{
          $('#bhadatatable tbody tr:eq('+index+')').find('.cumulative-length').val(total_measured_depth);
          $('#bhadatatable tbody tr:eq('+index+')').find('.length_edit').val(0);
        }
      }
      if(cumulative > total_measured_depth){
        var cum_inx=index;
        var pre_cum_inx=index-1;
        var pre_cumulative=$('#bhadatatable tbody tr:eq('+pre_cum_inx+')').find('.cumulative-length').val();
        var cum_length=total_measured_depth-pre_cumulative;
        $('#bhadatatable tbody tr:eq('+cum_inx+')').find('.length_edit').val(cum_length);
        $('#bhadatatable tbody tr:eq('+cum_inx+')').find('.cumulative-length').val(total_measured_depth);
        
        }
      
    });
  }
  else{
    alert('Length exiting final depth');
    $('#bhadatatable tbody tr:eq('+current_index+')').find('.cumulative-length').val('');
    $('#bhadatatable tbody tr:eq('+current_index+')').find('.length_edit').val('');
  }
});

// $('.pipe_type1').change(function(){
// $("#pipe_type").val($(this).val());
// });


 $("#pipe_type1").change(function () { 
  var pipe_type = $(this).val(); 
  var w_pipe=$(this).closest('tr').find('.weight1').val();
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.pipe_type').val(pipe_type);
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/bha_Connectpipe_calc",                    
    data: {
      pipe_type:pipe_type,
      w_pipe:w_pipe
    },
    dataType: "json",
    success: function (data) { 
      $(".connection_type1 option").remove(); 
    $('.connection_type1').append('<option value="">Connection type</option>');  
for(i=0;i<data.data.length;i++){
$('.connection_type1').append('<option value="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</option>');
     }
     $('.connection_type1').select2('open');
  }

  });
});
// $('.connection_type1').change(function(){
// $("#connection_type").val($(this).val());
// });


$("#connection_type1").change(function () { 
  var conn_type = $(this).val(); 
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(conn_type);
  var w_pipe=$(this).closest('tr').find('.weight1').val();
  var pipe_type=$(this).closest('tr').find('.pipe_type1').val();
  var well_id=$('#well').val();
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/bha_tooljoint_calc",                    
    data: {
      conn_type:conn_type,
      w_pipe:w_pipe,
      pipe_type:pipe_type,
      well_id:well_id
    },
    dataType: "json",
    success: function (data) {
    $(".tool_od1 option").remove(); 
    $('.tool_od1').append('<option value="">Tool OD</option>');
for(i=0;i<data.data.length;i++){
$('.tool_od1').append('<option value="'+data.data[i].data +'">'+ data.data[i].data+'</option>');
     }
     $('.tool_od1').select2('open');
  }

  });
});
// $('.tool_od1').change(function(){
// $("#tool_od").val($(this).val());
// });

$("#tool_od1").change(function () { 
  var tool_od = $(this).val(); 
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(tool_od);
  var w_pipe=$(this).closest('tr').find('.weight1').val();
  var pipe_type=$(this).closest('tr').find('.pipe_type1').val();
  var c_type=$(this).closest('tr').find('.connection_type1').val();
  var nod=$(this).closest('tr').find('.tool_od1').val();
  var well_id=$('#well').val();
  $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/bha_tooljoint_id_calc",                    
    data: {
      tool_od:tool_od,
      w_pipe:w_pipe,
      pipe_type:pipe_type,
      c_type:c_type,
      nod:nod,
      well_id:well_id
    },
    dataType: "json",
    success: function (data) { 
for(i=0;i<data.data.length;i++){
  $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.tool_id);
     } 
  }
  });
});

// Drill Pipe Radio select
var normal_od;
var normal_id;
$(document).on("change", ".drillpipe" , function() {
  normal_od = $(this).attr("data-id");
  normal_id = $(this).val();
  parentRow.find('.od').val(normal_od);
  parentRow.find('.identity').val(normal_id);  
  $('.drillpipebha').modal('hide');
});


// Drill PipeHWDP Radio select
var od;
var id;
$(document).on("change", ".drillpipehwdp1" , function() {  
  od = $(this).attr("data-id");
  id = $(this).val();
  var currenttr_index=$('#trindex').val();
  parentRow.find('.od').val();
  parentRow.find('.identity').val();  
  $('#bhadatatable tbody tr:eq('+currenttr_index+')').find('.od').val(od);
  $('#bhadatatable tbody tr:eq('+currenttr_index+')').find('.identity').val(id);
  $('.drillpipehwdp').modal('hide');
});
 
$(document).on("change", ".type_name" , function() {  
  var trindex=$(this).closest('tr').index();
  $('#trindex').val(trindex);
});

//wellphase casingsize validation
$(document).on("keyup", ".casing_size" , function() {
  casing_size = $(this).val();
  hole_size = $(this).closest('tr').find('.hole_size').val();
  var casing_type=$(this).closest('tr').find('.casing_type').val();
  if(casing_type!=2){
  if(parseInt(hole_size) < parseInt(casing_size)){
    alert("Hole size is greater than Casing size");
    casing_size = $(this).val("");
  }
  }
});

//wellphase holesize validation
$(document).on("keyup", ".hole_size" , function() {
  hole_size = $(this).val();
  casing_size = $(this).closest('tr').find('.casing_size').val();
  if(parseInt(hole_size) < parseInt(casing_size)){
    alert("Hole size is greater than Casing size");
  }
  prev_casing_size=$(this).closest('tr').prev().find('.casing_size').val();
  prev_driftid=$(this).closest('tr').prev().find('.driftid').val();

  if(prev_casing_size)
  {
    if(parseFloat(hole_size) > parseFloat(prev_casing_size)){
      alert("Hole size Must Be less than previous casing size");
      this.value='';
    }
    if(parseFloat(hole_size)>parseFloat(prev_driftid)){
      alert("Hole size Must Be less than previous drift ID");
      this.value='';
    }
  }
});




$(document).on("keyup", ".hole_size" , function() {
cur_ele = $(this).val()
get_holesize = $(this).closest("tr").prev().find(".hole_size").val();
get_pre_casingsize= $(this).closest("tr").prev().find(".casing_size").val();
if(parseInt(cur_ele) > parseInt(get_holesize)){
  alert("Must be small previous Holesize");
  cur_ele = $(this).val("")
}
else if(parseInt(cur_ele) > parseInt(get_pre_casingsize))
{
  alert("Must be small previous Casing Size");
  cur_ele = $(this).val("")
}
});


$(document).on("keyup", ".casing_size" , function() {
  cur_ele = $(this).val()
  get_casingsize= $(this).closest("tr").prev().find(".casing_size").val();
  if(parseInt(cur_ele) > parseInt(get_casingsize)){
    alert("Must be small previous Casingsize");
  }
  });


// $(document).on("blur", ".azimuth" , function() { 
//   var current_azimuth = $(this).val()
//   var cloesttr_index=$(this).closest('tr').index();
//   var prev_inclination = $(this).closest("tr").prev().find(".inclination").val();
//   var prev_azimuth = $(this).closest("tr").prev().find(".azimuth").val();
//   var current_inclination = $(this).closest("tr").find(".inclination").val();
//   var tvd=$(this).closest("tr").prev().find(".true_vertical_depth").val();
//   var current_md=$(this).closest("tr").find(".measured_depth").val();
//   var prev_md = $(this).closest("tr").prev().find(".measured_depth").val();
//   var prev_east = $(this).closest("tr").prev().find(".east").val();
//   var prev_north = $(this).closest("tr").prev().find(".north").val();
//   var surface_easting = $('#surface_easting').val();
//   var surface_northing = $("#surface_northing").val();


//   var current_element=$(this);
//   if(cloesttr_index>1){
//     $.ajax({
//       type: "GET",
//       url:"/wells/welltrajectory/welltrajectorytvdcal",
//       data: {
//         current_azimuth : current_azimuth,
//         prev_inclination : prev_inclination,
//         prev_azimuth : prev_azimuth,
//         current_inclination :  current_inclination,
//         tvd:tvd,
//         current_md:current_md,
//         prev_md:prev_md,
//         prev_east:prev_east,
//         prev_north:prev_north,
//         surface_easting:surface_easting,
//         surface_northing:surface_northing,
//       },
//       success: function(data) { 
//         current_element.closest('tr').find('.true_vertical_depth').val(data.tvd);
//         current_element.closest('tr').find('.dls').val(data.dls);
//         current_element.closest('td').find('.delta_e').val(data.delts_e); 
//         current_element.closest('td').find('.delta_n').val(data.delts_n);
//         current_element.closest('td').find('.east').val(data.east);
//         current_element.closest('td').find('.north').val(data.north);
//         current_element.closest('td').find('.easting').val(data.easting);
//         current_element.closest('td').find('.northing').val(data.northing);
//         current_element.closest('td').find('.vertical_section').val(data.vartical_section);
//         current_element.closest('tr').find('.dl').val(data.dl);
//         current_element.closest('tr').find('.dl_inc').val(data.dl_inc);
//         current_element.closest('tr').find('.dls_inc').val(data.dls_inc);
//         current_element.closest('tr').find('.dl_azi').val(data.dl_azi);
//         current_element.closest('tr').find('.dls_azi').val(data.dls_azi);
//       }
//   });
// }

// });
// $( document ).ready(function() {
//   var tvd_array = $('.tvd').get().map(function(el) { return parseFloat(el.value.trim()) });
//   var pore_pressure_array = $('.pore_pressure').get().map(function(el) { return parseFloat(el.value.trim()) });
//   var fracture_pressure_array = $('.fracture_pressure').get().map(function(el) { return parseFloat(el.value.trim()) });
//   console.log(pore_pressure_array);
//   console.log(fracture_pressure_array);

//   const pore_pressure_list = pore_pressure_array.filter(function (value) {
//     return !Number.isNaN(value);
// });

// const fracture_pressure_list = fracture_pressure_array.filter(function (value) {
//   return !Number.isNaN(value);
// });
// console.log(pore_pressure_array);
// console.log(fracture_pressure_array);
//   if(tvd_array.length>0)
//   {
//     $('.charts').show();
//     chart(tvd_array,pore_pressure_list,fracture_pressure_list)  
//   }
// });

// pore pressure conversion
var pore_pressure=[];
var fracture_pressure=[];
$(document).ready(function(){
  $('.tvd').each(function(index){
    var pore_pressure_val=$(this).closest('tr').find('.pore_pressure').val();
    var fracture_pressure_val=$(this).closest('tr').find('.fracture_pressure').val();
    pore_pressure.push(pore_pressure_val);
    fracture_pressure.push(fracture_pressure_val);
  })

// pore pressure chart ppg,psi,psi/ft conversion
$('.units').click(function(){
  // $(this).css('pointer-events', 'none');
  var unit=$(this).attr('id');
  var tvd_array=[];
  var pore_pressue_array=[];
  var fracture_pressure_array=[];

  //ppg to psi
  if(unit=='psi'){
    $('.charts').show();
    $('.tvd').each(function(index){
      var psi_tvd=$(this).val();
      tvd_array.push(parseFloat(psi_tvd));
      var psi_pore_conv=0.052*pore_pressure[index]* psi_tvd
      var pore_val=psi_pore_conv.toFixed(2);
      pore_pressue_array.push(parseFloat(pore_val));
      //alert(pore_pressue_array);
      $(this).closest('tr').find('.pore_pressures').html(pore_val+'<input type="hidden" class="pore_pressure" value="'+pore_val+'">');
      var psi_fracture_conv=0.052*fracture_pressure[index]* psi_tvd
      var fracture_val=psi_fracture_conv.toFixed(2);
      fracture_pressure_array.push(parseFloat(fracture_val));
     // alert(fracture_pressure_array);
      $(this).closest('tr').find('.fracture_pressures').html(fracture_val+'<input type="hidden" class="fracture_pressures" value="'+fracture_val+'">');
    })
    chart(tvd_array,pore_pressue_array,fracture_pressure_array)
  }
  //ppg to psift
  if(unit=='psift'){
    $('.charts').hide();
    $('.tvd').each(function(index){
      var psi_tvd=$(this).val();
      var psift_pore_conv=0.052*pore_pressure[index]
      var pore_val=psift_pore_conv.toFixed(2);
      $(this).closest('tr').find('.pore_pressures').text(pore_val);
      var psift_fracture_conv=0.052*fracture_pressure[index]
      var fracture_val=psift_fracture_conv.toFixed(2);
      $(this).closest('tr').find('.fracture_pressures').text(fracture_val);
    })
  }

  //psi to ppg
  if(unit=='ppg'){
    $('.charts').show();
    $('.tvd').each(function(index){
      var ppg_tvd=$(this).val();
      tvd_array.push(parseFloat(ppg_tvd));
      pore_pressue_array.push(parseFloat(pore_pressure[index]));
      fracture_pressure_array.push(parseFloat(fracture_pressure[index]));
      $(this).closest('tr').find('.pore_pressures').text(pore_pressure[index]);
      $(this).closest('tr').find('.fracture_pressures').text(fracture_pressure[index]);
    })
    chart(data1,data2)
  }
  
  // //psi to psift
  // if(unit=='psift'){
  //   $('.tvd').each(function(index){
  //     var psift_tvd=$(this).val();
  //     var pore_pressure_val=$(this).closest('tr').find('.pore_pressure').val();
  //     var fracture_pressure_val=$(this).closest('tr').find('.fracture_pressure').val();
  //     var ppg_pore_conv=pore_pressure_val/psift_tvd
  //     console.log(ppg_pore_conv)
  //     var ppg_fracture_conv=fracture_pressure_val/psift_tvd
  //     console.log(ppg_fracture_conv)
  //   })
  // }
  // //psift to ppg
  // if(unit=='ppg'){
  //   $('.tvd').each(function(index){
  //     var ppg_tvd=$(this).val();
  //     var pore_pressure_val=$(this).closest('tr').find('.pore_pressure').val();
  //     var fracture_pressure_val=$(this).closest('tr').find('.fracture_pressure').val();
  //     var ppg_pore_conv=pore_pressure_val/0.052
  //     $(this).closest('tr').find('.pore_pressures').text(ppg_pore_conv);
  //     var ppg_fracture_conv=fracture_pressure_val/0.052
  //     $(this).closest('tr').find('.pore_pressures').text(ppg_fracture_conv);
  //   })
    
  // }
  // //psift to psi
  // if(unit=='psi'){
  //   $('.tvd').each(function(index){
  //     var psift_tvd=$(this).val();
  //     var pore_pressure_val=$(this).closest('tr').find('.pore_pressure').val();
  //     var fracture_pressure_val=$(this).closest('tr').find('.fracture_pressure').val();
  //     var ppg_pore_conv=pore_pressure_val/psift_tvd
  //     console.log(ppg_pore_conv)
  //     var ppg_fracture_conv=fracture_pressure_val/psift_tvd
  //     console.log(ppg_fracture_conv)
  //   })
  // }
})
});
var t_line=[];
get_line_intersection = function(p0,p1,p2,p3)
{   
    var p0_x = p0.x;
    var p0_y = p0.y;
    var p1_x = p1.x;
    var p1_y = p1.y;
    var p2_x = p2.x;
    var p2_y = p2.y;
    var p3_x = p3.x;
    var p3_y = p3.y;  

    var s1_x, s1_y, s2_x, s2_y;
    s1_x = p1_x - p0_x;     s1_y = p1_y - p0_y;
    s2_x = p3_x - p2_x;     s2_y = p3_y - p2_y;

    var s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y);
    var t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y);
    if (s >= 0 && s <= 1 && t >= 0 && t <= 1)
    {
      line_intercet=[p0_x + (t * s1_x),p0_y + (t * s1_y)];
      // console.log(line_intercet);
      
        line=line_intercet[1];
        t_line.push(line.toFixed(2));
        
        return ([p0_x + (t * s1_x),p0_y + (t * s1_y)]);
    }

    return false;
}
function chart(pore_pressue_array,fracture_pressure_array,muddatachart=''){
  tvdunit=$("#tvdunit").val();
  pressureunit=$("#pressureunit").val();

  Highcharts.chart('pore_pressurecontainer', {

    chart: {
        inverted: true,
    //    marginTop: 25
    },
   title:'Pore Pressure and Frac Pressure',

    yAxis: {
          opposite: true,

        title: {
            text: 'Pressure'+'('+(pressureunit)+')'
        }
    },

    xAxis: {
      labels: {
        format: '{value}'
    },
        tickInterval: 1000,
        accessibility: {
            rangeDescription: 'Range: 2010 to 2017'
        },
        title: {
          text: 'TVD'+(tvdunit)
      }
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        // enabled: false
    },
    colors: [
      '#4572A7', 
      '#DB843D',
      '#20c170',
      'red'
      ],
      plotOptions: {
        series: {
            label: {
                connectorAllowed: true,
                enabled:false
            },
            // pointStart: 2010
        }
    },
     
    series: [{
      // showInLegend: false,
      name: 'Pore pressure'+'('+pressureunit+')',
      data:pore_pressue_array
    }, {
      // showInLegend: false,
      name: 'Fracture pressure'+'('+pressureunit+')',
        data: fracture_pressure_array
    },
    {
      // showInLegend: false,
      name: 'Mud Weight'+'('+pressureunit+')',
        data: muddatachart
    },
    {
      name: 'Intercept',
      data: [],
      // valueDecimals:2,
      tooltip: {
        // y: {
        //   formatter: function (y) {
        //     return  y.toFixed(2) ;
        //   }
        // },
        headerFormat: '<span style="font-size:10px">{series.name}</span><br><table>',
        pointFormat: '<tr><td style="padding:0">TVD: </td>' +
            '<td style="padding:0"><b>{point.y} </b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true,
        
    },
      marker: {
        symbol: 'point',
        // fillColor: 'rgba(0,0,0,0)',
        lineColor: 'red',
        lineWidth: 0.5
      },
      type: 'scatter'
      },
    // {
    //   name: 'intersect',
    //   data: [],
    //   marker: {
    //     radius: 10,
    //     symbol: 'circle',
    //     fillColor: 'rgba(0,0,0,0)',
    //     lineColor: 'red',
    //     lineWidth: 2
    //   },
    //   type: 'scatter'
    //   }
    ],  
    credits: {
      enabled: false
    },
    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

},
function (chart){
  var s0 = chart.series[1].points;
  var s1 = chart.series[2].points;
  var s2 = chart.series[3];
  var n0 = s0.length;
  var n1 = s1.length;
  var i,j,isect;
  for (i = 1; i < n0; i++){
     for (j = 1; j < n1; j++){
         if (isect = get_line_intersection(s0[i-1],s0[i],
                             s1[j-1],s1[j])){
             s2.addPoint(isect, false, false);
             
         }
     } 
  }
  let line = [];
  let d_line=[];
  for(i=0;i<t_line.length;i++){
    d_line.push(t_line[i]);
    line.push({

      name: 'TVD',
      color: 'red',
      value: t_line[i],
      width: 1,
      dashStyle: 'dash'
    })
  }
  //  chart.series[3].data.series.options.update(d_line)
  
    chart.update({

      yAxis:{
        // data=t_line,
        plotLines: line
      }
    
   })
  
  
  chart.redraw();
})
}
//pore pressure and fraction pressure chart
// function chart1(tvd_array,pore_pressue_array,fracture_pressure_array){

//   tvdunit=$("#tvdunit").val();
//   pressureunit=$("#pressureunit").val();

//   Highcharts.chart('pore_pressurecontainer', {  
//     credits: {
//       enabled: false
//       },
//       title: {
//         text: ''
//     },
//       chart: {
//         inverted: true,
//     //    marginTop: 25
//     },
//     yAxis: {
//           crosshair: true,
//     tickInterval: 2,

//       // reversed: false,
//       opposite: true,
//       title: {
//         text: 'Pressure'+'('+pressureunit+')'
//     }

      
//   //    align: 'top',
           
//     },
//     xAxis: {
//       categories:tvd_array,
//               tickAmount: 8,

//       // "labels": {
//       //   "formatter": function () {
//       //       return (this.value * 1)
//       //   }
//     // }, 

//       opposite : false,
//         tickInterval : 0.5, 
//  //     align: 'top',
//       title: {
//         text: 'TVD'
//       },
//         accessibility : {
//             rangeDescription: ''
//         },
//         title: {
//           text: 'TVD'+tvdunit,
//       }
//     },  

//     legend: {
//         layout: 'vertical',
//         align: 'right',
//         verticalAlign: 'middle'
//     },
//     colors: [
//     '#4572A7', 
//     '#DB843D'
//     ],
//     series: [{
//         name: 'Pore pressure'+'('+pressureunit+')',
//         data:pore_pressue_array,
//     },{
//       name: 'Fracture pressure'+'('+pressureunit+')',
//       data:fracture_pressure_array
//     }],       
// });
// }
// function numberWithCommas(num) {
//   var parts = num.toString().split(".");
//   parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
//   return parts.join(".");
// }

//   $("#northing").each(function() {
//     var num = $(this).text();
//     var commaNum = numberWithCommas(num);
//   });
// });
// $('.northing').mask("#,##0.00", {reverse: true});

// $("#northing").keyup(function(e){
//   var nothing=$(this).val();
//   var data=nothing.replace(/(.\d{2})\d*/, "$1").replace(/(\d)(?=(\d{3})+\b)/g, "$1,")
//     $("#northing").val(data);

// });
// $("#easting").keyup(function(e){
//   var easting=$(this).val();
//   var length=easting.length;
//   if(length==3 && e.keyCode!=8){
//     var value=easting+",";
//     $("#easting").val(value);
//   }
// });


$(document).on("change", ".grade" , function() {   
  var selected_option=$(this).val();
  if(selected_option=='others'){
    $(this).closest('td').append('<input type="text" name="others_grade" class="form-control others_grade">')
  }else{
    $('.others_grade').css('display','none');
  }
});
$(document).on("change", ".casing_range" , function() {   
  var selected_option=$(this).val();
  if(selected_option=='others'){
    $(this).closest('td').append('<input type="text" name="others_range" class="form-control others_range">')
  }else{
    $('.others_grade').css('display','none');
  }
});
var others_grade_array=[];
var others_range_array=[];

$(document).on("change", ".mudtype" , function() {   
  var selected_option=$(this).val();
  if(selected_option=='others'){
    $(this).closest('td').append('<input type="text" name="others_mudtype" class="form-control others_mudtype">')
  }else{
    $('.others_mudtype').css('display','none');
  }
});
var closesttrindex;
$(document).on("blur", ".others_mudtype" , function() { 
  closesttrindex=$(this).closest('tr').index();
  others_mudtype=$(this).val();
  var current_element=$(this);
  if(others_mudtype!=''){
  $.ajax({ 
     type: "GET",                      
     url: "/wells/muddata/insertmudtype",                    
     data: {
      mudtype:others_mudtype,
     },
     dataType: "json",
     success: function (data) {   
       if(data.status=="true"){
        current_element.closest('td').find('.mudtype option').eq(4).before($("<option selected></option>").val(data.mudtype.id).text(others_mudtype));
        $('#muddata-table tbody tr:eq('+closesttrindex+')').find('.mudtype').val(data.mudtype.id);
        $('#muddata-table tbody tr#muddatatobeadd').find('.mudtype option').eq(5).before($("<option ></option>").text(others_mudtype)); 
      }
    }
   });
  }
});
// $(document).on("blur", ".others_grade" , function() { 
//   var current_index=$(this).closest('tr').index();  
//   others_grade=$(this).val();
//   if($('#casingmastertable tbody tr:eq('+current_index+')').find('.grade option[value="'+others_grade+'"]').length==0){
//     $('#casingmastertable tbody tr:eq('+current_index+')').find('.grade option').eq(8).before($("<option selected></option>").val(others_grade).text(others_grade));
//   }
//   if(others_grade_array.indexOf(others_grade) === -1){  
//     others_grade_array.push(others_grade)
//   }   
// });
// call when add row in casing masters
$(document).on("click",".casingmaster_addrow" , function() {

  var current_index=$(this).closest('tr').index()+1;
  $("<tr>"+ $('#casingmaster_addrow').html()+" </tr>").insertAfter($(this).closest('tr'));
  for(var i=0;i<others_grade_array.length;i++){
    if(others_grade_array.length>0){
    $('#casingmastertable tbody tr:eq('+current_index+')').find('.grade option').eq(8).before($("<option></option>").val(others_grade_array[i]).text(others_grade_array[i]));
    }
    if(others_range_array.length > 0){
      $('#casingmastertable tbody tr:eq('+current_index+')').find('.casing_range option').eq(3).before($("<option></option>").val(others_range_array[i]).text(others_range_array[i]));
    }
    
  }
});
// $(document).on("blur", ".others_range" , function() { 
//   var current_index=$(this).closest('tr').index();  
//   others_range=$(this).val();
//   if($('#casingmastertable tbody tr:eq('+current_index+')').find('.casing_range option[value="'+others_range+'"]').length==0){
//     $('#casingmastertable tbody tr:eq('+current_index+')').find('.casing_range option').eq(3).before($("<option selected></option>").val(others_range).text(others_range));
//   }
//   if(others_range_array.indexOf(others_range) === -1){  
//     others_range_array.push(others_range)
//   }   
// });
//call when remove row in casing masters
$(document).on("click", ".casingmaster_removerow" , function() {   
 $(this).closest("tr").remove();
});

$('.casingmaster-unit').change(function(){
  var unit_array=["Nominal OD","Inside Diameter","Connection OD"];
  var unit=$(this).val();
  var unit_data;
  if(unit=='API'){
    unit_data='in'; 
  }else{
    unit_data='mm';
  }
  var html='';
  html +='<tr>';
  $("#casingmastertable thead tr th").each(function(){
    let curentText ;
    if($(this).find('span').length > 0){
      curentText = $(this).find('span').text();
    }else{
      curentText = $(this).text();
    } 
    if(unit_array.indexOf(curentText) !== -1){  
      html +='<th><span>'+ curentText+'</span>'+'('+unit_data+')'+'</th>';
    }else{
      html +='<th><span>'+curentText+'</span></th>';
    }  
  });
  html +='</tr>';
  $("#casingmastertable thead").html(html);
})

// $('.muddata_date').change(function(){
//   var wellphase=$("#well_phase").val();
//   var date=$("#basicDate").val();
//   $.ajax({
//     type: "GET",
//     data:{
//       wellphase:wellphase,
//       date:date
//     },
//     url:"/wells/bhadata/getmud",
//     success: function(data) {
//       var weight=data.data[0].mud_weight;
//       var plastic_viscosity=data.data[0].plastic_viscosity;
//       var yield_point=data.data[0].yield_point;
//       var low_shear_rate=data.data[0].low_shear_rate;
//       var gel_strength_0sec=data.data[0].gel_strength_0sec;
//       var gel_strength_10min=data.data[0].gel_strength_10min;
//       var gel_strength_30min=data.data[0].gel_strength_30min;

//       // if(data.length > 0 )
//       // {
//       $('#mud_weight').val(weight);
//       $('#plastic_viscosity').val(plastic_viscosity);
//       $('#yield_point').val(yield_point);
//       $('#low_shear_rate').val(low_shear_rate);
//       $('#gel_strength_0sec').val(gel_strength_0sec);
//       $('#gel_strength_10min').val(gel_strength_10min);
//       $('#gel_strength_30min').val(gel_strength_30min);
//       // }
//       // else{
//       // $('#mud_weight').val('');
//       // $('#plastic_viscosity').val('');
//       // $('#yield_point').val('');
//       // $('#low_shear_rate').val('');
//       // $('#gel_strength_0sec').val('');
//       // $('#gel_strength_10min').val('');
//       // $('#gel_strength_30min').val('');
//       // }
      
//     }
//   });
// });

// $('.bhadata_date').change(function(){
//   var wellphase=$("#well_phases").val();
//   var date=$("#basicDate").val();
//   $.ajax({
//     type: "GET",
//     data:{
//       wellphase:wellphase,
//       date:date
//     },
//     url:"/wells/bhadata/getbhadata",
//     success: function(data) {
//       console.log(data.data.length);

//       var html='';
//       html+= "<tr>"+ $('#header').html()+" </tr>";

      
//       for(i=0;i< data.data.length;i++){

//         var weight = data.data[i].weight!=null ? data.data[i].weight : '' ;
//         var pipe_type = data.data[i].pipe_type!=null ? data.data[i].pipe_type : '' ;
//         var connection_type = data.data[i].connection_type!=null ? data.data[i].connection_type : '' ;
//         var tool_od = data.data[i].tool_od!=null ? data.data[i].tool_od : '' ;
//         var classtype = data.data[i].classtype!=null ? data.data[i].classtype : '' ;
//         html +='<tr id="bhadatarow" class="bhadatarow"><td><input id="type_name" name="type_name" class="form-control" value="'+data.data[i].type_name+'"></td>';
//           html +='<td><input type="text" id="element" class="form-control element" name="element" value="'+data.data[i].element+'"></td>';
//           html +='<td><input type="number" step="any" id="od" class="form-control od" name="od" value="'+data.data[i].od+'"></td>';
//           html +='<td><input type="hidden" id="weight" class="form-control coll_weight" name="weight"  value="'+weight+'"><input type="hidden"  id="pipe_type" class="form-control pipe_type" name="pipe_type" value="'+pipe_type+'"><input type="hidden"  id="connection_type" name="connection_type" class="form-control connection_type" value="'+connection_type+'" ><input type="hidden"  id="tool_od" class="form-control tool_od" name="tool_od" value="'+tool_od+'" ><input type="hidden"  id="classtype" class="form-control classtype" name="classtype" value="'+classtype+'" ><input type="hidden"  id="grade" class="form-control grade" name="grade" value="'+data.data[i].grade+'"><input type="number" step="any" id="identity" class="form-control identity" name="identity" value="'+data.data[i].identity+'"></td>';
//           html +='<td><input type="number" step="any" id="length" class="form-control length" name="length" value="'+data.data[i].length+'"></td>';
//           html +='<td><input type="number" step="any" id="length_onejoint" class="form-control cumulative-length" name="length_onejoint" value="'+data.data[i].length_onejoint+'"></td>';

//           html+='<td><button type="button" name="add" class="addbhadatarows iconaction"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="deletebhadatarow iconaction"><i class="fa fa-trash"></i></button></td></tr>'
//       }
//       html+= "<tr id='bhadatarow' class='bhadatarow1'  style='display:none'>"+ $('.bhadatarow1').html()+" </tr>";
//       $("#bhadatatable tbody").html(html);


//       }
    
//     });
// });


$('.rheogram_date').change(function(){
  var wellphase=$("#well_phase").val();
  var date=$("#basicDate").val();
  $.ajax({
    type: "GET",
    data:{
      wellphase:wellphase,
      date:date
    },
    url:"/wells/bhadata/getrheogram",
    success: function(data) {

      var html='';
      html+= "<tr>"+ $('#header').html()+" </tr>";

      for(i=0;i< data.data.length;i++){
        html +='<tr><td><input type="text" id="rpm" class="form-control" name="rpm" placeholder="Rpm" value="'+data.data[i].rpm+'"></td><td><input type="text" id="dial" class="form-control" name="dial" placeholder="Dial" value="'+data.data[i].dial+'"></td><td><button type="button" name="add" class="addrheogram iconaction"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove iconaction"><i class="fa fa-trash"></i></button></td></tr>';

      }
      html+= "<tr id='rheogramrow' class='rheogramrow1' style='display:none'>"+ $('.rheogramrow1').html()+" </tr>";
      $("#rheogramtable tbody").html(html);
    }
  });
});


$('.drillbitdata_date').change(function(){
  var wellphase=$("#well_phases").val();
  var date=$("#basicDate").val();
  $.ajax({
    type: "GET",
    data:{
      wellphase:wellphase,
      date:date
    },
    url:"/wells/bhadata/getdrillbitdata",
    success: function(data) {

      var html='';
      html+= "<tr>"+ $('#header').html()+" </tr>";

    
      $("#bit_type").val(data.data[0][1].bit_type_id);
      $("#no_of_nozzle").val(data.data[0][1].no_of_nozzle);
      
      for(i=0;i< data.data[0][0].length;i++){
        html +='<tr><td><input type="number" step="any" id="nozzle_size" class="form-control nozzle_size" name="nozzle_size" value="'+data.data[i].nozzle_size+'"></td></tr>';

      }
      // html+= "<tr id='rheogramrow' class='rheogramrow1' style='display:none'>"+ $('.rheogramrow1').html()+" </tr>";
      // console.log(html);
      $("#drillbittable tbody").html(html);
    }
  });
});

$(document).on("click",".addmuddatarow" , function() {
  var trindex=$(this).closest('tr').index();
  var well_phase=$(this).attr("wellphase-id");
  if(welltype=='PLAN'){
    var trlength=$('#muddata-table tbody tr:last').index();
    // alert(trlength)
    var userfrom_depth=$(this).closest('tr').find('.from_depth').val()
    var userto_depth=$('#muddata-table tbody tr:eq('+(trlength-1)+')').find('.to_depth').val()
    var original_from_depth=$('#muddata-table tbody tr:eq(0)').find('.fromdepth').val();
    var original_to_depth=$('#muddata-table tbody tr:eq(0)').find('.todepth').val();
    // alert(original_to_depth);
    // alert(userto_depth)
    if(parseInt(userto_depth)<parseInt(original_to_depth)){
      // $('#muddata-table tbody').append("<tr>"+ $('#muddatatobeadd').html()+" </tr>");
      $("<tr>"+ $('#muddatatobeadd').html()+" </tr>").insertBefore('#muddata-table tbody tr#muddatatobeadd');
  
      // $("<tr>"+ $('#muddatatobeadd').html()+" </tr>").insertAfter($(this).closest('tr'));   
      $('#muddata-table tbody tr:eq('+(trlength)+')').find('.from_depth').val(parseInt(userto_depth));
      $('#muddata-table tbody tr:eq('+(trlength)+')').find('.to_depth').val(original_to_depth);
    }
    // var wellphase=$(this).closest('tr').find('#well_phases').val()
    var num=$(this).closest('tr').find('.section').val()
    var newindex=trindex+1;
      // $('#muddata-table tbody tr:eq('+newindex+')').find('.section').val('SEC'+(well_phase)+'0'+(++sect2));
      $('#muddata-table tbody tr:eq('+newindex+')').find('.section').val(userto_depth+'-'+original_to_depth);
    // $(this).closest('tr').find('.section').val((++sect2));
  }
  else{
    var $this     = $(this),
    $parentTR = $this.closest('tr');
    // $("<tr>"+ $('#muddatatobeadd').html()+" </tr>").insertBefore('#muddata-table tbody tr#muddatatobeadd');
    var newindex=trindex+1
    $parentTR.clone().insertAfter($parentTR).find('input').val('');
 
    $('#muddata-table tbody tr:eq('+newindex+')').addClass('new-row');
    $('#muddata-table tbody tr:eq('+newindex+')').find('.muddata_id').val("");
    $('#muddata-table tbody tr:eq('+newindex+')').find('.section_id').val("");
    $('#muddata-table tbody tr:eq('+newindex+')').find('.rheogramid').val("");

  }
 


});
$(document).on("keyup",".to_depth" , function() {
  var todepth=$(this).val();
  var original_to_depth=$('#muddata-table tbody tr:eq(0)').find('.todepth').val();
  if(parseInt(todepth)>parseInt(original_to_depth)){
    $(this).val('');
  }
});
$('.alert_message').hide();
$(document).on("blur",".to_depth" , function() {
  var trindex=$(this).closest('tr').index();
  var todepth=$(this).val();
  var fromdepth = $('#muddata-table tbody tr:eq('+trindex+')').find('.from_depth').val();
  if(parseInt(fromdepth) > parseInt(todepth)){
    // alert('From depth is not greater then To depth');
    $('#muddata-table tbody tr:eq('+trindex+')').find('.to_depth').val('');
    $( "div.alert_message" ).show();
    setTimeout(
      function() 
      {
        $( "div.alert_message" ).hide();
      }, 3000);
    
  }
  var nexttrindex = trindex +1;
  $('#muddata-table tbody tr:eq('+nexttrindex+')').find('.from_depth').val(todepth);
  var next_todepth=$('#muddata-table tbody tr:eq('+nexttrindex+')').find('.to_depth').val();
  $('#muddata-table tbody tr:eq('+trindex+')').find('.section').val(fromdepth+'-'+todepth);
  $('#muddata-table tbody tr:eq('+nexttrindex+')').find('.section').val(todepth+'-'+next_todepth);
});

$(document).on("blur",".from_depth" , function() {
var from_depth= $(this).val();
var current_ind = $(this).closest('tr').index();
var pre_ind=current_ind-1;
var todepth=$('#muddata-table tbody tr:eq('+current_ind+')').find('.to_depth').val();
var pre_todepth=$('#muddata-table tbody tr:eq('+pre_ind+')').find('.to_depth').val();
var pre_fromdepth=$('#muddata-table tbody tr:eq('+pre_ind+')').find('.from_depth').val();
if(parseInt(pre_fromdepth) > parseInt(from_depth)){
  // alert('From depth is not greater then To depth');
  $( "div.alert_message" ).show();
    setTimeout(
      function() 
      {
        $( "div.alert_message" ).hide();
      }, 3000);
  $('#muddata-table tbody tr:eq('+current_ind+')').find('.from_depth').val(pre_todepth);
}
else if(parseInt(from_depth) > parseInt(todepth)){
  $( "div.alert_message" ).show();
      setTimeout(
        function() 
        {
          $( "div.alert_message" ).hide();
        }, 3000);
  $('#muddata-table tbody tr:eq('+current_ind+')').find('.from_depth').val(pre_todepth);
}
else{
  $('#muddata-table tbody tr:eq('+pre_ind+')').find('.to_depth').val(from_depth);
  $('#muddata-table tbody tr:eq('+pre_ind+')').find('.section').val(pre_fromdepth+'-'+from_depth);
  $('#muddata-table tbody tr:eq('+current_ind+')').find('.section').val(from_depth+'-'+todepth);
}
});
// $(document).on("blur",".from_depth" , function() {
//   var trindex=$(this).closest('tr').index();
//   var fromdepth=$(this).val();
//   var pre_index=trindex-1;
//   var todepth = $('#muddata-table tbody tr:eq('+trindex+')').find('.to_depth').val();
//   if(parseInt(fromdepth) > parseInt(todepth)){
//     // alert('From depth is not greater then To depth');
//     $( "div.alert_message" ).show();
//     setTimeout(
//       function() 
//       {
//         $( "div.alert_message" ).hide();
//       }, 3000);
//     $('#muddata-table tbody tr:eq('+trindex+')').find('.from_depth').val('');
//   }
// });

$(document).on("click",".deletemuddatarow" , function() {
  var trcount=$('#muddata-table tbody tr').not("#muddatatobeadd").length
  if(trcount>1){
    $(this).closest('tr').remove();  
  }
});


$(document).on("click",".addrheogram-row" , function() {
  var currenttab_index=$(this).attr('data-id');
  var rheology_type=$(this).attr('data-type');
  var html='';
  alert(rheology_type)
  if(rheology_type=='indirect'){
    var tableid=$(this).closest('table').attr('id')
    var splitid=tableid.split('-')[0]
    html +='<tr> <input type="hidden" name="'+splitid+'rheogram_id'+currenttab_index+'"><td><input type="text" name="'+splitid+'rpm'+currenttab_index+'" class="form-control" placeholder="Rpm"></td><td><input type="text" name="'+splitid+'dial'+currenttab_index+'" class="form-control" placeholder="Dial"></td><td><button type="button" name="add" class="addrheogram-row iconaction" data-id='+currenttab_index+' data-type="indirect"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove-row iconaction" data-id='+currenttab_index+'><i class="fa fa-trash"></i></button></td></tr>';
    $(this).closest('table').append(html)
  }else{
  html +='<tr> <input type="hidden" name="rheogram_id'+currenttab_index+'"><td><input type="text" name="rpm'+currenttab_index+'" class="form-control rheo-edit-tbl" placeholder="Rpm"></td><td><input type="text" name="dial'+currenttab_index+'" class="form-control rheo-edit-tbl" placeholder="Dial"></td><td><button type="button" name="add" class="addrheogram-row iconaction" data-id='+currenttab_index+'><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove-row iconaction" data-id='+currenttab_index+'><i class="fa fa-trash"></i></button></td></tr>';
  $("#rheogram-table"+currenttab_index+"").append(html);
  }
  
});

$(document).on("click",".rheogramremove-row" , function() {
 $(this).closest('tr').remove();
});

$(document).on("click",".rheogramremove-tab" , function() {
  var tabcount = $("#section-tab a.nav-link").length;
  if(tabcount>1){
    var currenttab_index=$(this).attr('data-id');
    var tabid = "#section"+currenttab_index+"" +'-tab'
    $(tabid).remove();
    $("#section"+currenttab_index+"").remove()
  }
});

// $(document).on("keyup",".dial" , function() {
//   var rpm=$(this).closest('tr').find('.rpm').val();
//   var dial=$(this).val();
//   var plastic_viscosity=$(this).closest('tbody').find('.viscocity').val();
//   var newdial=rpm*plastic_viscosity;
//   $(this).closest('td').find('.calculateddial').val(newdial)
// });

$(document).on("keyup", ".mud_weight" , function() {
  from=$(this).closest('tr').find('.from_depth').val();
  to=$(this).closest('tr').find('.to_depth').val();
  var mud_weight=$(this).val();
  var well_id=$('#well').val();
  $.ajax({
    type: "GET",
    data:{
      from:from,
      to:to,
      well_id:well_id
    },
    url:"/wells/muddata/get_porepressure_md",
    success: function(data) {
      // console.log(data);
      if((mud_weight>data.from)||(mud_weight>data.to)){
        alert("Mud Weight is greater than fraction pressure");
      }
    }
  })
});
// $(document).on("change", ".modalselect" , function() {
//   var selectedmodal=$(this).val();
//   var section_name=$(this).attr('data-id')
//   var wellphase_id=$(this).attr('wellphase-id')
//   var tabindex=$(this).attr('tab-index')
//   $.ajax({
//     type: "GET",
//     data:{
//       selectedmodal:selectedmodal,
//       section_name:section_name,
//       wellphase_id:wellphase_id

//     },
//     url:"/wells/muddata/calculatedial",
//     success: function(data) {
//       var modal
//       if(selectedmodal==1){
//         modal='newtonian';
//       }else if(selectedmodal==2){
//         modal='bingham';
//       }else if(selectedmodal==3){
//         modal='powerlaw';
//       }else{
//         modal='hershel';
//       }
//       if(data.newdial.length>0){
//         var html='';
//         html +="<table id="+modal+"-table"+tabindex+"><thead><tr><th>RPM</th><th>Dial</th></tr></thead><tbody>"
//         for(var i=0;i<data.rpm.length;i++){
//           html +='<tr><td><input type="text" id="rpm" class="form-control rpm" name="rpm0" placeholder="Rpm" value='+data.rpm[i]+'></td><td><input type="text" id="dial" class="form-control dial" name="dial0" placeholder="Dial" value='+data.newdial[i]+'></td><td><button type="button" name="add" class="addrheogram-row iconaction" data-id="0"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="rheogramremove iconaction" data-id="0"><i class="fa fa-trash"></i></button></td></tr>'
//         }
//         html +='</tbody></table>';
//         $('#section'+tabindex).append(html)
//         if(selectedmodal==1){
//           $('#bingham-table'+tabindex).hide();
//           $('#powerlaw-table'+tabindex).hide();
//           $('#hershel-table'+tabindex).hide();
//         }else if(selectedmodal==2){
//           $('#newtonian-table'+tabindex).hide();
//           $('#powerlaw-table'+tabindex).hide();
//           $('#hershel-table'+tabindex).hide();
//         }else if(selectedmodal==3){
//           $('#newtonian-table'+tabindex).hide();
//           $('#powerlaw-table'+tabindex).hide();
//           $('#hershel-table'+tabindex).hide();
//         }else{
//           modal='hershel';
//         }
//       }

//     }
//   })

  
// });


// var storedArray = JSON.parse(sessionStorage.getItem("items"));
// // console.log(storedArray)
// var warning=''
// warning +='<div class="col-md-12 alert"><span class="closebtn" onclick="this.parentElement.style.display="none";">&times;</span>'
// warning +='<strong>ECD is greater than Fracture Pressure.</strong></div>'
// if(storedArray[0] != ''){
//     $('.warning').append(warning);
// }
// $('.closebtn').click(function(){
//   $('.alert').hide();
// })