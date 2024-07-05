$('body').on('click',".addhydraulic_data", function(){
 var dataid=$(this).attr('data_id')
 var append_html=$('.tablerow').html()
 var type=$('#type').val();
  $('#hydraulic_content'+dataid+'').append('<div class="tablerow row1" id="new_row">'+append_html+'</div>')
// $('#hydraulic_content'+dataid+'').append('<tbody class="tablerow row1">'+append_html+'</tbody>')
//  $('#hydraulicrow'+dataid+'').find('.start_time').attr('name','start_time'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.start_time').attr('dataid',dataid)
//  $('#hydraulicrow'+dataid+'').find('.md').attr('name','md'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.flowrate').attr('name','flowrate'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.rop').attr('name','rop'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.rpm').attr('name','rpm'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.pump_pressure').attr('name','pump_pressure'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.annular_pressure').attr('name','annular_pressure'+dataid+'')
//  $('#hydraulicrow'+dataid+'').find('.ecd').attr('name','ecd'+dataid+'')
 $('#hydraulicrow'+dataid+'').find('.addhydraulic_data').attr('data_id',dataid)
 $('#hydraulicrow'+dataid+'').find('.removehydraulic_data').attr('data_id',dataid)
//  if(type=='edit'){
//     $('#hydraulicrow'+dataid+'').find('#hydraulic_id').attr('name','hydraulic_id'+dataid+'')
//  }
});
$('body').on('click',".removehydraulic_data", function(){
    var dataid=$(this).attr('data_id')
});
$('body').on('click',".addhydraulic_content", function(){
    var html=$('.addtableBox').html()
    var rowlength=$('.tableBox').length
    var type=$('#type').val();
    $('.tableContent').append('<div class="tableBox" id="hydraulicrow'+rowlength+'">'+html+'</div>')
    $('#hydraulicrow'+rowlength+'').find('.rightCol').attr('id','hydraulic_content'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.start_time').attr('name','start_time'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.start_time').attr('dataid',rowlength)
    $('#hydraulicrow'+rowlength+'').find('.md').attr('name','md'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.flowrate').attr('name','flowrate'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.rop').attr('name','rop'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.rpm').attr('name','rpm'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.pump_pressure').attr('name','pump_pressure'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.annular_pressure').attr('name','annular_pressure'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.ecd').attr('name','ecd'+rowlength+'')
    $('#hydraulicrow'+rowlength+'').find('.addhydraulic_data').attr('data_id',rowlength)
    $('#hydraulicrow'+rowlength+'').find('.removehydraulic_data').attr('data_id',rowlength)
    if(type=='edit'){
        $('#hydraulicrow'+rowlength+'').find('#hydraulic_id').attr('name','hydraulic_id'+rowlength+'')
    }

});
$(document).on("change",'.start_time',function(){
    var closest_index=$(this).closest('div.tablerow').index()
    var newindex=closest_index-1
    var dataid=$(this).attr('dataid')
    var selected_time=$(this).val()
    var selected_date=$('#hydraulicrow'+dataid+'').find('.start_date').val()
    console.log(newindex)
    if(closest_index>0){
        var previous_time=$('#hydraulic_content'+dataid+'').find('.tablerow:eq('+newindex+')').find('.start_time').val()
        var previous_date=selected_date

    }else{
        var previous_time=""
        var previous_date=""

    }
    getmdtvd(selected_date,selected_time,previous_time,previous_date,$(this))
})
function getmdtvd(selected_date,selected_time,previous_time,previous_date,current_element){
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
            current_element.closest('div.tablerow').find('.md').val(data.md)

        }
    });
}
