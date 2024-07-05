$( document ).ready(function() {
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    $('#cuttings_density').val(alldata.data.cuttings_density)
    $('#cuttings_size').val(alldata.data.cuttings_size)
    $('#mudweight_hidden').val(alldata.data.mudweight)
    $('#pv_hidden').val(alldata.data.pv)
    $('#yp_hidden').val(alldata.data.yp)
    $('#todepth_hidden').val(alldata.data.todepth)
    $('#original_flowrate').val(flowrate)
    $('#original_rop').val(rop)
    $('#original_cs').val(alldata.data.cuttings_size)
    $('#original_cd').val(alldata.data.cuttings_density)
    $('#original_pv').val(alldata.data.plastic_viscocity)
    $('#original_yp').val(alldata.data.yieldpoint)
    $('#flowrate_userenter').val(alldata.data.flowrate);
    $('#rpm_userenter').val(alldata.data.rpm);
    $('#rop_userenter').val(alldata.data.rop);
    $('#section_name').val(alldata.data.section_name);
    if(alldata.data.unit == 'SI'){
        var pressure = ' kPa';
        var depth = 'm';
        var length = 'm';
        var diameter = 'mm';
        var flowrate = 'LPM';
        var mud_weight = 'g/cc';
        var nozzlesize = 'mm';
        var tfa = 'mm<sup>2</sup>';
        var bhhp = 'hp';
        var hsi = 'hp/in<sup>2</sup>';
        var rop = 'm/hr';
        var impact = 'lbf';
        var jetvelocity = 'ft/sec';
        var viscocity = 'Pa.sec';
        var yeildpoint = 'Pa';
    }
    else{ 
        var pressure = ' psi';
        var depth = ' ft';
        var length = ' ft';
        var diameter = ' in';
        var flowrate = ' GPM';
        var mud_weight = ' ppg';
        var nozzlesize = ' 1/32in';
        var tfa = ' in<sup>2</sup>';
        var bhhp = 'kW';
        var hsi = 'kW/mm<sup>2</sup>';
        var impact = 'N';
        var rop = ' ft/hr';
        var jetvelocity = 'm/sec';
        var viscocity = ' cP';
        var yeildpoint = ' lbf/100ft^2';
    }
    var from_depth
    var todepth
    var totalpipeloss=0
    var totalsurfacelosses=0
    var totalannularpressureloss=0


    Promise.all([surface_loss(alldata),bit_loss(alldata),annular_pressure_loss(alldata)])
    .then(() => {
        pressureloss_chart_first(alldata)
    })
    .catch(error => {
        console.error(error);
    });
    all_summary()
    slip_velocity(alldata)
    bitdepth_calculation(alldata)
    ecdalongwell_calculation(alldata)

})
    // bitdepthcalculation(alldata)
    // ecdalongwellcalculation(alldata)


    


//     var bitloss_nozzle=""
//     if(alldata.data.unit=='API'){
//         bitloss_nozzle +="<table class='table noz-tbl'><thead><tr><th>Nozzle Size<br>"+nozzlesize+"</th></thead><tbody>";
//     }else{
//         bitloss_nozzle +="<table class='table noz-tbl'><thead><tr><th>Nozzle Size<br>"+nozzlesize+"</th></thead><tbody>";
//     }
//     for(var i=0;i<alldata.data.bitpressurelosses.length;i++){
//     for(var j=0;j<alldata.data.bitpressurelosses[i].nozzle_size.length;j++){
//         bitloss_nozzle +='<tr>';
//         bitloss_nozzle +='<td>'+alldata.data.bitpressurelosses[i].nozzle_size[j]+'</td>';
//         bitloss_nozzle +='</tr>';
//     }}
//     bitloss_nozzle +='</tbody></table></div>';
//     $('#nozzle-element').html(bitloss_nozzle);
//     bitloss_values.push(alldata.data.bitpressurelosses)
//     totalpressureloss = totalsurfacelosses+totalpipeloss+totalannularpressureloss+totalbitpressureloss
//     surface_pecentage = totalsurfacelosses/totalpressureloss*100
//     drillstring_pecentage = totalpipeloss/totalpressureloss*100
//     annular_pecentage = totalannularpressureloss/totalpressureloss*100
//     bit_percentage = totalbitpressureloss/totalpressureloss*100


//     annularpressureloss=parseInt(allannularloss,10)
//     surfacelosses=parseInt(totalsurfacelosses,10)
//     pipeloss=parseInt(allpipeloss,10)
//     bitloss=parseInt(totalbitpressureloss,10)
//     summary_values.push(totalsurfacelosses,totalpipeloss,totalbitpressureloss,totalannularpressureloss,totalpressureloss)
//     var pressureloss_datatable="";
//     pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>Pressure Loss Table</h4></tr><tr><th>Pressure loss ({%display_pressureunit request.session.unit%})</th><th>MD({%display_depthunit request.session.unit%})</th></tr></thead><tbody>";
//     for(var i=alldata.data.chartdata.length-1;i>=0;i--){
//     pressureloss_datatable +='<tr><td>'+alldata.data.chartdata[i].x+'</td><td>'+alldata.data.chartdata[i].y+'</td></tr>';
//     }
//     pressureloss_datatable +="</tbody></table></div>";
//     $('#pressureloss_datatable').html(pressureloss_datatable);

