var closesttrindex;
var indexid
$("document").ready(function() {
    $(".empirical_popup_button").each(function() {
        var bhaelememt_id=$(this).attr('bhaelement_id')
        var dataid=$(this).attr('dataid')
        var type_name=$(this).closest('tr').find('.type_name').val();
        var calculation_type=$(this).closest('tr').find('.calculation_type').val();
        var index=$(this).closest('tr').index();
        var unit=$('.unit').val();
        var modalid=type_name+dataid+'_'+index
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getempiricaldata",                    
            data: {
               bhaelememt_id:bhaelememt_id,
            },
            dataType: "json",
            success: function (data) { 
                var html = '';
                html +='<div class="modal" id='+modalid+'>'
                html +='<div class="modal-dialog">'
                html +='<div class="modal-content">'
                html +='<div class="modal-header">'
                html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations</h4>'
                html +='</div>'
                html += '<h2 style="text-align: center;">'+type_name+'</h2>'
                html +='<div class="modal-body">'
                html +='<div class="table-responsive formgroup_b0">'
                html +='<div class="row">'
                html +='<div class="col-6">'
                html +='<h3 style="text-align: center;">Specifications</h3>'
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+dataid+'_'+index+'" placeholder="Name" value='+type_name+'></div></div></div>';
                if(unit == 'API'){
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(in)</label></div><div class="col"><input type="text" id="specification_od'+dataid+'_'+index+'" class="form-control" name="specification_od'+dataid+'_'+index+'" placeholder="OD" value='+data[0].specifications[0].specification_od+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(in)</label></div><div class="col"><input type="text" id="specification_id'+dataid+'_'+index+'" class="form-control" name="specification_id'+dataid+'_'+index+'" placeholder="ID" value='+data[0].specifications[0].specification_id+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(ft)</label></div><div class="col"><input type="text" id="specification_length'+dataid+'_'+index+'" class="form-control" name="specification_length'+dataid+'_'+index+'" placeholder="Length" value='+data[0].specifications[0].specification_length+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate" value='+data[0].specifications[0].minimum_flowrate+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate" value='+data[0].specifications[0].maximum_flowrate+'></div></div></div>';
                }else{
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(mm)</label></div><div class="col"><input type="text" id="specification_od'+dataid+'_'+index+'" class="form-control" name="specification_od'+dataid+'_'+index+'" placeholder="OD" value='+data[0].specifications[0].specification_od+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(mm)</label></div><div class="col"><input type="text" id="specification_id'+dataid+'_'+index+'" class="form-control" name="specification_id'+dataid+'_'+index+'" placeholder="ID" value='+data[0].specifications[0].specification_id+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(m)</label></div><div class="col"><input type="text" id="specification_length'+dataid+'_'+index+'" class="form-control" name="specification_length'+dataid+'_'+index+'" placeholder="Length" value='+data[0].specifications[0].specification_length+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" placeholder="Minimum Flowrate" value='+data[0].specifications[0].minimum_flowrate+'></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" placeholder="Maximum Flowrate" value='+data[0].specifications[0].maximum_flowrate+'></div></div></div>';
                }
                html += '</div>'
                html += '<div  class="col-6">'
                html += '<h3 style="text-align: center;">Pressure Drop across Tool</h3>'
                html += '<ul class="nav nav-tabs" role="tablist">'
                html += '<li class="nav-item">'
                html += '<a class="nav-link" onclick="test(1)" data-toggle="tab" href="#flowrate_tab'+dataid+'_'+index+'" role="tab" aria-selected="true">Flow Test</a>'
                html += '</li>'
                html += '<li class="nav-item">'
                html += '<a class="nav-link" onclick="test(2)" data-toggle="tab" href="#empirical_tab'+dataid+'_'+index+'" role="tab">Empirical</a>'
                html += '</li>'
                html += '</ul>'
                html += '<div class="tab-content">'
                html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+dataid+'_'+index+' role="tabpanel" aria-labelledby="home-tab">'
                html += '<table class="table flowratetable" id="flowratetable">'
                if(unit == 'API'){
                html += '<thead><tr><th>Flowrate(GPM)</th><th>Pressure Drop(psi)</th><th>Action</th></tr></thead>'
                }else{
                html += '<thead><tr><th>Flowrate(LPM)</th><th>Pressure Drop(kPa)</th><th>Action</th></tr></thead>'
                }
                if(calculation_type==1){
                for(var i=0;i<data[0].pressdroptool.length;i++){
                html += '<tbody><tr id="flowraterow">'
                html += '<td><input type="hidden" name="pressuredrop_tool'+dataid+'_'+index+'" value='+data[0].pressdroptool[i].id+'><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+dataid+'_'+index+'" placeholder="Flowrate" value='+data[0].pressdroptool[i].flowrate+'></td>'
                html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'_'+index+'" placeholder="Pressure Drop" value='+data[0].pressdroptool[i].pressure_drop+'></td>'
                html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                html += '</tr>'
                }}
                else{
                html += '<tbody><tr id="flowraterow">'
                html += '<td><input type="hidden" name="pressuredrop_tool'+dataid+'_'+index+'" value=""><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+dataid+'_'+index+'" placeholder="Flowrate" value=""></td>'
                html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'_'+index+'" placeholder="Pressure Drop" value=""></td>'
                html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                html += '</tr>'
                }
                html += '<tr id="flowraterow2" style="display:none">'
                html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+dataid+'_'+index+'" placeholder="Flowrate"></td>'
                html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+dataid+'_'+index+'" placeholder="Pressure Drop"></td>'
                html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                html += '</tr></tbody>'
                html +='</table>'
                html += '</div>'
                html += '<div class="tab-pane empirical_tab fade show" id=empirical_tab'+dataid+'_'+index+' role="tabpanel" aria-labelledby="home-tab">'
                html += '<h4>Variables</h4>'
                html += '<ul class="parameters_list">'
                html +='<li class="parameter">Mud Weight</li>'
                html +='<li class="parameter">Flowrate</li>'
                html +='<li class="parameter">Inner Diameter</li>'
                html +='<li class="parameter">Constant</li>'
                html +='</ul>'
    
                html += '<h4>Operators</h4>'
                html += '<ul class="parameter_list">'
                html +='<li class="parameter">+</li>'
                html +='<li class="parameter">_</li>'
                html +='<li class="parameter">*</li>'
                html +='<li class="parameter">/</li>'
                html +='<li class="parameter">Power</li>'
                html +='<li class="parameter">Square</li>'
                html +='<li class="parameter">Cube</li>'
                html +='<li class="parameter">Square Root</li>'
                html +='<li class="parameter">Cube Root</li>'
                html +='</ul>'
                if(calculation_type==2){
                html +='<div id=formula'+dataid+'_'+index+' contenteditable="true" style="width: 400px;height: 100px;background-color: #0302020f;">'+data[0].empirical[0].formula+'<input type="hidden" name=formulatext'+dataid+'_'+index+' id=formulatext'+dataid+'_'+index+' value="'+data[0].empirical[0].formula+'"><input type="hidden" id=formula_python_text'+dataid+'_'+index+' name=formula_python_text'+dataid+'_'+index+' value='+data[0].empirical[0].formula_python_text+'></div>'
                html += '</div>'
                }
                else{
                html +='<div id=formula'+dataid+'_'+index+' contenteditable="true" style="width: 400px;height: 100px;background-color: #0302020f;"><input type="hidden" name=formulatext'+dataid+'_'+index+' id=formulatext'+dataid+'_'+index+' value=""><input type="hidden" id=formula_python_text'+dataid+'_'+index+' name=formula_python_text'+dataid+'_'+index+' value=""></div>'
                html += '</div>'
                }
                html += '</div>'
    
                html += '</div>'
                html += '</div>'
                html += '</div>'
                html += '</div>'
                
                html += '<div class="modal-footer"><button type="button" class="btn btn-danger" data-id='+dataid+'_'+index+' data-modal='+modalid+' data-dismiss="rss_inputs" id="modalclose" >Close</button></div> '
                html += '</div>'
                html += '</div>'
                html +='</div>'
                $('#flowratemodal').append(html);
                if(calculation_type==2){
                $('#formula'+closestindex).append(data[0].empirical[0].formula);
                }
            }
        })
    })
    $('.mudmotor_popup_button').each(function(){
        var bhaelememt_id=$(this).attr('bhaelement_id')
        var dataid=$(this).attr('dataid')
        var type_name=$(this).closest('tr').find('.type_name').val();

        var index=$(this).closest('tr').index();
        var unit=$('.unit').val();
        var modalid='mud_motor'+dataid+'_'+index

        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getdifferential_Pressure",                    
            data: {
                bhaelememt_id:bhaelememt_id,
            },
            dataType: "json",
            success: function (data) { 
                var html = '';
                html +='<div class="modal" id='+modalid+'>'
                html +='<div class="modal-dialog">'
                html +='<div class="modal-content">'
                html +='<div class="modal-header">'
                html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations</h4>'
                html +='</div>'
                html += '<h2 style="text-align: center;">'+type_name+'</h2>'
                html +='<div class="modal-body">'
                html +='<div class="row">'
                html +='<div class="col-5">'
                html +='<h3 style="text-align: center;">Specifications</h3>'
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+dataid+'_'+index+'" value="'+type_name+'"></div></div></div>';
                if(unit == 'API'){
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" value="'+data[0].specifications[0].maximum_flowrate+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" value="'+data[0].specifications[0].minimum_flowrate+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+dataid+'_'+index+'" value="'+data[0].specifications[0].maximum_rpm+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+dataid+'_'+index+'" value="'+data[0].specifications[0].minimum_rpm+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(psi) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+dataid+'_'+index+'" value="'+data[0].specifications[0].no_load_diff_pressure+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(psi)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+dataid+'_'+index+'" value="'+data[0].specifications[0].max_dp+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(psi)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+dataid+'_'+index+'" value="'+data[0].specifications[0].recom_dp+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB(lbf)</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+dataid+'_'+index+'" value="'+data[0].specifications[0].max_wob+'"></div></div></div>';
                }else{
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+dataid+'_'+index+'" value="'+data[0].specifications[0].maximum_flowrate+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+dataid+'_'+index+'" value="'+data[0].specifications[0].minimum_flowrate+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+dataid+'_'+index+'" value="'+data[0].specifications[0].maximum_rpm+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+dataid+'_'+index+'" value="'+data[0].specifications[0].minimum_rpm+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(kPa) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+dataid+'_'+index+'" value="'+data[0].specifications[0].no_load_diff_pressure+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(kPa)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+dataid+'_'+index+'" value="'+data[0].specifications[0].max_dp+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(kPa)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+dataid+'_'+index+'" value="'+data[0].specifications[0].recom_dp+'"></div></div></div>';
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+dataid+'_'+index+'" value="'+data[0].specifications[0].max_wob+'"></div></div></div>';
                }
                html += '</div>'
                html += '<div class="tab-content">'
                html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
                html +='<h3 style="text-align: center;">Differential Pressure Table</h3>'
                html += '<table class="table diff_pressure_table" id="diff_pressure_table">'
                html += '<thead><tr><th></th><th>Torque</th><th>Differential Pressure</th><th>Action</th></tr></thead>'
                for(var i=0;i<data[0].differntial_pressure.length;i++){
                html += '<tbody><tr id="pressure_row">'
                html += '<td><input type="hidden" name="differntial_pressure'+dataid+'_'+index+'" value='+data[0].differntial_pressure[i].id+'>'
                html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+dataid+'_'+index+'" value="'+data[0].differntial_pressure[i].torque+'"></td>'
                html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+dataid+'_'+index+'" value="'+data[0].differntial_pressure[i].diff_pressure+'"></td>'
                html += '<td><button type="button" name="add" class="addpressurerows_edit iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows_edit iconaction"><i class="fa fa-trash"></i></button></td>'
                html += '</tr>'
                }
                html += '<tr id="pressure_row2" style="display:none">'
                html += '<td><input type="hidden" name="differntial_pressure'+dataid+'_'+index+'" value="">'
                html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+dataid+'_'+index+'" placeholder="Torque"></td>'
                html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+dataid+'_'+index+'" placeholder="Differential Pressure"></td>'
                html += '<td><button type="button" name="add" class="addpressurerows_edit iconaction" dataid='+dataid+'_'+index+'><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows_edit iconaction"><i class="fa fa-trash"></i></button></td>'
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
            }
        })
    })
    // call when click od in bhaedit page
    $(document).on("click",".od_edit",function(){
        var type_name = $(this).closest('tr').find('.type_name_edit').val(); 
        closesttrindex=$(this).closest('tr').index();
        $('input[type="radio"]').prop('checked', false); 
        if( type_name == 'Drill Collar')
        {
          $('.drillcollar-modal').modal('show');
        }
        else if( type_name == 'Drill Pipe')
        {
          $('.drillpipebha_edit').modal('show');
        }
        else if( type_name == 'Heavy Weight Drill Pipe')
        {
          $('.drillpipehwdp_edit').modal('show');
        }
    });
   
})

