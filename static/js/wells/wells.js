$(document).ready(function() {
    $('.environment').click(function(){
        var sub_environment = '';
        sub_environment = '<div class="tab">';
        if(this.value=="Onshore"){
        sub_environment +='<p class="on-shore">Onshore Type</p>'
        sub_environment +='<ul class="nav nav-tabs env_sub_type" role="tablist"><li class="nav-item "><a class="nav-link active side-on-lists" onclick="tags_value(this)" data-toggle="tab" href="#standalone_tab" role="tab" aria-selected="false" type="standalone">Standalone</a></li>'
        sub_environment +='<li class="nav-item"><a class="nav-link side-on-lists" onclick="tags_value(this)" data-toggle="tab" href="#padtype_tab" role="tab" aria-selected="true" type="padtype">Pad Type</a></li>'
        }
        else if(this.value=="Offshore"){
        sub_environment +='<p class="on-shore">Offshore Type</p>'
        sub_environment +='<ul class="nav nav-tabs env_sub_type" role="tablist"><li class="nav-item "><a class="nav-link active side-on-lists" onclick="tags_value(this)" data-toggle="tab" href="#standalone_tab" role="tab" aria-selected="false" type="standalone" >Standalone</a></li>'
        sub_environment +='<li class="nav-item"><a class="nav-link side-on-lists" data-toggle="tab" onclick="tags_value(this)" href="#platform_tab" role="tab" aria-selected="true" type="platform">Platform</a></li>'
        sub_environment +='<li class="nav-item"><a class="nav-link side-on-lists" data-toggle="tab" onclick="tags_value(this)" href="#subsea_tab" role="tab" aria-selected="true" type="subsea">Subsea</a></li>'
        }
        else{
        sub_environment +='<p class="on-shore">Offshore Type</p>'
        sub_environment +='<p class="on-shore-swap">Swamp</p>'
        sub_environment +='<div class="tab-pane" id="swamp_tab"><input type="text" id="pad_name" class="form-control on-bottom-space" name="pad_name" placeholder="Pad Name"></div>'
        }
        sub_environment +='</div></ul>'
        sub_environment +='<div class="tab-content"><div class="tab-pane fade show active" id="standalone_tab"></div>'
        sub_environment +='<div class="tab-pane fade" id="subsea_tab"><input type="text" id="cluster_name" class="form-control on-bottom-space" name="cluster_name" placeholder="Cluster Name"></div>'
        sub_environment +='<div class="tab-pane fade" id="padtype_tab"><input type="text" id="pad_name" class="form-control on-bottom-space" name="pad_name" placeholder="Pad Name">'
        sub_environment +='<input type="number" step="any" id="number_of_well_slots_in_pad" class="form-control on-bottom-space" name="number_of_well_slots_in_pad" placeholder="No of Well Slots in Pad">'
        sub_environment +='<input type="text" id="well_slot_no_or_name" class="form-control on-bottom-space" name="well_slot_no_or_name" placeholder="Well Slot No or Name">'
        sub_environment +='</div>'
        sub_environment +='<div class="tab-pane fade" id="platform_tab"><input type="text" id="platform_name" class="form-control on-bottom-space" name="platform_name" placeholder="Platform Name">'
        sub_environment +='<input type="number" step="any" id="number_of_slots_in_platform" class="form-control on-bottom-space" name="number_of_slots_in_platform" placeholder="Number of Slots in Platform">'
        sub_environment +='<input type="number" step="any" id="slot_no" class="form-control" name="slot_no" placeholder="Slot No"></div></div>'
        sub_environment +='<table ><tr ><p class="datu-center">Datum information</p></tr>'
        if(this.value=="Onshore"){
        sub_environment +='<tr><input type="number" step="any" id="ground_elevations" class="form-control ground_elevations on-bottom-space" name="ground_elevation" placeholder="Ground Elevation ('+length_unit+')"></tr>'
        }else if(this.value=="Offshore" || this.value=="Swamp"){
        sub_environment +='<tr><input type="number" step="any" id="water_depth" class="form-control on-bottom-space" name="water_depth" placeholder="Water Depth ('+length_unit+')"></tr>'
        }
        sub_environment +='<tr><input type="number" step="any" id="air_gap" class="form-control on-bottom-space" name="air_gap" placeholder="Air Gap ('+length_unit+')"></tr>'
        sub_environment +='<tr><input type="number" step="any" id="wellhead_to_datum" class="form-control on-bottom-space" name="wellhead_to_datum" placeholder="Wellhead To Datum ('+length_unit+')"></tr>'
        sub_environment +='<tr><input type="number" step="any" id="rkb_wellhead" class="form-control on-bottom-space" name="rkb_wellhead" placeholder="RKB to Wellhead ('+length_unit+')"></tr>'
        sub_environment +='<tr><input type="number" step="any" id="rkb_datum" class="form-control on-bottom-space" name="rkb_datum" placeholder="RKB to Datum ('+length_unit+')"></tr></table>'
    
    
        $('#onshore_elements').html(sub_environment);
        $('#onshore_elements').show();
        var environment_type=$('.tab').find('a.active').attr('type');
        $('#environment_sub_type').val(environment_type);
        if(this.value=="Swamp"){
            $('#environment_sub_type').val('swamp');
        }
    })
})
  