//     var rheology_mud_parameters=''
//     rheology_mud_parameters +='<table class="mud-reh-det">'
//     if(alldata.data.unit=='API'){
//         rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+alldata.data.mudweight+mud_weight+'</td>'
//         rheology_mud_parameters +='<th>PV / YP:</th><td>'+alldata.data.pv+viscocity+'/ '+alldata.data.yp+yeildpoint+'</td></tr>'
//         rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+alldata.data.selected_modal+'</td>'
//         rheology_mud_parameters +='<th>n / K:</th><td>'+alldata.data.m+' / '+alldata.data.K+'</td></tr>'
//         rheology_mud_parameters +='</table>'
//         $('#rheology_mud_parameters').html(rheology_mud_parameters)
//         rheology_parameters.push(alldata.data.mudweight,alldata.data.pv,alldata.data.yp,alldata.data.selected_modal,alldata.data.K,alldata.data.m)
//         $('.totalpressure').html(Math.round(totalpressureloss)+pressure)
//     }else{
//         rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+alldata.data.mudweight+mud_weight+'</td>'
//         rheology_mud_parameters +='<th>PV / YP:</th><td>'+alldata.data.pv+viscocity+'/ '+alldata.data.yp+yeildpoint+'</td></tr>'
//         rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+alldata.data.selected_modal+'</td>'
//         rheology_mud_parameters +='<th>n / K:</th><td>'+alldata.data.m+' / '+alldata.data.K+'</td></tr>'
//         rheology_mud_parameters +='</table>'
//         $('#rheology_mud_parameters').html(rheology_mud_parameters)
//         rheology_parameters.push(alldata.data.mudweight,alldata.data.pv,alldata.data.yp,alldata.data.selected_modal,alldata.data.K,alldata.data.m)
//         $('.totalpressure').html(Math.round(totalpressureloss)+pressure)
//     }
//     $('.total_pressure_loss').val(Math.round(totalpressureloss));

//     // var slipvelocity_datatable="";
//     // slipvelocity_datatable += "<div class=' p-3'><table class='popup-presstbl' ><thead><tr><h4 class='phase_det_head'>Slip Velocity Loss Table</h4></tr><tr><th>Velocity(ft/min)</th><th>MD(ft)</th></tr></thead><tbody>";
//     // for(var i=0;i<alldata.data.slipvelocitychart.length;i++){
//     // slipvelocity_datatable +='<tr><td>'+alldata.data.slipvelocitychart[i].x+'</td><td>'+alldata.data.slipvelocitychart[i].y+'</td></tr>';
//     // }
//     // slipvelocity_datatable +="</tbody></table></div>";
//     // slipvelocity_datatable += "<div class=' p-3'><table class='popup-presstbl' ><thead><tr><h4 class='phase_det_head'>Annular Velocity Loss Table</h4></tr><tr><th>Velocity(ft/min)</th><th>MD(ft)</th></tr></thead><tbody>";
//     // for(var i=0;i<alldata.data.annularvelocitychartdata.length;i++){
//     // slipvelocity_datatable +='<tr><td>'+alldata.data.annularvelocitychartdata[i].x+'</td><td>'+alldata.data.annularvelocitychartdata[i].y+'</td></tr>';
//     // }
//     // slipvelocity_datatable +="</tbody></table></div>";
//     // $('#slipvelocity_datatable').html(slipvelocity_datatable);

//     var ecdalongwell_datatable="";
//     ecdalongwell_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>ECD Alonghole Table</h4></tr><tr><th>ECD {%display_densityunit request.session.unit%}</th><th>MD({%display_depthunit request.session.unit%})</th></tr></thead><tbody>";
//     for(var i=0;i<alldata.data.ecdchartdata.length;i++){
//     ecdalongwell_datatable +='<tr><td>'+alldata.data.ecdchartdata[i].x+'</td><td>'+alldata.data.ecdchartdata[i].y+'</td></tr>';
//     }
//     ecdalongwell_datatable +="</tbody></table></div>";
//     $('#ecd_alonghole_datatable').html(ecdalongwell_datatable);
    
//     var ecd_bitdepth_datatable="";
//     ecd_bitdepth_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>ECD Bitdepth Table</h4></tr><tr><th>ECD {%display_densityunit request.session.unit%}</th><th>MD({%display_depthunit request.session.unit%})</th></tr></thead><tbody>";
//     for(var i=0;i<alldata.data.ecdalongwell.length;i++){
//     ecd_bitdepth_datatable +='<tr><td>'+alldata.data.ecdalongwell[i].x+'</td><td>'+alldata.data.ecdalongwell[i].y+'</td></tr>';
//     }
//     ecd_bitdepth_datatable +="</tbody></table></div>";
//     $('#ecd_bitdepth_datatable').html(ecd_bitdepth_datatable);