$(document).on("change",'.start_date',function(){
    var data_id=$(this).attr('data-id')
    var selected_date=$(this).val()
    var selected_time=$("#starttime"+data_id+"").val()
    previousindex=data_id-1
    if(data_id>1){
        var previous_date=$("#startdate"+previousindex+"").val()
        var previous_time=$("#starttime"+previousindex+"").val()
    }
    else{
        var previous_date=""
        var previous_time=""
    }
    if(selected_date!='' && selected_time!=''){
        getmdtvd(selected_date,selected_time,previous_date,previous_time,data_id)
    }
})
$(document).on("change",'.start_time',function(){
    var data_id=$(this).attr('data-id')

    var selected_time=$(this).val()
    var selected_date=$("#startdate"+data_id+"").val()
    previousindex=data_id-1

    if(data_id>1){
        var previous_date=$("#startdate"+previousindex+"").val()
        var previous_time=$("#starttime"+previousindex+"").val()
    }
    else{
        var previous_date=""
        var previous_time=""
    }
    if(selected_date!='' && selected_time!=''){
        getmdtvd(selected_date,selected_time,previous_date,previous_time,data_id)
    }
})


function getmdtvd(selected_date,selected_time,previous_date,previous_time,data_id){
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
            $('#bhadatatable'+data_id+' tbody tr:eq(0) td:eq(5)').find('.cumulative-length').val(data.md)
            $('#bhadatatable'+data_id+' tbody tr:eq(0) td:eq(5)').find('.measured_depth').val(data.md)
        }
    });
}

