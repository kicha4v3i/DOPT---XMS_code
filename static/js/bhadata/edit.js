$("document").ready(function() {
    var closestindex 
    allvalues = [];

    $('.mudmotor_popup_button').click(function(){
        var bhaelememt_id=$(this).attr('data-id')
        var type_name=$(this).closest('tr').find('#type_name_edit').val();
        var index=$(this).closest('tr').index();
        modalid='mud_motor'+index
        closestindex=index-1;
       var unit = $('.unit').val();
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
             html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations2</h4>'
             html +='</div>'
             html += '<h2 style="text-align: center;">'+type_name+'</h2>'
             html +='<div class="modal-body">'
             html +='<div class="row">'
             html +='<div class="col-5">'
             html +='<h3 style="text-align: center;">Specifications</h3>'
             html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+closestindex+'" value="'+type_name+'"></div></div></div>';
             if(unit == 'API'){
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" value="'+data[0].specifications[0].maximum_flowrate+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" value="'+data[0].specifications[0].minimum_flowrate+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+closestindex+'" value="'+data[0].specifications[0].maximum_rpm+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+closestindex+'" value="'+data[0].specifications[0].minimum_rpm+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(psi) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+closestindex+'" value="'+data[0].specifications[0].no_load_diff_pressure+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(psi)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+closestindex+'" value="'+data[0].specifications[0].max_dp+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(psi)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+closestindex+'" value="'+data[0].specifications[0].recom_dp+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB(lbf)</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+closestindex+'" value="'+data[0].specifications[0].max_wob+'"></div></div></div>';
             }else{
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" value="'+data[0].specifications[0].maximum_flowrate+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" value="'+data[0].specifications[0].minimum_flowrate+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum RPM(rpm)</label></div><div class="col"><input type="text" id="maximum_rpm" class="form-control" name="maximum_rpm'+closestindex+'" value="'+data[0].specifications[0].maximum_rpm+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum RPM(rpm)</label></div><div class="col"><input type="text" id="minimum_rpm" class="form-control" name="minimum_rpm'+closestindex+'" value="'+data[0].specifications[0].minimum_rpm+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">No Load Differential Pressure(kPa) </label></div><div class="col"><input type="text" id="no_load_diff_pressure" class="form-control" name="no_load_diff_pressure'+closestindex+'" value="'+data[0].specifications[0].no_load_diff_pressure+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum DP(kPa)</label></div><div class="col"><input type="text" id="max_dp" class="form-control" name="max_dp'+closestindex+'" value="'+data[0].specifications[0].max_dp+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Recom DP(kPa)</label></div><div class="col"><input type="text" id="recom_dp" class="form-control" name="recom_dp'+closestindex+'" value="'+data[0].specifications[0].recom_dp+'"></div></div></div>';
               html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Max WOB</label></div><div class="col"><input type="text" id="max_wob" class="form-control" name="max_wob'+closestindex+'" value="'+data[0].specifications[0].max_wob+'"></div></div></div>';
             }
             html += '</div>'
             html += '<div class="tab-content">'
             html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
             html +='<h3 style="text-align: center;">Differential Pressure Table</h3>'
             html += '<table class="table diff_pressure_table" id="diff_pressure_table">'
             html += '<thead><tr><th></th><th>Torque</th><th>Differential Pressure</th><th>Action</th></tr></thead>'
             for(var i=0;i<data[0].differntial_pressure.length;i++){
             html += '<tbody><tr id="pressure_row">'
             html += '<td><input type="hidden" name="differntial_pressure'+closestindex+'" value='+data[0].differntial_pressure[i].id+'>'
             html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" value="'+data[0].differntial_pressure[i].torque+'"></td>'
             html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" value="'+data[0].differntial_pressure[i].diff_pressure+'"></td>'
             html += '<td><button type="button" name="add" class="addpressurerows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows_edit iconaction"><i class="fa fa-trash"></i></button></td>'
             html += '</tr>'
             }
             html += '<tr id="pressure_row2" style="display:none">'
             html += '<td><input type="hidden" name="differntial_pressure'+closestindex+'" value="">'
             html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" placeholder="Torque"></td>'
             html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" placeholder="Differential Pressure"></td>'
             html += '<td><button type="button" name="add" class="addpressurerows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows_edit iconaction"><i class="fa fa-trash"></i></button></td>'
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
             $('#mud_motor_edit').append(html);
             $('#mud_motor_edit').show();
             $('#'+modalid).modal('show');
          }
        });
    });

    $(document).on("click",".addpressurerows_edit" , function() {
        console.log("closestindex"+closestindex)
        var html="";
        html +='<tr id="flowraterow">'
        html += '<td><input type="hidden" name="differntial_pressure'+closestindex+'">'
        html += '<td><input type="text" id=" torque" class="form-control torque" name="torque'+closestindex+'" placeholder="Torque"></td>'
        html += '<td><input type="text" id="diff_pressure" class="form-control diff_pressure" name="diff_pressure'+closestindex+'" placeholder="Differential Pressure"></td>'
        html +='<td><button type="button" name="add" class="addpressurerows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deletepressurerows_edit iconaction"><i class="fa fa-trash"></i></button></td>'
        html +="</tr>"
        $(this).closest('tr').after(html);
        $('#diff_pressure_table > tbody > tr:gt(0)').find(".deletepressurerows_edit").show();
    });

    $('.empirical_popup_button').click(function(){
        var bhaelememt_id=$(this).attr('data-id')
        var type_name=$(this).closest('tr').find('#type_name_edit').val();
        var calculation_type=$(this).closest('tr').find('.calculation_type').val();
        var index=$(this).closest('tr').index();
        var unit=$('.unit').val();
        modalid=type_name+index
        closestindex=index-1;
     
        $.ajax({ 
            type: "GET",                      
            url: "/wells/bhadata/getempiricaldata",                    
            data: {
                bhaelememt_id:bhaelememt_id,
            },
            dataType: "json",
            success: function (data) { 
                console.log(data)
                var html = '';
                html +='<div class="modal" id='+modalid+'>'
                html +='<div class="modal-dialog">'
                html +='<div class="modal-content">'
                html +='<div class="modal-header">'
                html +='<h4 class="modal-title">Configure Downhole Tool Specifications and Limitations1</h4>'
                html +='</div>'
                html += '<h2 style="text-align: center;">'+type_name+'</h2>'
                html +='<div class="modal-body">'
                html +='<div class="table-responsive formgroup_b0">'
                html +='<div class="row">'
                html +='<div class="col-6">'
                html +='<h3 style="text-align: center;">Specifications</h3>'
                html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Name</label></div><div class="col"><input type="text" id="name" class="form-control" name="name'+closestindex+'" placeholder="Name" value='+type_name+'></div></div></div>';
                if(unit == 'API'){
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(in)</label></div><div class="col"><input type="text" id="specification_od'+closestindex+'" class="form-control" name="specification_od'+closestindex+'" placeholder="OD" value='+data[0].specifications[0].specification_od+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(in)</label></div><div class="col"><input type="text" id="specification_id'+closestindex+'" class="form-control" name="specification_id'+closestindex+'" placeholder="ID" value='+data[0].specifications[0].specification_id+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(ft)</label></div><div class="col"><input type="text" id="specification_length'+closestindex+'" class="form-control" name="specification_length'+closestindex+'" placeholder="Length" value='+data[0].specifications[0].specification_length+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(GPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate" value='+data[0].specifications[0].minimum_flowrate+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(GPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate" value='+data[0].specifications[0].maximum_flowrate+'></div></div></div>';
                }else{
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">OD(mm)</label></div><div class="col"><input type="text" id="specification_od'+closestindex+'" class="form-control" name="specification_od'+closestindex+'" placeholder="OD" value='+data[0].specifications[0].specification_od+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">ID(mm)</label></div><div class="col"><input type="text" id="specification_id'+closestindex+'" class="form-control" name="specification_id'+closestindex+'" placeholder="ID" value='+data[0].specifications[0].specification_id+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Length(m)</label></div><div class="col"><input type="text" id="specification_length'+closestindex+'" class="form-control" name="specification_length'+closestindex+'" placeholder="Length" value='+data[0].specifications[0].specification_length+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Minimum Flowrate(LPM)</label></div><div class="col"><input type="text" id="minimum_flowrate" class="form-control" name="minimum_flowrate'+closestindex+'" placeholder="Minimum Flowrate" value='+data[0].specifications[0].minimum_flowrate+'></div></div></div>';
                    html += '<div class="col-12"><div class="form-group row"><div class="col col-form-label"><label class="project-edit-name" for="well-name">Maximum Flowrate(LPM)</label></div><div class="col"><input type="text" id="maximum_flowrate" class="form-control" name="maximum_flowrate'+closestindex+'" placeholder="Maximum Flowrate" value='+data[0].specifications[0].maximum_flowrate+'></div></div></div>';
                }
                html += '</div>'
                html += '<div  class="col-6">'
                html += '<h3 style="text-align: center;">Pressure Drop across Tool</h3>'
                html += '<ul class="nav nav-tabs" role="tablist">'
                html += '<li class="nav-item">'
                html += '<a class="nav-link" onclick="change_calculationtype(1,'+closestindex+')" data-toggle="tab" href="#flowrate_tab'+closestindex+'" role="tab" aria-selected="true">Flow Test</a>'
                html += '</li>'
                html += '<li class="nav-item">'
                html += '<a class="nav-link" onclick="change_calculationtype(2,'+closestindex+')" data-toggle="tab" href="#empirical_tab'+closestindex+'" role="tab">Empirical</a>'
                html += '</li>'
                html += '</ul>'
                html += '<div class="tab-content">'
                html += '<div class="tab-pane flowrate_tab fade show active" id=flowrate_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
                html += '<table class="table flowratetable" id="flowratetable">'
                if(unit == 'API'){
                html += '<thead><tr><th>Flowrate(GPM)</th><th>Pressure Drop(psi)</th><th>Action</th></tr></thead>'
                }else{
                html += '<thead><tr><th>Flowrate(LPM)</th><th>Pressure Drop(kPa)</th><th>Action</th></tr></thead>'
                }
                if(calculation_type==1){
                    for(var i=0;i<data[0].pressdroptool.length;i++)
                    {
                        html += '<tbody><tr id="flowraterow">'
                        html += '<td><input type="hidden" name="pressuredrop_tool'+closestindex+'" value='+data[0].pressdroptool[i].id+'><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate" value='+data[0].pressdroptool[i].flowrate+'></td>'
                        html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop" value='+data[0].pressdroptool[i].pressure_drop+'></td>'
                        html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                        html += '</tr>'
                    }
                }
                else{
                    html += '<tbody><tr id="flowraterow">'
                    html += '<td><input type="hidden" name="pressuredrop_tool'+closestindex+'" value=""><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate" value=""></td>'
                    html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop" value=""></td>'
                    html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                    html += '</tr>'
                }
                html += '<tr id="flowraterow2" style="display:none">'
                html += '<td><input type="text" id=" flowrate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate"></td>'
                html += '<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop"></td>'
                html += '<td><button type="button" name="add" class="addflowtestrows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
                html += '</tr></tbody>'
                html +='</table>'
                html += '</div>'
                html += '<div class="tab-pane empirical_tab fade show" id=empirical_tab'+closestindex+' role="tabpanel" aria-labelledby="home-tab">'
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
                html +='<li class="parameter">-</li>'
                html +='<li class="parameter">*</li>'
                html +='<li class="parameter">/</li>'
                html +='<li class="parameter">Power</li>'
                html +='<li class="parameter">Square</li>'
                html +='<li class="parameter">Cube</li>'
                html +='<li class="parameter">Square Root</li>'
                html +='<li class="parameter">Cube Root</li>'
                html +='</ul>'
                // if(calculation_type==2){
                //     // html +='<div id=formula'+closestindex+' contenteditable="true" style="width: 400px;height: 100px;background-color: #0302020f;"><input type="hidden" name=formulatext'+closestindex+' id=formulatext'+closestindex+' value="'+data[0].empirical[0].formula+'"><input type="hidden" id=formula_python_text'+closestindex+' name=formula_python_text'+closestindex+' value='+data[0].empirical[0].formula_python_text+'></div>'
                //     // html += '</div>'
                //     html +='<input type="hidden" name=formulatests id=formulatexts>'
                //     html +='<input type="hidden" name=formulatext'+closestindex+' id=formulatext'+closestindex+' value='+data[0].empirical[0].formula+'>'
                //     html +='<input type="hidden" id=formula_python_text'+closestindex+' name=formula_python_text'+closestindex+' value='+data[0].empirical[0].formula_python_text+'>'
                //     html +='<textarea id="text_formula_edit" class="form-control" value="" data-role="tagsinput" value="mudweight,+,flowrate" ></textarea>'
                // }
                // else{
                // html +='<div id=formula'+closestindex+' contenteditable="true" style="width: 400px;height: 100px;background-color: #0302020f;"><input type="hidden" name=formulatext'+closestindex+' id=formulatext'+closestindex+' value=""><input type="hidden" id=formula_python_text'+closestindex+' name=formula_python_text'+closestindex+' value=""></div>'
                // html += '</div>'
                // }
                html +='<input type="hidden" name=formulatests id=formulatexts>'
                html +='<input type="hidden" name=formulatext'+closestindex+' id=formulatext'+closestindex+'><input type="hidden" id=formula_python_text'+closestindex+' name=formula_python_text'+closestindex+'>'
                html +='<textarea id="text_formula_edit'+closestindex+'" class="form-control text_formula" value="" data-role="tagsinput" ></textarea>'
                html += '</div>'
        
                html += '</div>'
                html += '</div>'
                html += '</div>'
                html += '</div>'
                
                html += '<div class="modal-footer"><button type="button" class="btn btn-danger" data-id='+closestindex+' data-modal='+modalid+' data-dismiss="rss_inputs" id="modal-close" >Close</button></div> '
                html += '</div>'
                html += '</div>'
                html +='</div>'
                $('#flowrateempiricalmodal').append(html);
                if(calculation_type==2){
                $('#formula'+closestindex).append(data[0].empirical[0].formula);
                }
                $('#flowrateempiricalmodal').show();
                $('#'+modalid).modal('show');

                $(document).ready(function() {
                    if(data[0].empirical.length > 0){
                        var tagsValue = (data[0].empirical[0].formula).split(",");
                        console.log("tagsValue"+tagsValue)
                        for(var i=-1 ;i<=tagsValue.length;i++){
                            var tagInputEle = $('#text_formula_edit'+closestindex);
                            tagInputEle.tagsinput('add', tagsValue[i]);
                        }
                        allvalues.push(data[0].empirical[0].formula);
                        $('.bootstrap-tagsinput input').addClass('bootstrap_test');
                        $(".bootstrap-tagsinput input").prop("type", "number");
                        $('.bootstrap-tagsinput').addClass('empirical_label_edit'+closestindex+'');

                        $('.bootstrap_test').on('blur',function(){
                        var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
                        $('#formulatext'+closestindex).val(allvalues)
                        $('#formula_python_text'+closestindex).val(test)
                        })  
                    }
                });
        
          
            }
        });
    })

    $(document).on("click",".addflowtestrows_edit" , function() {
        var html="";
        html +='<tr id="flowraterow">'
        html +='<td><input type="hidden" name="pressuredrop_tool'+closestindex+'"><input type="text" id="florate" class="form-control flowrate" name="flowrate'+closestindex+'" placeholder="Flowrate"></td>'
        html +='<td><input type="text" id="pressure_drop" class="form-control pressure_drop" name="pressure_drop'+closestindex+'" placeholder="Pressure Drop"></td>'
        html +='<td><button type="button" name="add" class="addflowtestrows_edit iconaction"><i class="fa fa-plus"></i></button><button type="button" name="add" class="deleteflowtestrow iconaction"><i class="fa fa-trash"></i></button></td>'
        html +="</tr>"
        $(this).closest('tr').after(html);
        $('#flowratetable > tbody > tr:gt(0)').find(".deleteflowtestrow").show();
    });

    
    var previous_index
    $('body').on('click','.parameter',function(){
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
            var tagInputEle = $('#text_formula_edit'+closestindex)
            tagInputEle.tagsinput('add','²');
            var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
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
            var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
            
            $('#formula'+closestindex).html(newformula)
            var newcurrenttext_format=currenttext_format+"<sup>3</sup>"
            allvalues.push('³');
            $('#formulatext'+closestindex).val(allvalues)
            var newformula_python_text=formula_python_text+'**3'
            $('#formula_python_text'+closestindex).val(test)
            previous_operator=parameter_name
            var tagInputEle =$('#text_formula_edit'+closestindex) 
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
            var tagInputEle = $('#text_formula_edit'+closestindex) 
            tagInputEle.tagsinput('add','√');
            var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
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
            var tagInputEle = $('#text_formula_edit'+closestindex)
            tagInputEle.tagsinput('add','∛');
            var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
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
                  var tagInputEle = $('#text_formula_edit'+closestindex)
                  tagInputEle.tagsinput('add',symbol);
                }
                else if(previous_operator=='Cube Root'){
                  var newcurrenttext_format=currenttext_format+symbol
                  var newformula_python_text=formula_python_text+symbol+"**(1/3)"
                  var tagInputEle = $('#text_formula_edit'+closestindex)
                  tagInputEle.tagsinput('add',symbol);
                }else{
                  var newcurrenttext_format=currenttext_format+symbol
                  var newformula_python_text=formula_python_text+symbol
                  var tagInputEle = $('#text_formula_edit'+closestindex)
                   tagInputEle.tagsinput('add',symbol);
                }
                var tagInputEle = $('#text_formula_edit'+closestindex)
                tagInputEle.tagsinput('add',symbol);
                allvalues.push(symbol);
                var test= $('.empirical_label_edit'+closestindex+' .label' ).text();
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
            $(this).closest('div').find('.bootstrap-tagsinput').addClass('empirical_label_edit'+closestindex+'');
      
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
            var test= $('.empirical_label_edit'+dataid+' .label' ).text();
            $('#formula'+dataid).html(newformula)
            allvalues.push('²');
            $('#formulatext'+dataid).val(allvalues)
            $('#formula_python_text'+dataid).val(test)
            previous_operator=parameter_name
      
          }
          else if(parameter_name=="Cube"){
            var newformula=currenttext+"<sup>3</sup>"
            var test= $('.empirical_label_edit'+dataid+' .label' ).text();
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
                var test= $('.empirical_label_edit'+dataid+' .label' ).text();
      
      
                $('#formulatext'+dataid).val(allvalues)
                $('#formula_python_text'+dataid).val(test)  
            }
            previous_operator=parameter_name
          }
          $('.bootstrap-tagsinput input').addClass('bootstrap_test');
          $(".bootstrap-tagsinput input").prop("type", "number");
          $(this).closest('div').find('.bootstrap-tagsinput').addClass('empirical_label_edit'+dataid+'');
      
          $('.bootstrap_test').on('blur',function(){
              var test= $('.empirical_label_edit'+dataid+' .label' ).text();
              $('#formulatext'+dataid).val(allvalues)
              $('#formula_python_text'+dataid).val(test)
          })
      
        }
    })

    $("#drillpipe_nod_edit").change(function () { 
      var normal_od=$(this).val();
      $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/getweight_drillpipe",                    
        data: {
          normal_od:normal_od
        },
        dataType: "json",
        success: function (data) { 
          $(".drillpipe_weight_edit option").remove();
          $('.drillpipe_weight_edit').append('<option value="">Weight</option>');
          for(i=0;i<data.data.length;i++){
            $('.drillpipe_weight_edit').append('<option value="'+data.data[i].weight +'">'+ data.data[i].weight+'</option>');
          }
          $('.drillpipe_weight_edit').select2('open');
        }
  
      });
    });
    $(document.body).on("click",".drillpipe_weight_edit > li",function () { 
      $(this).addClass('active').siblings().removeClass('active');
      var drillpipe_weight = $(this).attr('databasevalue');  
      var drillpipe_weight_val = $(this).attr('drillpipe_weight');  
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.coll_weight').val(drillpipe_weight_val);
      var normal_od=$('ul.drillpipe_nod_edit').find('li.active').attr('databasevalue');
      $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/getgrade_drillpipe",                    
        data: {
          drillpipe_weight:drillpipe_weight,
          normal_od:normal_od
        },
        dataType: "json",
        success: function (data) { 
          $(".drillpipe_grade_edit li").remove();
          $('#pipe_grade_head').show();
          for(i=0;i<data.data.length;i++){
            $('.drillpipe_grade_edit').append('<li drillpipe_grade="'+data.data[i].steel_grade +'">'+ data.data[i].steel_grade+'</li>');
          }
          $(".drillpipe_jointtype_edit li").hide(); 
          $(".drillpipe_jointod_edit li").hide(); 
          $(".drillpipe_class_edit li").hide(); 
          $(".drillpipe_onejoint_length_edit").hide(); 
          $('#pipe_joint_head').hide();
          $('#pipe_od_head').hide();
          $('#pipe_class_head').hide();
          $('#pipe_one_joint_head').hide();
            
        }
      });
    });
    $("#drillpipe_grade_edit").change(function () { 
      var drillpipe_grade = $(this).val();  
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.grade').val(drillpipe_grade);
      var normal_od=$(this).closest('tr').find('.drillpipe_nod_edit').val();
      var drillpipe_weight=$(this).closest('tr').find('.drillpipe_weight_edit').val();
   
      $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/getjointtype_drillpipe",                    
        data: {
          drillpipe_weight:drillpipe_weight,
          normal_od:normal_od,
          drillpipe_grade:drillpipe_grade
        },
        dataType: "json",
        success: function (data) { 
          $(".drillpipe_jointtype_edit option").remove(); 
          $('.drillpipe_jointtype_edit').append('<option value="">Type</option>');
          for(i=0;i<data.data.length;i++){
            $('.drillpipe_jointtype_edit').append('<option value="'+data.data[i].connection_type +'">'+ data.data[i].connection_type+'</option>');
        }
        $('.drillpipe_jointtype_edit').select2('open');
        }
      });
    });
    $(document.body).on("click",".drillpipe_jointtype_edit > li",function () { 
      $(this).addClass('active').siblings().removeClass('active');
      var drillpipe_jointtype = $(this).attr('drillpipe_jointtype');  
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.connection_type').val(drillpipe_jointtype);
      var normal_od=$('ul.drillpipe_nod_edit').find('li.active').attr('databasevalue');
      console.log(normal_od)
      var nod=$('ul.drillpipe_nod_edit').find('li.active').attr('normal_od');
      var drillpipe_weight=$('ul.drillpipe_weight_edit').find('li.active').attr('databasevalue');
      var drillpipe_grade=$('ul.drillpipe_grade_edit').find('li.active').attr('drillpipe_grade');
      $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/getjointod_drillpipe",                    
        data: {
          drillpipe_weight:drillpipe_weight,
          normal_od:normal_od,
          drillpipe_grade:drillpipe_grade,
          drillpipe_jointtype:drillpipe_jointtype,
          well_id:well_id,
          nod:nod
        },
        dataType: "json",
        success: function (data) { 
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.identity_edit').val(data.data[0][0].data);
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_od_edit').val(normal_od);
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.database_weight_edit').val(drillpipe_weight);
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.od_edit').val(data.nod);
          $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_id').val(data.tool_id.data);
          $(".drillpipe_jointod_edit li").remove(); 
          $('#pipe_od_head').show();
          for(i=0;i<data.data.length;i++){
            $('.drillpipe_jointod_edit').append('<li drillpipe_jointod="'+data.data[i][1].data+'">'+ data.data[i][1].data+'</li>');
          }
          $(".drillpipe_class_edit li").hide(); 
          $(".drillpipe_onejoint_length_edit").hide();
          $('#pipe_class_head').hide();
          $('#pipe_one_joint_head').hide();
        }
      });
    });
    $(document.body).on("click",".drillpipe_jointod_edit > li",function () { 
      $(this).addClass('active').siblings().removeClass('active');
      var drillpipe_jointod = $(this).attr('drillpipe_jointod');  
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.tool_od').val(drillpipe_jointod);
      var normal_od=$('ul.drillpipe_nod_edit').find('li.active').attr('normal_od');
      var drillpipe_weight=$('ul.drillpipe_weight_edit').find('li.active').attr('drillpipe_weight');
      var drillpipe_grade=$('ul.drillpipe_grade_edit').find('li.active').attr('drillpipe_grade');
      var drillpipe_jointtype=$('ul.drillpipe_jointtype_edit').find('li.active').attr('drillpipe_jointtype');
      $(".drillpipe_class_edit li").removeClass('active');
      $(".drillpipe_class_edit li").show();
      $(".drillpipe_onejoint_length_edit").hide();
      $('#pipe_class_head').show();
      $('#pipe_one_joint_head').hide();
      $.ajax({ 
        type: "GET",                      
        url: "/wells/bhadata/getclass_drillpipe",                    
        data: {
          drillpipe_weight:drillpipe_weight,
          normal_od:normal_od,
          drillpipe_grade:drillpipe_grade,
          drillpipe_jointtype:drillpipe_jointtype,
          drillpipe_jointod:drillpipe_jointod
        },
        dataType: "json",
        success: function (data) { 
          $(".drillpipe_class_edit li").remove(); 
          for(i=0;i<data.data.length;i++){
            $('.drillpipe_class_edit').append('<li classtype="'+data.data[i].class_type +'">'+ data.data[i].class_type+'</li>');
          }
        }
      });
    });
    $(document.body).on("click",".drillpipe_class_edit > li",function () { 
      $(this).addClass('active').siblings().removeClass('active');
      var classtype=$(this).attr('classtype');
      $('#bhadatatable tbody tr:eq('+closesttrindex+')').find('.classtype').val(classtype);
      $('#pipe_one_joint_head').show();
      $('.drillpipe_onejoint_length_edit').show();
    });
})
function change_calculationtype(val,index){
  var newindex=index+1
 $('#bhadatatable').find('tr:eq('+newindex+')').find('.calculation_type').val(val)
} 