//     var cutting_concentration_datatable="";
//     cutting_concentration_datatable += "<div class='p-3'><table class='popup-presstbl'><thead><tr><h4 class='phase_det_head'>Cutting Concentration Table</h4></tr><tr><th>Percentage(%)</th><th>MD(ft)</th></tr></thead><tbody>";
//     for(var i=0;i<alldata.data.cuttingsconcentration.length;i++){
//     cutting_concentration_datatable +='<tr><td>'+alldata.data.cuttingsconcentration[i].x+'</td><td>'+alldata.data.cuttingsconcentration[i].y+'</td></tr>';
//     }
//     cutting_concentration_datatable +="</tbody></table></div>";
//     $('#cutting_concentration_datatable').html(cutting_concentration_datatable);

//     pressurelosschart(alldata.data.chartdata,alldata.data.previous_measured_depth,alldata.data.previous_linear)
//     container(surfacelosses,pipeloss,bitloss,annularpressureloss)
//     var min_scale=parseInt(alldata.data.slipvelocitychart[0].x.toFixed());
//     var last_scale = $(alldata.data.annularvelocitychartdata).last()[0]
//     var max_scale=parseInt(last_scale.x.toFixed());
//     if($(alldata.data.ecd_fracturepressure).last()[0].x ==0 && $(alldata.data.ecd_fracturepressure).last()[0].y == 0){
//         var ecd_alonghole_max=parseInt($(alldata.data.ecdalongwellincreased).last()[0].x);
//         var ecd_chart_max=parseInt($(alldata.data.increasedecdchartdata).last()[0].x);
//     }
//     else if($(data.ecd_fracturepressure).last()[0].x <= $(alldata.data.ecdalongwellincreased).last()[0].x){
//         var ecd_alonghole_max=parseInt($(alldata.data.ecdalongwellincreased).last()[0].x);
//         var ecd_chart_max=parseInt($(alldata.data.increasedecdchartdata).last()[0].x);
//     }
//     else{   
//         var ecd_alonghole_max=parseInt($(alldata.data.ecd_fracturepressure).last()[0].x);
//         var ecd_chart_max=parseInt($(alldata.data.ecd_fracturepressure).last()[0].x);
//     }
//     var cutting_min=parseInt(alldata.data.cuttingsconcentration[0].x.toFixed());
//     var cutting_max=parseInt($(alldata.data.cuttingsconcentration).last()[0].x);
    
//     // slipvelocitychart(data.slipvelocitychart,data.annularvelocitychartdata,min_scale,max_scale)
//     // ecdchart(alldata.data.ecdchartdata,alldata.data.previous_measured_depth,alldata.data.mudweight,alldata.data.todepth,ecd_chart_max,alldata.data.increasedecdchartdata,alldata.data.ecd_fracturepressure)
//     // ecdalongwellchart(alldata.data.ecdalongwell,alldata.data.previous_measured_depth,alldata.data.mudweight,alldata.data.todepth,ecd_alonghole_max,alldata.data.ecdalongwellincreased,alldata.data.ecd_fracturepressure)
//     cuttingsconcentration_chart(alldata.data.cuttingsconcentration,cutting_min,cutting_max)
//     transportratiochart(alldata.data.transportratio)
//     ccichart(alldata.data.cci,alldata.data.maxcci)
//     $('#original_mudweight').val(alldata.data.mudweight)
//     if(alldata.data.unit=='API'){
//         $('#ecd_td_without_bitdepth').html(alldata.data.bitdepth_td_without+'(ppg)')
//         $('#ecd_td_with_bitdepth').html(alldata.data.bitdepth_td_with+'(ppg)')
//         $('#ecd_csg_without_bitdepth').html(alldata.data.bitdepth_csg_without+'(ppg)')
//         $('#ecd_csg_with_bitdepth').html(alldata.data.bitdepth_csg_with+'(ppg)')
//         $('#ecd_td_without').html(alldata.data.alongwell_td_without+'(ppg)')
//         $('#ecd_td_with').html(alldata.data.alongwell_td_with+'(ppg)')
//         $('#ecd_csg_without').html(alldata.data.alongwell_csg_without+'(ppg)')
//         $('#ecd_csg_with').html(alldata.data.alongwell_csg_with+'(ppg)')
//     }else{
//         $('#ecd_td_without_bitdepth').html(alldata.data.bitdepth_td_without+'(g/cc)')
//         $('#ecd_td_with_bitdepth').html(alldata.data.bitdepth_td_with+'(g/cc)')
//         $('#ecd_csg_without_bitdepth').html(alldata.data.bitdepth_csg_without+'(g/cc)')
//         $('#ecd_csg_with_bitdepth').html(alldata.data.bitdepth_csg_with+'(g/cc)')
//         $('#ecd_td_without').html(alldata.data.alongwell_td_without+'(g/cc)')
//         $('#ecd_td_with').html(alldata.data.alongwell_td_with+'(g/cc)')
//         $('#ecd_csg_without').html(alldata.data.alongwell_csg_without+'(g/cc)')
//         $('#ecd_csg_with').html(alldata.data.alongwell_csg_with+'(g/cc)')
//     }
    