$(document).on("blur",'.actual_length',function(){
    var data_id=$(this).attr('dataid')
    var current_index=$(this).closest('tr').index();
    var total_measured_depth=$('#bhadatatable'+data_id+' tbody tr:eq(0)').find('.measured_depth').val();
  
    var cumulative_total=0;
    $('#bhadatatable'+data_id+' tbody tr').each(function(index,tr){
        if($(tr).find('td input.actual_length').val()!=undefined && $(tr).find('td input.actual_length').val()!=''){
            cumulative_total =cumulative_total+parseFloat($(tr).find('td input.actual_length').val());
        }
    });
    // console.log(cumulative_total)
    // console.log(total_measured_depth)
    var remaining=total_measured_depth-cumulative_total;
    if(parseFloat(cumulative_total)<total_measured_depth){
      $(this).closest('tr').find('.cumulative-length').val(cumulative_total);
      var newindex=current_index+1;
      $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.actual_length').val(remaining);
      $('#bhadatatable'+data_id+' tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
  
    }else{
      $(this).closest('tr').find('.cumulative-length').val(total_measured_depth);
    //   $(this).val('')
    }
})
$(document).on("blur",'.depth',function(){
   var depth=$(this).val();
   var data_id=$(this).attr('data-id')
   $('#bhadatatable'+data_id+' tbody tr:eq(0) td:eq(5)').find('.cumulative-length').val(depth)
   $('#bhadatatable'+data_id+' tbody tr:eq(0) td:eq(5)').find('.measured_depth').val(depth)
})
$(document).on("click",'.remove_bha',function(){
    $(this).closest('.panel').remove()
})

$(document).on("click",'#add_bha',function(){
    var panel_count = $('.panel').length
    var panel_html=$('.panel').html()
    var type=$('#type').val();
    var new_panel_html='<div class="panel panel-default new_row">'+panel_html+'</div>'
    $('#accordion').append(new_panel_html)
    $('.panel:last').find('.start_date').attr('id','startdate'+panel_count+'')
    $('.panel:last').find('.start_date').attr('data-id',panel_count)
    $('.panel:last').find('.start_time').attr('id','starttime'+panel_count+'')
    $('.panel:last').find('.start_time').attr('data-id',panel_count)
    $('.panel:last').find('.depth').attr('data-id',panel_count)
    $('.panel:last').find('.depth').attr('id','depth'+panel_count)
    $('.panel:last').find('.bhaname').attr('id','bhaname'+panel_count+'')
    $('.panel:last').find('.bhaname').attr('data-id',panel_count)
    $('.panel:last').find('.expand-btn').attr('href','#collapseOne'+panel_count+'')
    $('.panel:last').find('.viewfile').attr('data-id',panel_count+'')
    $('.panel:last').find('.exceltable').attr('id','exceltable'+panel_count+'')
    $('.panel:last').find('.excelfile').attr('id','excelfile'+panel_count+'')
    $('.panel:last').find('.collapse').attr('id','collapseOne'+panel_count+'')
    $('.panel:last').find('.bhadatatable').attr('id','bhadatatable'+panel_count+'')
    $('.panel:last').find('.type_name').attr('name','type_name'+panel_count+'')
    $('.panel:last').find('.type_name').attr('dataid',panel_count)
    $('.panel:last').find('.rss_button').attr('dataid',panel_count)
    $('.panel:last').find('.mudmotor_button').attr('dataid',panel_count)
    $('.panel:last').find('.element').attr('name','element'+panel_count+'')
    $('.panel:last').find('.od').attr('name','od'+panel_count+'')
    $('.panel:last').find('.od').attr('dataid',panel_count)
    $('.panel:last').find('.database_od').attr('name','database_od'+panel_count+'')
    $('.panel:last').find('.coll_weight').attr('name','weight'+panel_count+'')
    $('.panel:last').find('.pipe_type').attr('name','pipe_type'+panel_count+'')
    $('.panel:last').find('.connection_type').attr('name','connection_type'+panel_count+'')
    $('.panel:last').find('.tool_od').attr('name','tool_od'+panel_count+'')
    $('.panel:last').find('.tool_id').attr('name','tool_id'+panel_count+'')
    $('.panel:last').find('.classtype').attr('name','classtype'+panel_count+'')
    $('.panel:last').find('.grade').attr('name','grade'+panel_count+'')
    $('.panel:last').find('.onejoint_length').attr('name','onejoint_length'+panel_count+'')
    $('.panel:last').find('.box_tj_length').attr('name','box_tj_length'+panel_count+'')
    $('.panel:last').find('.pin_tj_length').attr('name','pin_tj_length'+panel_count+'')
    $('.panel:last').find('.identity').attr('name','identity'+panel_count+'')
    $('.panel:last').find('.actual_length').attr('name','length'+panel_count+'')
    $('.panel:last').find('.actual_length').attr('dataid',panel_count)
    $('.panel:last').find('.cumulative-length').attr('name','length_onejoint'+panel_count+'')
    $('.panel:last').find('.addbhadatarows').attr('dataid',panel_count)
    $('.panel:last').find('.deletebhadatarow').attr('dataid',panel_count)
    $('.panel:last').find('.bhaelement_id').attr('name','bhaelement_id'+panel_count+'')
    $('.panel:last').find('.copy_bha').attr('dataid',panel_count)
    $('.panel:last').find('.paste_bha').attr('dataid',panel_count)

    if(type=='edit'){
        $('.panel:last').find('.start_date').val("")
        $('.panel:last').find('.start_time').val("")
        $('.panel:last').find('.depth').val("")
        $('.panel:last').find('.bhaname').val("")
        $('.panel:last').find('.bhaelement_id').val("")
        $('.panel:last').find('.type_name:first').val("Bit")
        $('.panel:last').find('.type_name:not(:first)').val("")
        $('.panel:last').find('.element').val("")
        $('.panel:last').find('.od').val("")
        $('.panel:last').find('.od').val("")
        $('.panel:last').find('.actual_length').val("")
        $('.panel:last').find('.cumulative-length').val("")
        $('.panel:last').find('.identity').val("")
        $('.panel:last').find('.coll_weight').val("")
        $('.panel:last').find('.pipe_type').val("")
        $('.panel:last').find('.connection_type').val("")
        $('.panel:last').find('.tool_od').val("")
        $('.panel:last').find('.tool_id').val("")
        $('.panel:last').find('.classtype').val("")
        $('.panel:last').find('.grade').val("")
        $('.panel:last').find('.onejoint_length').val("")
        $('.panel:last').find('.box_tj_length').val("")
        $('.panel:last').find('.pin_tj_length').val("")
        $('.panel:last').find('.bha_id').val("")
        $('.panel:last').find('.empirical_popup_button').remove()
        $('.panel:last').find('.mudmotor_popup_button').remove()
    }
})

$(document).on("click",'.empirical_popup_button',function(){
    var bhaelememt_id=$(this).attr('bhaelement_id')
    var dataid=$(this).attr('dataid')
    var type_name=$(this).closest('tr').find('.type_name').val();
    var calculation_type=$(this).closest('tr').find('.calculation_type').val();
    var index=$(this).closest('tr').index();
    var unit=$('.unit').val();
    var modalid=type_name+dataid+'_'+index
    $('#'+modalid).modal('show');
    $('#flowratemodal').show();

})
$('.mudmotor_popup_button').click(function(){ 
    var bhaelememt_id=$(this).attr('bhaelement_id')
    var dataid=$(this).attr('data-id')
    var type_name=$(this).closest('tr').find('.type_name').val();
    var index=$(this).closest('tr').index();
    var unit=$('.unit').val();
    var modalid='mud_motor'+dataid+'_'+index
    $('#'+modalid).modal('show');
})


 $(document).on("click",".deletebhadatarow" , function() {
    var closest_index =$(this).closest('tr').index()
    var dataid=$(this).attr('dataid');
    var rowCounts = $('#bhadatatable'+dataid+' >tbody >tr').length;
    var actual_length=$(this).closest('tr').find('.actual_length').val()
    var cumulative_length=$(this).closest('tr').find('.cumulative-length').val()
    new_index=closest_index+1
    var totalrows=rowCounts-1
    // console.log(totalrows)
    // console.log(actual_length)
    // console.log(cumulative_length)
    if(new_index=totalrows){
       

    }



    $(this).closest('tr').remove()
});

var $clone = 0;
$(document).on("click",'.copy_bha',function(){
    var dataid=$(this).attr('dataid');
    $clone = $('#bhadatatable'+dataid+'').clone();
    $clone.find("input:hidden").val();
    $clone.find("#type_name").val();
})
$(document).on("click",'.paste_bha',function(){
    var dataid=$(this).attr('dataid');
    $clone.find('td').find('input').each(function(){
        var el = $(this);
        var id = el.attr('id') || null;
        if(id) {
            var i = id.substr(id.length);
            var prefix = id.substr(0, (id.length));
            el.attr('name', prefix+(+dataid));
        }
    });
    $clone.find('td').find('select').each(function(){
        var el = $(this);
        var id = el.attr('id') || null;
        if(id) {
            var i = id.substr(id.length);
            var prefix = id.substr(0, (id.length));
            el.attr('name', prefix+(+dataid));
        }
    });
    $('#bhadatatable'+dataid+'').html($clone);
})


$(document).on("change", ".type_name", function(){
    var val = $(this).val(); 
    $("option", this).removeAttr("selected").filter(function(){
        return $(this).attr("value") == val;
    }).first().attr("selected", "selected"); 
});



// call when click od in bhacreate page
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
/* call when change one length joint of drill pipe in bhaedit page or bhacreate page
get box tj length and pin tj length from database
*/
$("#drillpipe_onejoint_length").keyup(function () { 
  var onejointlength=$(this).val();
  var well_id = $('#well').val();
  var currentpage=$('#currentpage').val()
  if(welltype=='ACTUAL'){
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val(onejointlength);
    var type_name= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.type_name').val();
    var od= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.database_od').val();
    var id=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.identity').val();
    var weight= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.coll_weight').val();
    var grade=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.grade').val();
    var connection_type=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.connection_type').val();
    var classtype=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.classtype').val();
    var onejoint_length=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val();
    var total_measured_depth=$('#bhadatatable'+indexid+' tbody tr:eq(1)').find('.measured_depth').val();
  }else{
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val(onejointlength);
    if(currentpage=='createbha'){
      var type_name= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.type_name').val();
      var od= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od').val();
      var id=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val();


    }else{
      var type_name= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.type_name_edit').val();
      var od= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od_edit').val();
      var id=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity_edit').val();

    }
    var weight= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val();
    var grade=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.grade').val();
    var connection_type=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val();
    var classtype=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val();
    var onejoint_length=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val();
    var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();

  }
 
  if(onejointlength!='' ){
    gettool_joint(type_name,od,id,weight,grade,connection_type,classtype,onejoint_length,total_measured_depth,well_id)
}
});
/* call when change one length joint of heavy weight drill pipe in bhaedit page or bhacreate page
get box tj length and pin tj length from database
*/
$("#hwdp_one_joint_length").keyup(function () { 
  var well_id = $('#well').val();
  var onejointlength=$(this).val();
  if(welltype=='ACTUAL'){
    $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val(onejointlength);
    var type_name= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.type_name').val();
    var od= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.database_od').val();
    var id=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.identity').val();
    var weight= $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.coll_weight').val();
    var grade=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.grade').val();
    var connection_type=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.connection_type').val();
    var classtype=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.classtype').val();
    var onejoint_length=$('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val();
    var total_measured_depth=$('#bhadatatable'+indexid+' tbody tr:eq(1)').find('.measured_depth').val();
  }else{
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val(onejointlength);
    var type_name= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.type_name').val();
    var od= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od').val();
    var id=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val();
    var weight= $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val();
    var grade=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.grade').val();
    var connection_type=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val();
    var classtype=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val();
    var onejoint_length=$('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.onejoint_length').val();
    var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();

  }
  
  if(onejointlength!='' ){
    gettool_joint(type_name,od,id,weight,grade,connection_type,classtype,onejoint_length,total_measured_depth,well_id)
}
});
//common function for get tool joint
function gettool_joint(type_name,od,id,weight,grade,connection_type,classtype,onejoint_length,total_measured_depth,well_id){
  console.log(type_name)
  console.log(od)
  console.log(id)
  console.log(weight)


    $.ajax({ 
      type: "GET",                      
      url: "/wells/bhadata/box_pin_tooljoint",                    
      data: {
        type_name:type_name,
        well_id:well_id,
        od:od,
        id:id,
        weight:weight,
        grade:grade,
        connection_type:connection_type,
        classtype:classtype,
        onejoint_length:onejoint_length,
        total_measured_depth:total_measured_depth
      },
      dataType: "json",
      success: function (data) { 
        if(welltype=='ACTUAL'){
          $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.box_tj_length').val(data.box_tj_length.databasevalue);
          $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.pin_tj_length').val(data.pin_tj_length.databasevalue);
        }else{
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.box_tj_length').val(data.box_tj_length.data);
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.pin_tj_length').val(data.pin_tj_length.data);  
        }
       
      }
    });
}

// calculate cumulative length when enter length in bha
$(document).on("blur",'.length',function(){
    var current_index=$(this).closest('tr').index();
    var total_measured_depth=$('#bhadatatable tbody tr:eq(1)').find('.measured_depth').val();
  
    var cumulative_total=0;
    $('.length').each(function(index){
      if($(this).val()!='' && index<current_index){
        cumulative_total =cumulative_total+parseFloat($(this).val());
      }
    });
    var remaining=total_measured_depth-cumulative_total;
    if(parseFloat(cumulative_total)<total_measured_depth){
      $(this).closest('tr').find('.cumulative-length').val(cumulative_total);
      var newindex=current_index+1;
      $('#bhadatatable tbody tr:eq('+newindex+')').find('.length').val(remaining);
      $('#bhadatatable tbody tr:eq('+newindex+')').find('.cumulative-length').val(total_measured_depth);
  
    }else{
      $(this).closest('tr').find('.cumulative-length').val(total_measured_depth);
      $(this).val('')
    }
  })
 
  // get nominal weight when change nominal od
  $(".nominal_od_val li").click(function () { 
    $(this).addClass('active').siblings().removeClass('active');
     var drillcoll = $(this).attr('databasevalue');
     if(well_type=='PLAN'){
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(drillcoll);
     }else{
      $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.od').val(drillcoll);
     }
     var well_id=$('#well').val();
     $.ajax({ 
       type: "GET",                      
       url: "/wells/bhadata/bhacaluculation",                    
       data: {
         drillcoll:drillcoll,
         well_id:well_id
       },
       dataType: "json",
       success: function (data) { 
        $('#weight_head').show();
         $(".weight_val li").remove(); 
        for(i=0;i<data.data.length;i++){
        $('.weight_val').append('<li databasevalue="'+data.data[i].databasevalue+'" collar_weight="'+data.data[i].weight +'">'+ data.data[i].weight+'</li>');
          }
          $(".pipetype_val li").remove(); 
          $(".connectiontype_val li").remove(); 
          $(".tool_od_val li").remove(); 
          $(".one_joint_length").hide(); 
          $("#pipe_head").hide(); 
          $("#connect_head").hide(); 
          $("#tj_head").hide(); 
          $("#one_joint_head").hide(); 
          }
     });
   });

  // get pipe type when change nominal weight
   $(document.body).on("click",".weight_val > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var collar_weight = $(this).attr('databasevalue');  
    var col_weight = $(this).attr('collar_weight');  
    if(well_type=='PLAN'){
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(col_weight);
    }else{
      $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(col_weight);
    }
    $.ajax({ 
      type: "GET",                      
      url: "/wells/bhadata/bha_pipe_calc",                    
      data: {
       collar_weight:collar_weight
      },
      dataType: "json",
      success: function (data) {   
        $('#pipe_head').show();
       $(".pipetype_val li").remove(); 
       for(i=0;i<data.data.length;i++){
         $('.pipetype_val').append('<li pipe_type="'+data.data[i].pipe_type +'">'+ data.data[i].pipe_type+'</li>');
       }
      $(".connectiontype_val li").remove(); 
      $(".tool_od_val li").remove(); 
      $(".one_joint_length").hide(); 
      $("#connect_head").hide(); 
      $("#tj_head").hide(); 
      $("#one_joint_head").hide(); 
    }
    });
  });
  
  // get connection type when change pipe type
$(document.body).on("click",".pipetype_val > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var pipe_type = $(this).attr('pipe_type'); 
    var w_pipe=$('ul.weight_val').find('li.active').attr('databasevalue');
    if(well_type=='PLAN'){
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.pipe_type').val(pipe_type);
    }else{
      $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.pipe_type').val(pipe_type);
    }
    $.ajax({ 
      type: "GET",                      
      url: "/wells/bhadata/bha_Connectpipe_calc",                    
      data: {
        pipe_type:pipe_type,
        w_pipe:w_pipe
      },
      dataType: "json",
      success: function (data) { 
        $('#connect_head').show();
        $(".connectiontype_val li").remove(); 
    for(i=0;i<data.data.length;i++){
    $('.connectiontype_val').append('<li conn_type="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</li>');
        }
      $(".tool_od_val li").remove(); 
      $(".one_joint_length").hide();
      $("#tj_head").hide(); 
      $("#one_joint_head").hide(); 
      }
    });
});

