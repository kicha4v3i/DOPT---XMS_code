$('body').on('focus',".muddata_date", function(){
    $(this).flatpickr({
        dateFormat: "d-m-Y",
        defaultDate: $(this).val()!=''?$(this).val():new Date()
    });
});
$('body').on('focus',".muddata_time", function(){
    $(this).flatpickr({
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        defaultDate: $(this).val()!=''?$(this).val():"12:00"
    });
});

$(document).on("change",'.muddata_date',function(){
    var closest_index=$(this).closest('tr').index()
    var selected_date=$(this).val()
    var selected_time=$(this).closest('tr').find('.muddata_time').val()
    if(closest_index>0){
        newindex=closest_index-1
        var previous_date=$('#muddata-table tbody tr:eq('+(newindex)+')').find('.muddata_date').val();
        var previous_time=$('#muddata-table tbody tr:eq('+(newindex)+')').find('.muddata_time').val();
    }
    else{
        var previous_date=""
        var previous_time=""
    }
    if(selected_date!='' && selected_time!=''){
        getmdtvd(selected_date,selected_time,previous_date,previous_time,closest_index)
    }
})
var focus_index
$(document).on("focus",'.rpm_parameter',function(){
    focus_index=$(this).closest('th').index()
})
$(document).on("click",'.add_column_muddata',function(){
   $('#muddata-table > tbody  > tr').each(function() {
        $(this).find('td').eq(focus_index).after('<td class="inp-width"><input type="number" step="any" class="form-control dial" name="dial"><input type="hidden" name="rheogram_id" class="rheogramid"></td>');
   });
   $('#muddata-table > thead:eq(1) > tr').find('th').eq(focus_index).after('<th class="txt-col-sub"><input type="number" step="any" class="form-control rpm_parameter" name="rpm_parameter"></th>');

})
$(document).on("click",'.remove_column_muddata',function(){
    $('#muddata-table > tbody  > tr').each(function() {
         $(this).find('td').eq(focus_index+1).remove();
    });
    $('#muddata-table > thead:eq(1) > tr').find('th').eq(focus_index+1).remove()
 
})
$(document).on("blur",'.rpm_parameter',function(){
    var closest_index=$(this).closest('th').index()
    var rpm=$(this).val()
    // console.log(closest_index)
    // console.log(rpm)


    $('#muddata-table > tbody  > tr').each(function() {
        $(this).find('td').eq(closest_index).find('.dial').attr('name','dial_'+rpm+'');
        $(this).find('td').eq(closest_index).find('.rheogramid').attr('name','rheogram_id_'+rpm+'');

   });


 
})

 
$(document).on("change",'.muddata_time',function(){
    var closest_index=$(this).closest('tr').index()

    var selected_time=$(this).val()
    var selected_date=$(this).closest('tr').find('.muddata_date').val()

    if(closest_index>0){
        newindex=closest_index-1
        var previous_date=$('#muddata-table tbody tr:eq('+(newindex)+')').find('.muddata_date').val();
        var previous_time=$('#muddata-table tbody tr:eq('+(newindex)+')').find('.muddata_time').val();
    }
    else{
        var previous_date=""
        var previous_time=""
    }
    if(selected_date!='' && selected_time!=''){
        getmdtvd(selected_date,selected_time,previous_date,previous_time,closest_index)
    }
})
$(document).on("click",'.addrheogram',function(){
    var index=$(this).closest('tr').index()
    $.ajax({
        type: "GET",
        url:"/wells/muddata/getrheogramrpm",
        success: function(data) { 
            var html = '';
            html +='<div class="modal" id="rheogram_popup'+index+'">'
            html +='<div class="modal-dialog">'
            html +='<div class="modal-content">'
            html +='<div class="modal-header">'
            html +='<h4 class="modal-title">Rheogram</h4>'
            html +='</div>'
            html +='<div class="modal-body">'
            html +='<table>'
            html +='<tbody>'
            for(var i=0;i<data.length;i++){
                html +='<tr>'
                html +='<td><input type="text" name="rpm'+index+'" value='+data[i].fields.rheogram_rpm+' class="form-control"></td>'
                html +='<td><input type="text" name="dial'+index+'" class="form-control"></td>'
                html +='<td><button type="button" name="add" class="addrheo_row iconaction"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="removerheo_row iconaction"><i class="fa fa-trash"></i></button></td>'
                html +='</tr>'
            }
            html +='</tbody>'
            html +='</table>'
            html += '</div>'
            html += '<div class="modal-footer"><button type="button" class="btn btn-danger" data-dismiss="modal">Close</button></div>'
            html += '</div>'
            html += '</div>'
            html +='</div>'
            $('#rheogrammodals').append(html);
            $('#rheogram_popup'+index).modal('show');

        }
    });   
})
$(document).on("click",'.addrheo_row',function(){
    var index=$(this).closest('tr').index()
    html=''
    html +='<tr>'
    html +='<td><input type="text" name="rpm'+index+'"  class="form-control"></td>'
    html +='<td><input type="text" name="dial'+index+'" class="form-control"></td>'
    html +='<td><button type="button" name="add" class="addrheo_row iconaction"><i class="fa fa-plus"></i></button><button type="button" name="remove" class="removerheo_row iconaction"><i class="fa fa-trash"></i></button></td>'
    html +='</tr>'
    $(this).closest('tr').after(html);
})
$(document).on("click",'.removerheo_row',function(){
    $(this).closest('tr').remove()
})

function getmdtvd(selected_date,selected_time,previous_date,previous_time,closest_index){
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
            $('#muddata-table tbody tr:eq('+(closest_index)+')').find('.depth').val(data.md);
        }
    });
}