//     $('#ecd_with_bitdepth').val(alldata.data.bitdepth_td_with);

// });


function pressureloss_chart_first(alldata){
    var flowrate=alldata.data.flowrate;
    var rpm=alldata.data.rpm;
    var rop=alldata.data.rop;
    var bitdepth=alldata.data.todepth;
    var cuttings_density=alldata.data.cuttings_density;
    var cuttings_size=alldata.data.cuttings_size;

    data = {}
    var surface_value = $('#surface_loss_value').val();
    var bit_value = $('#bit_loss_value').val();
    var annular_value = $('#annular_loss_value').val();
    var drillstring_value = $('#drillstring_loss_value').val();
    
    if(($('#torque').val()==undefined | $('#torque').val()=='') && ($('#wob').val()==undefined | $('#wob').val()=='')){
        data.rpm=rpm
        data.flowrate=flowrate
        data.wellphase_id=wellphase_id
        data.section_name=section_name
        data.rop=rop
        data.cuttings_density=cuttings_density
        data.cuttings_size=cuttings_size
        data.bitdepth=bitdepth
        data.surface_value=surface_value
        data.bit_value=bit_value
        data.annular_value = annular_value 
        data.drillstring_value = drillstring_value
    }
    else{
        data.rpm=rpm
        data.flowrate=flowrate
        data.wellphase_id=wellphase_id
        data.section_name=section_name
        data.torque=$('#torque').val()
        data.wob=$('#wob').val()
        data.rop=rop
        data.cuttings_density=cuttings_density
        data.cuttings_size=cuttings_size
        data.bitdepth=bitdepth
        data.surface_value=surface_value
        data.bit_value=bit_value
        data.annular_value = annular_value 
        data.drillstring_value = drillstring_value

    }
    
    $.ajax({
        type: "GET",
        url:"/wells/muddata/pressurelosschart",
        cache: false,  
        data:data,
        success: function(data) {
            pressurelosschart(data.chartdata,data.previous_measured_depth,data.previous_linear) 
            obj['chart_data']=data.chartdata

            var pressureloss_datatable="";
            pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Pressure Loss Table</h4></tr><tr><th>Pressure loss ("+display_pressureunit+")</th><th>MD"+display_depthunit+"</th></tr></thead><tbody>";
            for(var i=data.chartdata.length-1;i>=0;i--){
            pressureloss_datatable +='<tr><td>'+data.chartdata[i].x+'</td><td>'+data.chartdata[i].y+'</td></tr>';
            }
            pressureloss_datatable +="</tbody></table></div>";
            $('#pressureloss_datatable').html(pressureloss_datatable);
        },
        error: function (err) {
            console.log('Error',err)
        }, 
    })
}

function ecdalongwell_calculation(alldata){

    var flowrate=alldata.data.flowrate;
    var rpm=alldata.data.rpm;
    var rop=alldata.data.rop;
    var bitdepth=alldata.data.todepth;
    var cuttings_density=alldata.data.cuttings_density;
    var cuttings_size=alldata.data.cuttings_size;
    $.ajax({
        type: "GET",
        url: "/wells/muddata/ecdalongwell_calculation",
        cache: false,
        data: {
            flowrate:flowrate,
            section_name:section_name,
            wellphase_id:wellphase_id,
            rop:rop,
            bitdepth:bitdepth,
            rpm:rpm,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size
            
        },
        beforeSend: function () {
            
        },
        success: function (data) {
           if($(data.ecd_fracturepressure).last()[0].x ==0 && $(data.ecd_fracturepressure).last()[0].y == 0){
            var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            }
            else if($(data.ecd_fracturepressure).last()[0].x <= $(data.ecdalongwellincreased).last()[0].x){
                var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            }
            else{   
                var ecd_alonghole_max=parseInt($(data.ecd_fracturepressure).last()[0].x);
            }
        
        ecdalongwellchart(data.ecdalongwell,data.previous_measured_depth,data.mudweight,data.todepth,ecd_alonghole_max,data.ecdalongwellincreased,data.ecd_fracturepressure)
        


        },
        error: function (error) {
            console.log(error);
        },
        complete: function () {
        }
    });
}