// get tool joint od when change connection type
$(document.body).on("click",".connectiontype_val > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var conn_type = $(this).attr('conn_type'); 
    if(well_type=='PLAN'){
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(conn_type);
    }else{
      $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.connection_type').val(conn_type);
    }
    var w_pipe=$('ul.weight_val').find('li.active').attr('databasevalue');
    var pipe_type=$('ul.pipetype_val').find('li.active').attr('pipe_type');
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
        $('#tj_head').show();
      $(".tool_od_val li").remove(); 
      for(i=0;i<data.data.length;i++){
      $('.tool_od_val').append('<li tool_od="'+data.data[i].data +'">'+ data.data[i].data+'</li>');
          }
      $(".one_joint_length").hide();
      $("#one_joint_head").hide(); 
        }
    });
  });

  //get od and id and show one joint length input
  $(document.body).on("click",".tool_od_val > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var tool_od = $(this).attr('tool_od'); 
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(tool_od);
    var w_pipe=$('ul.weight_val').find('li.active').attr('databasevalue');
    var pipe_type=$('ul.pipetype_val').find('li.active').attr('pipe_type');
    var c_type=$('ul.connectiontype_val').find('li.active').attr('conn_type');
    var nod=$('ul.tool_od_val').find('li.active').attr('tool_od');
    var well_id=$('#well').val();
    var welltype=$('#well_type').val()
    
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
        $('#one_joint_head').show();
        for(i=0;i<data.data.length;i++){
            if(welltype=='ACTUAL'){
            $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
            $('#bhadatatable'+indexid+' tbody tr:eq('+closesttrindex+')').find('.identity').val(data.tool_id[0].data);
            }
            else{
            $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od').val(data.nod);
            $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity').val(data.tool_id[0].data);
            }
        
        } 
        $('.one_joint_length').show();
    }
    });
  });