function bitdepth_calculation(alldata){
    var cuttings_density=alldata.data.cuttings_density;
    var cuttings_size=alldata.data.cuttings_size;
    var bitdepth=alldata.data.todepth;
    var flowrate=alldata.data.flowrate;
    var rpm=alldata.data.rpm;
    var rop=alldata.data.rop;

    $.ajax({
        type: "GET",
        url: "/wells/muddata/ecdbitdepth_calculation",
        cache: false,
        data: {
            flowrate:flowrate,
            section_name:section_name,
            wellphase_id:wellphase_id,
            rop:rop,
            bitdepth:bitdepth,
            rpm:rpm,
            cuttings_density:cuttings_density,
            cuttings_size:cuttings_size,
            torque:$('#torque').val(),
            wob:$('#wob').val(),
            
        },
        beforeSend: function () {
            
        },
        success: function (data) {
        if($(data.ecd_fracturepressure).last()[0].x ==0 && $(data.ecd_fracturepressure).last()[0].y == 0){
            var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            var ecd_chart_max=parseInt($(data.increasedecdchartdata).last()[0].x);
        }
        else if($(data.ecd_fracturepressure).last()[0].x <= $(data.ecdalongwellincreased).last()[0].x){
            var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            var ecd_chart_max=parseInt($(data.increasedecdchartdata).last()[0].x);
        }
        else{   
            var ecd_alonghole_max=parseInt($(data.ecd_fracturepressure).last()[0].x);
            var ecd_chart_max=parseInt($(data.ecd_fracturepressure).last()[0].x);
        }
        ecdchart(data.ecdchartdata,data.previous_measured_depth,data.mudweight,data.todepth,ecd_chart_max,data.increasedecdchartdata,data.ecd_fracturepressure) 


        },
        error: function (error) {
            console.log(error);
        },
        complete: function () {
        }
    });
}

function slip_velocity(alldata){
    var cuttings_density=alldata.data.cuttings_density;
    var cuttings_size=alldata.data.cuttings_size;
    var bitdepth=alldata.data.todepth;
    var flowrate=alldata.data.flowrate;
    var rpm=alldata.data.rpm;
    var rop=alldata.data.rop;
    
    data={}
   
    data.rpm=rpm
    data.flowrate=flowrate
    data.wellphase_id=wellphase_id
    data.section_name=section_name
    data.rop=rop
    data.cuttings_density=cuttings_density
    data.cuttings_size=cuttings_size
    data.bitdepth=bitdepth

    $.ajax({
        type: "GET",
        url:"/wells/muddata/calculate_slipvelocity",
        cache: false,        
        data:data,
        beforeSend: function() {
        },
        success: function(data1) {
            load_chart=true
            // var min_scale=parseInt(data.slipvelocitychart[0].x.toFixed());
            // var last_scale = $(data.annularvelocitychartdata).last()[0];
            // var max_scale=parseInt(last_scale.x.toFixed());
            var slip_data= data1.slipvelocitychart
            obj['slipvelocity']=data1.slipvelocitychart
            var min_scale=parseInt(data1.slipvelocitychart[0].x.toFixed());
            obj['min_scale']=min_scale

            $.ajax({
                type: "GET",
                url: "/wells/muddata/calculate_cci_trans_cutting",
                cache: false,
                data: {
                    slip_data: JSON.stringify(slip_data),
                    flowrate:flowrate,
                    section_name:section_name,
                    wellphase_id:wellphase_id,
                    rop:rop,
                    bitdepth:bitdepth
                    
                },
            
                beforeSend: function () {
                    
                },
                success: function (data) {
                    var cutting_min=parseInt(data.cuttingsconcentration[0].x.toFixed());
                    var cutting_max=parseInt($(data.cuttingsconcentration).last()[0].x);
                    ccichart(data.cci,data.maxcci)
                    cuttingsconcentration_chart(data.cuttingsconcentration,cutting_min,cutting_max)
                    transportratiochart(data.transportratio)
                    
                    
                },
                error: function (error) {
                    // Handle errors, if any
                    console.log(error);
                },
                complete: function () {
                    // Code to be executed after the request completes, regardless of success or failure
                }
            });
            
            var series={
                type: 'spline',
                color: 'rgb(22,96,178)',
                data: data1.slipvelocitychart,
                dashStyle: 'Solid',
                name:'Slip Velocity'
            }
            checkseries=isSeriesExists('Slip Velocity',slipvelocity_chart)
            
            if(checkseries==false){
                
                slipvelocity_chart.addSeries(series)
                slipvelocity_chart.redraw()
            }

           
          
    },
    error: function (err) {
        console.log(err)
    },   
    complete: function(){
        $('#loader').addClass('hidden')
    },
    
});


}

function surface_loss(alldata){
    data = {
        rpm:alldata.data.rpm,
        flowrate:alldata.data.flowrate,
        wellphase_id:wellphase_id,
        section_name:section_name
    }
    return new Promise((resolve, reject) => {
        fetch("/pressureloss/calculatesurfacelosses",{method: 'POST', body:  JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        })
        .then(response => response.json())
        .then(data => {
            resolve(data)
            change_surface.push(data);
            obj['surface']=change_surface
            var totalsurfacelosses=0
            var total_sur=0
            var surface=""
            surface +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Surface Pressure Losses</h4></tr><tr><th>Element</th><th>ID</th><th>Length</th><th>Pressure Drop</th></tr></thead><tbody>"
            for(var i=0;i<data.length;i++){
                surface +='<tr>';
                surface +='<td>'+data[i].type+'</td>';
                surface +='<td>'+data[i].id+' '+display_diameter+'</td>';
                surface +='<td>'+data[i].length+' '+display_depthunit+'</td>';
                surface +='<td>'+Math.round(data[i].pressureloss)+' '+display_pressureunit+'</td>';
                surface +='</tr>'
                total_sur = total_sur + data[i].pressureloss
                totalsurfacelosses=totalsurfacelosses+Math.round(data[i].pressureloss)
                

            }
            surface +='</tbody></table>';
            surface +='<div class="text-center"><div class="text-danger pressure-ttl">Total Surface Pressure Loss   '+totalsurfacelosses+' '+display_pressureunit+'</div></div>'
            $('#surface-loss').html(surface)
            $('#surface_loss_value').val(total_sur)
           
        })
        .catch(error => {
        reject(error); 
        });
    });





}

function annular_pressure_loss(alldata){
    var bitdepth=$('#bitdepth_userenter').val();
    data= {
        csrfmiddlewaretoken: csrf,
        'rpm':alldata.data.rpm,
        'flowrate':alldata.data.flowrate,
        'wellphase_id':wellphase_id,
        'section_name':section_name,
        'torque':$('#torque').val(),
        'wob':$('#wob').val(),
        'bitdepth':bitdepth,
        'rop':alldata.data.rop,
        'cuttings_density':alldata.data.cuttings_density,
        'cuttings_size':alldata.data.cuttings_size
    }
    return new Promise((resolve, reject) => {
        fetch("/wells/muddata/calculate_annular_drillstring_loss",{method: 'POST', body:  JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        })
        .then(response => response.json())
        .then(data => {
            resolve(data)
            allpressure=data.allpressureloss
            var totalannularpressureloss=0
            var totalpipeloss=0
            var total_ann=0
            var total_pipe=0
            annularpressure_values.push(data.allpressureloss,data.type_name,data.bit_od,data.bit_length);
            obj["annular"]=annularpressure_values;
            annuluspressureloss=''
            cumulative_length=1
            annuluspressureloss +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Pressure Loss Result</h4></tr><tr><th></th><th>BHA Element</th><th>OD/ID</th><th>Length</th><th>Cumulative Length</th><th>Drillstring</th><th>Annulus</th><th>Annular flow regime</th></tr></thead><tbody>"
            annuluspressureloss +='<tr bgcolor="#d9d4d4">';
            annuluspressureloss +='<td><span class="OH">OH</span></td>';
            annuluspressureloss +='<td>'+data.type_name+'</td>';
            annuluspressureloss +='<td>'+data.bit_od+' '+display_diameter+'</td>';
            annuluspressureloss +='<td>'+data.bit_length+' '+display_depthunit+'</td>';
            annuluspressureloss +='<td>'+data.bit_length+' '+display_depthunit+'</td>';
            annuluspressureloss +='<td></td>';
            annuluspressureloss +='<td></td>';
            annuluspressureloss +='<td></td>';
            annuluspressureloss +='</tr>';
            for(var i=allpressure.length-1;i>=0;i--){
                cumulative_length=cumulative_length+allpressure[i].length_against
                annuluspressureloss +='<tr>';
                annuluspressureloss +='<td><span class='+allpressure[i].element_type+'>'+allpressure[i].element_type+'</span></td>';
                annuluspressureloss +='<td>'+allpressure[i].element+'</td>';
                annuluspressureloss +='<td>'+allpressure[i].od+' '+display_diameter+'/'+allpressure[i].id+' '+display_diameter+'</td>';
                annuluspressureloss +='<td>'+allpressure[i].length_against.toFixed(0)+' '+display_depthunit+'</td>';
                annuluspressureloss +='<td>'+cumulative_length.toFixed(0)+' '+display_depthunit+'</td>';
                
                annuluspressureloss +='<td>'+Math.round(allpressure[i].drillstringloss)+' '+display_pressureunit+'</td>';
                annuluspressureloss +='<td>'+Math.round(allpressure[i].pressureloss)+' '+display_pressureunit+'</td>';
                annuluspressureloss +='<td>'+allpressure[i].flowregime+'</td>';

                annuluspressureloss +='</tr>'
                total_ann=total_ann+allpressure[i].pressureloss
                total_pipe=total_pipe+allpressure[i].drillstringloss
                totalannularpressureloss=totalannularpressureloss+Math.round(allpressure[i].pressureloss)
                totalpipeloss=totalpipeloss+Math.round(allpressure[i].drillstringloss)

            }
            allannularloss=totalannularpressureloss
            allpipeloss=totalpipeloss
            $('#annular_loss_value').val(total_ann)
            $('#drillstring_loss_value').val(total_pipe)
            annuluspressureloss +='</tbody></table>';
            annuluspressureloss +='<div class="text-center"><div class="pressure-ttl text-danger">Total Annular Pressure Loss   '+allannularloss+' '+display_pressureunit+'</div><div class="pressure-ttl text-danger">Total Drillstring Pressure Loss   '+allpipeloss+' '+display_pressureunit+'</div></div></div>'
            $('#Annular-loss').html(annuluspressureloss)
            obj['annularvelocity']=data.annularvelocitychartdata
            var series={
                type: 'spline',
                color: 'rgb(255,0,0)',
                data: data.annularvelocitychartdata,
                dashStyle: 'Solid',
                name:'Annular Velocity'
            }
            checkseries=isSeriesExists('Annular Velocity',slipvelocity_chart)
            if(checkseries==false){
                slipvelocity_chart.addSeries(series)
            }
            var last_scale = $(data.annularvelocitychartdata).last()[0]
            var max_scale=parseInt(last_scale.x.toFixed());
            obj['max_scale']=max_scale
            getsummary_pressure_loss()
        })
        .catch(error => {
            reject(error); 
        });
    });
}