//get weight when change od in bhaedit
$(document.body).on("click",".nod_edit > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var coll_value = $(this).attr('drillcoll');
    var drillcoll = $(this).attr('databasevalue'); 
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od_edit').val(coll_value);
    var cloesttr_index=$(this).closest('tr').index(); 
    var current_element=$(this);
    var well_id=$('#well').val();
    $.ajax({ 
    type: "GET",                      
    url: "/wells/bhadata/bhacaluculation",                    
    data: {
        drillcoll:drillcoll,
        well_id:well_id
    },
    dataType: "json",
    success: function (data) {   
    $(".weight1_edit li").remove(); 
    $('#coller_weight_head').show();
        for(i=0;i<data.data.length;i++){
        $('.weight1_edit').append('<li databasevalue="'+data.data[i].databasevalue+'" collar_weight="'+data.data[i].weight +'">'+ data.data[i].weight+'</li>');
        }
    $(".pipe_type1_edit li").remove(); 
    $(".connection_type1_edit li").remove(); 
        $(".tool_od1_edit li").remove();  
        $(".one_joint_length").hide(); 
        $('#coller_type_head').hide();
        $('#coller_ctype_head').hide();
        $('#coller_od_head').hide();
        $('#coller_joint_head').hide();
    }

    });
});
//get pipe type when change weight in bha edit
$(document.body).on("click",".weight1_edit > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var collar_weight = $(this).attr('databasevalue');  
    var weight_val = $(this).attr('collar_weight');  
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(weight_val);
    $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/bha_pipe_calc",                    
        data: {
        collar_weight:collar_weight
        },
        dataType: "json",
        success: function (data) {   
        $(".pipe_type1_edit li").remove(); 
        $('#coller_type_head').show();
        for(i=0;i<data.data.length;i++){
            $('.pipe_type1_edit').append('<li pipe_type="'+data.data[i].pipe_type +'">'+ data.data[i].pipe_type+'</li>');
        }
        $(".connection_type1_edit li").remove(); 
            $(".tool_od1_edit li").remove();  
            $(".one_joint_length").hide(); 
            $('#coller_ctype_head').hide();
            $('#coller_od_head').hide();
            $('#coller_joint_head').hide();
        }
    });
});
//get connection type when change pipe type
$(document.body).on("click",".pipe_type1_edit > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var pipe_type = $(this).attr('pipe_type'); 
    var w_pipe=$('ul.weight1_edit').find('li.active').attr('databasevalue');
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
        $(".connection_type1_edit li").remove(); 
        for(i=0;i<data.data.length;i++){
            $('#coller_ctype_head').show();
        $('.connection_type1_edit').append('<li conn_type="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</li>');
        }
        $(".tool_od1_edit li").remove();  
            $(".one_joint_length").hide(); 
            $('#coller_od_head').hide();
            $('#coller_joint_head').hide();
        }

    });
});
//get tool joint od when change connection type
$(document.body).on("click",".connection_type1_edit > li",function () {
    $(this).addClass('active').siblings().removeClass('active');
    var conn_type = $(this).attr('conn_type'); 
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(conn_type);
    var w_pipe=$('ul.weight1_edit').find('li.active').attr('databasevalue');
    var pipe_type=$('ul.pipe_type1_edit').find('li.active').attr('pipe_type');
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
    $(".tool_od1_edit li").remove(); 
    $('#coller_od_head').show();
    for(i=0;i<data.data.length;i++){
    $('.tool_od1_edit').append('<li tool_od="'+data.data[i].data +'">'+ data.data[i].data+'</li>');
    }
    $(".one_joint_length").hide();
    $('#coller_joint_head').hide();
    }

    });
});
//show one joint length when change tool joint od
$(document.body).on("click",".tool_od1_edit > li",function () { 
    $(this).addClass('active').siblings().removeClass('active');
    var tool_od = $(this).attr('tool_od'); 
    $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od_edit').val(tool_od);
    var w_pipe=$('ul.weight1_edit').find('li.active').attr('databasevalue');
    var pipe_type=$('ul.pipe_type1_edit').find('li.active').attr('pipe_type');
    var c_type=$('ul.connection_type1_edit').find('li.active').attr('conn_type');
    var well_id=$('#well').val();
    var nod=$('ul.nod_edit').find('li.active').attr('drillcoll');
    $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/bha_tooljoint_id_calc",                    
        data: {
        tool_od:tool_od,
        w_pipe:w_pipe,
        pipe_type:pipe_type,
        c_type:c_type,
        well_id:well_id,
        nod:nod
        },
        dataType: "json",
        success: function (data) { 
        for(i=0;i<data.data.length;i++){
        // $('.identity').val(data.data[i].tool_id);
            $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity_edit').val(data.tool_id[0].data);
        }
        $('#coller_joint_head').show();
        $('.one_joint_length').show();
        }
    });
});
  