function all_summary(){
    if(alldata.data.unit == 'SI'){
        var pressure = ' kPa';
    }
    else{ 
        var pressure = ' psi';
    }
    let totalsurfacelosses = parseInt($("#surface_loss_value").val());
    let totalannularpressurelosses = parseInt($("#annular_loss_value").val());
    let totaldrillstringpressurelosses = parseInt($("#drillstring_loss_value").val());
    let totalbitpressurelosses = parseInt($("#bit_loss_value").val());
    totalpressureloss = totalsurfacelosses+totalannularpressurelosses+totaldrillstringpressurelosses+totalbitpressurelosses
    surface_pecentage = totalsurfacelosses/totalpressureloss*100
    drillstring_pecentage = totaldrillstringpressurelosses/totalpressureloss*100
    annular_pecentage = totalannularpressurelosses/totalpressureloss*100
    bit_percentage = totalbitpressurelosses/totalpressureloss*100


    var summary="";
    summary +="<table class='table card p-3 card-mg'>";
    summary +="<thead>";
    summary +="<tr><th><h4 class='text-center phase_det_head'>Summary Of Pressure Loss</h4></th></tr>";
    summary +="</thead>";
    summary +="<tbody>";
    
    if(alldata.data.unit=="API"){
        summary +='<tr><th class="text-danger">Surface Pressure Loss</th><td>'+Math.round(totalsurfacelosses)+pressure+' </td><td>'+surface_pecentage.toFixed()+'% </td></tr>';
        summary +='<tr><th class="text-danger">Drill String Pressure Loss</th><td>'+Math.round(totaldrillstringpressurelosses)+pressure+' </td><td>'+drillstring_pecentage.toFixed()+'%</td></tr>';   
        summary +='<tr><th class="text-danger">Bit Pressure Loss</th><td>'+Math.round(totalbitpressurelosses)+pressure+' </td><td>'+bit_percentage.toFixed()+'%</td></tr>';  
        summary +='<tr><th class="text-danger">Annular Pressure Loss</th><td>'+Math.round(totalannularpressurelosses)+pressure+' </td><td>'+annular_pecentage.toFixed()+'%</td></tr>';  
        summary +='<tr><th class="text-danger">Total Pressure Loss</th><td>'+Math.round(totalpressureloss)+pressure+' </td></tr>';  
    }else{
        summary +='<tr><th class="text-danger">Surface Pressure Loss</th><td>'+Math.round(totalsurfacelosses)+pressure+' </td><td>'+surface_pecentage.toFixed()+'% </td></tr>'; 
        summary +='<tr><th class="text-danger">Drill String Pressure Loss</th><td>'+Math.round(totalpipeloss)+pressure+' </td><td>'+drillstring_pecentage.toFixed()+'%</td></tr>';   
        summary +='<tr><th class="text-danger">Bit Pressure Loss</th><td>'+Math.round(totalbitpressureloss)+pressure+' </td><td>'+bit_percentage.toFixed()+'%</td></tr>';  
        summary +='<tr><th class="text-danger">Annular Pressure Loss</th><td>'+Math.round(totalannularpressureloss)+pressure+' </td><td>'+annular_pecentage.toFixed()+'%</td></tr>';  
        summary +='<tr><th class="text-danger">Total Pressure Loss</th><td>'+Math.round(totalpressureloss)+pressure+' </td></tr>';  
    }
    summary +='</tbody></table>'; 
    $('#summary_pressureloss').html(summary)
}

function bit_loss(alldata){
    // if(alldata.data.unit == 'SI'){
    //     var pressure = ' kPa';
    //     var tfa = 'mm<sup>2</sup>';
    //     var bhhp = 'hp';
    //     var hsi = 'hp/in<sup>2</sup>';
    //     var impact = 'lbf';
    //     var jetvelocity = 'ft/sec';
    // }
    // else{ 
    //     var pressure = ' psi';
    //     var tfa = ' in<sup>2</sup>';
    //     var bhhp = 'kW';
    //     var hsi = 'kW/mm<sup>2</sup>';
    //     var impact = 'N';
    //     var jetvelocity = 'm/sec';

    // }
    // var bitloss=""
    // bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable'><thead><tr><h4 class='phase_det_head'>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
    // for(var i=0;i<alldata.data.bitpressurelosses.length;i++){
    //     bitloss +='<tr>';
    //     if(alldata.data.unit=='API'){
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].tfa_value+tfa+'</td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].bit_pressure_loss.toFixed()+pressure+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].bhhp.toFixed()+bhhp+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].hsi.toFixed(2)+hsi+'</td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].impact_forces.toFixed()+impact+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].jet_velocity.toFixed()+jetvelocity+' </td>';
    //     }else{
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].tfa_value+tfa+'</td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].bit_pressure_loss.toFixed()+pressure+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].bhhp.toFixed()+bhhp+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].hsi.toFixed(2)+hsi+'</td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].impact_forces.toFixed()+impact+' </td>';
    //         bitloss +='<td>'+alldata.data.bitpressurelosses[i].jet_velocity.toFixed()+jetvelocity+' </td>';
    //     }
    //     bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
    //     bitloss +='</tr>';

    //     totalbitpressureloss=alldata.data.bitpressurelosses[i].bit_pressure_loss
    //     $('#bit_loss_value').val(totalbitpressureloss)
    // }      
    // bitloss +='</tbody></table>';
    // bitloss +=`<div class="collapse first"><div class="block__content" id='nozzle-element'></div></div>`;
    // $('#bit-loss').html(bitloss);
    data={
        rpm:alldata.data.rpm,
        flowrate:alldata.data.flowrate,
        wellphase_id:wellphase_id,
        section_name:section_name,
        bitdepth:$('#bitdepth_userenter').val()

    }

    return new Promise((resolve, reject) => {
        fetch("/pressureloss/calculatebitpressureloss",{method: 'POST', body:  JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        })
        .then(response => response.json())
        .then(data => {
            resolve(data)
            obj['fromdepth']=data.fromdepth
            obj['fromdepthtvd']=data.fromdepthtvd
            obj['todepthtvd']=data.todepthtvd
            obj['todepth']=data.todepth
            obj['K']=data.K;
            obj['n']=data.m;
            bitloss_values.push(data.bit_losses)
            obj["bit"]=bitloss_values;
            var bitloss=""
            bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable'><thead><tr><h4 class='phase_det_head'>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
            var bitpressureloss=data.bit_losses
            for(var i=0;i<bitpressureloss.length;i++){
                bitloss +='<tr>';
                bitloss +='<td>'+bitpressureloss[i].tfa_value+' '+display_diameter+'<sup>2</sup></td>';
                bitloss +='<td>'+bitpressureloss[i].bit_pressure_loss.toFixed()+' '+display_pressureunit+'</td>';
                bitloss +='<td>'+bitpressureloss[i].bhhp.toFixed()+' '+display_bhhp+'</td>';
                bitloss +='<td>'+bitpressureloss[i].hsi.toFixed(2)+' '+display_bhhp+'/'+display_diameter+'<sup>2</sup></td>';
                bitloss +='<td>'+bitpressureloss[i].impact_forces.toFixed()+' '+display_impactforce+'</td>';
                bitloss +='<td>'+bitpressureloss[i].jet_velocity.toFixed()+' '+display_depthunit+'/sec</td>';
                bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
                bitloss +='</tr>';
                totalbitpressureloss=bitpressureloss[i].bit_pressure_loss
                $('#bit_loss_value').val(totalbitpressureloss)

            }      

            bitloss +='</tbody></table>';
            bitloss +=`<div class="collapse first"><div class="block__content" id='nozzle-element'></div></div>`;
            $('#bit-loss').html(bitloss);

            var rheology_mud_parameters=''
            rheology_mud_parameters +='<table class="mud-reh-det">'
            rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+data.mudweight+' '+display_densityunit+'</td>'
            rheology_mud_parameters +='<th>PV / YP:</th><td>'+data.pv+' '+display_plastic_viscosity+'/'+data.yp+' '+display_gelstrengthunit+'</td></tr>'
            rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+data.selected_modal+'</td>'
            rheology_mud_parameters +='<th>n / K:</th><td>'+data.m+' / '+data.K+'</td></tr>'
            rheology_mud_parameters +='</table>'
            $('#rheology_mud_parameters').html(rheology_mud_parameters)
        })
        .catch(error => {
        reject(error); 
        });
    });



}

