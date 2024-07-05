$(".final_data").on("click",function(){
    var flowrate=$('#flowrate_userenter').val();
    var rpm=$('#rpm_userenter').val();
    var rop=$('#rop_userenter').val();
    var bitdepth=$('#bitdepth_userenter').val();
    var surface_pressure=$('.total_pressure_loss').val();
    var ecd=$('#ecd_with_bitdepth').val();
    var section_name=$('.wellphase_sidemenu.active').attr('data-id');
    var wellphase_id=$('.wellphase_sidemenu.active').attr('wellphase_id');
    var well_id=$('#well_id').val();
    var pressure_data=$('#pressureloss_datatable').val();
    $.ajax({
        type: "GET",
        url:"/wells/muddata/planfinal_data",
        cache: false,        

        data:{
            flowrate:flowrate,
            rpm:rpm,
            rop:rop,
            well_id:well_id,
            section_name:section_name,
            wellphase_id:wellphase_id,
            bitdepth:bitdepth,
            surface_pressure:surface_pressure,
            ecd:ecd
        },
        
        success: function(data) {
            console.log(data);
        }
    })
})


$( ".change_unit" ).on( "click", function(){

    unit_change(obj)
});

function unit_change(obj){
    var flowrate_val=$('.flowrate').val();
    var rop_val=$('#rop_userenter').val();
    if(obj.unit == 'API'){
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
        $('.flowrate').val((flowrate_val*3.78).toFixed());
        $('#rop_userenter').val((rop_val/3.281).toFixed(2));
        $(".flowrate_lable").html('Flowrate (LPM)');
        $(".rop_lable").html('ROP (m/hr)');
        $(".bitdepth_lable").html('Bit Depth (m)');
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
        $('.flowrate').val((flowrate_val*0.2647).toFixed());
        $('#rop_userenter').val((rop_val*3.281).toFixed(2));
        $(".flowrate_lable").html('Flowrate (GPM)');
        $(".rop_lable").html('ROP (ft/hr)');
        $(".bitdepth_lable").html('Bit Depth (ft)');
    }
    
        var totalpipeloss=0
        var totalsurfacelosses=0
        var totalannularpressureloss=0

            var phasedetails=''
            phasedetails +="<table class='hyd-from'><thead><tr><th><span class='sectiondetails'>From </span></th><th><span  class='sectiondetails'>To</span></th></tr><tr><th>MD / TVD</th><th>MD / TVD</th></tr></thead>"
            phasedetails +="<tbody><tr><td><span class='sectiondetails_value'>"+(obj.fromdepth).toFixed()+depth+"/"+(obj.fromdepthtvd).toFixed()+depth+"</span></td><td><span class='sectiondetails_value'>"+(obj.todepth).toFixed()+depth+'/'+(obj.todepthtvd).toFixed()+depth+'</span></td></tr></tbody></table>'
            $('#phase_details').html(phasedetails)

            var surface=""
            surface +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Surface Pressure Losses</h4></tr><tr><th>Element</th><th>ID</th><th>Length</th><th>Pressure Drop</th></tr></thead><tbody>"
            for(var i=0;i<obj.surface[0].length;i++){
                surface +='<tr>';
                surface +='<td>'+obj.surface[0][i].type+'</td>';
                if(obj.unit == 'API'){
                    surface +='<td>'+(obj.surface[0][i].id /0.03937008).toFixed(2)+diameter+'</td>';
                    surface +='<td>'+(obj.surface[0][i].length/3.281).toFixed(2)+length+'</td>';
                    surface +='<td>'+(obj.surface[0][i].pressureloss*6.894757).toFixed()+pressure+'</td>';
                    totalsurfacelosses += obj.surface[0][i].pressureloss*6.894757
                    // surface +='</tr>'
                }
                else{
                    surface +='<td>'+(obj.surface[0][i].id *0.03937008).toFixed(2)+diameter+'</td>';
                    surface +='<td>'+(obj.surface[0][i].length*3.281).toFixed(2)+length+'</td>';
                    surface +='<td>'+(obj.surface[0][i].pressureloss/6.894757).toFixed()+pressure+'</td>';
                    totalsurfacelosses += obj.surface[0][i].pressureloss/6.894757
                }
                surface +='</tr>'   
            }
            surface +='</tbody></table>';
            surface +='<div class="text-center"><div class="text-danger pressure-ttl">Total Surface Pressure Loss   '+(totalsurfacelosses).toFixed()+pressure+'</div></div>'
            
            $('#surface-loss').html(surface)
            
            annuluspressureloss=''
            cumulative_length=1
            annuluspressureloss +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Pressure Loss Result</h4></tr><tr><th></th><th>BHA Element</th><th>OD/ID</th><th>Length</th><th>Cumulative Length</th><th>Drillstring</th><th>Annulus</th><th>Annular flow regime</th></tr></thead><tbody>"
            annuluspressureloss +='<tr bgcolor="#d9d4d4">';
            annuluspressureloss +='<td><span class="OH">OH</span></td>';
            if(obj.unit=='API'){
                annuluspressureloss +='<td>'+obj.annular[1]+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[2]/0.03937008).toFixed(2)+diameter+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[3]/3.281).toFixed(2)+length+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[3]/3.281).toFixed(2)+length+'</td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='</tr>';
                for(var i=obj.annular[0].length-1;i>=0;i--){
                    cumulative_length=cumulative_length+obj.annular[0][i].length_against/3.281
                    annuluspressureloss +='<tr>';
                    annuluspressureloss +='<td><span class='+obj.annular[0][i].element_type+'>'+obj.annular[0][i].element_type+'</span></td>';
                    annuluspressureloss +='<td>'+obj.annular[0][i].element+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].od/0.03937008).toFixed(2)+diameter+'/'+(obj.annular[0][i].id/0.03937008).toFixed(2)+diameter+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].length_against/3.281).toFixed(0)+length+'</td>';
                    annuluspressureloss +='<td>'+(cumulative_length).toFixed(0)+length+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].drillstringloss*6.894757).toFixed(0)+pressure+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].pressureloss*6.894757).toFixed(0)+pressure+'</td>';
                    annuluspressureloss +='<td>'+obj.annular[0][i].flowregime+'</td>';
    
                    annuluspressureloss +='</tr>'
                    totalannularpressureloss += obj.annular[0][i].drillstringloss*6.894757
                    totalpipeloss += obj.annular[0][i].drillstringloss*6.894757
    
                }
            }
            else{
                annuluspressureloss +='<td>'+obj.annular[1]+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[2]*0.03937008).toFixed(2)+diameter+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[3]*3.281).toFixed(2)+length+'</td>';
                annuluspressureloss +='<td>'+(obj.annular[3]*3.281).toFixed(2)+length+'</td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='<td></td>';
                annuluspressureloss +='</tr>';
                for(var i=obj.annular[0].length-1;i>=0;i--){
                    cumulative_length=cumulative_length+obj.annular[0][i].length_against*3.281
                    annuluspressureloss +='<tr>';
                    annuluspressureloss +='<td><span class='+obj.annular[0][i].element_type+'>'+obj.annular[0][i].element_type+'</span></td>';
                    annuluspressureloss +='<td>'+obj.annular[0][i].element+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].od*0.03937008).toFixed(2)+diameter+'/'+(obj.annular[0][i].id*0.03937008).toFixed(2)+diameter+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].length_against*3.281).toFixed(0)+length+'</td>';
                    annuluspressureloss +='<td>'+(cumulative_length).toFixed(0)+length+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].drillstringloss/6.894757).toFixed(0)+pressure+'</td>';
                    annuluspressureloss +='<td>'+(obj.annular[0][i].pressureloss/6.894757).toFixed(0)+pressure+'</td>';
                    annuluspressureloss +='<td>'+obj.annular[0][i].flowregime+'</td>';
    
                    annuluspressureloss +='</tr>'
                    totalannularpressureloss += obj.annular[0][i].pressureloss/6.894757
                    totalpipeloss += obj.annular[0][i].drillstringloss/6.894757
    
                }
            }
            allannularloss=totalannularpressureloss
            allpipeloss=totalpipeloss
            annuluspressureloss +='</tbody></table>';
            annuluspressureloss +='<div class="text-center"><div class="pressure-ttl text-danger">Total Annular Pressure Loss   '+(allannularloss).toFixed()+pressure+'</div><div class="pressure-ttl text-danger">Total Drillstring Pressure Loss   '+(allpipeloss).toFixed()+pressure+'</div></div></div>'
            $('#Annular-loss').html(annuluspressureloss)


            
         
            var bitloss=""
            bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable'><thead><tr><h4 class='phase_det_head'>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
            for(var i=0;i<obj.bit[0].length;i++){
                if(obj.unit=='API'){
                    bitloss +='<tr>';
                    bitloss +='<td>'+(obj.bit[0][i].tfa_value*634.09).toFixed(2)+tfa+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].bit_pressure_loss*6.894757).toFixed()+pressure+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].bhhp/1000*746).toFixed()+bhhp+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].hsi).toFixed(2)+hsi+' </td>';
                    bitloss +='<td>'+(obj.bit[0][i].impact_forces/0.2248).toFixed()+impact+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].jet_velocity/3.281).toFixed()+jetvelocity+'</td>';
                    bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
                    bitloss +='</tr>';
                    totalbitpressureloss=obj.bit[0][i].bit_pressure_loss*6.894757
                }
                else{
                    bitloss +='<tr>';
                    bitloss +='<td>'+(obj.bit[0][i].tfa_value/634.09).toFixed(2)+'('+tfa+')</td>';
                    bitloss +='<td>'+(obj.bit[0][i].bit_pressure_loss/6.894757).toFixed()+pressure+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].bhhp*1000/746).toFixed()+bhhp+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].hsi).toFixed(2)+hsi+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].impact_forces*0.2248).toFixed()+impact+'</td>';
                    bitloss +='<td>'+(obj.bit[0][i].jet_velocity*3.281).toFixed()+jetvelocity+'</td>';
                    bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
                    bitloss +='</tr>';
                    totalbitpressureloss=obj.bit[0][i].bit_pressure_loss/6.894757
                }
            }      
            bitloss +='</tbody></table>';
            bitloss +=`<div class="block collapse first"><div class="block__content" id='nozzle-element'></div></div>`;
            $('#bit-loss').html(bitloss);

            var bitloss_nozzle=""
            if(obj.unit=='API'){
                bitloss_nozzle +='<table class="table noz-tbl"><thead><tr><th>Nozzle Size('+nozzlesize+')</th></thead><tbody>';
            }
            else{  
                bitloss_nozzle +='<table class="table noz-tbl"><thead><tr><th>Nozzle Size('+nozzlesize+')</th></thead><tbody>';
            }
            for(var i=0;i<obj.bit[0].length;i++){
            for(var j=0;j<obj.bit[0][i].nozzle_size.length;j++){
                bitloss_nozzle +='<tr>';
                bitloss_nozzle +='<td>'+obj.bit[0][i].nozzle_size[j]+'</td>';
                bitloss_nozzle +='</tr>';
            }}
            bitloss_nozzle +='</tbody></table></div>';
            $('#nozzle-element').html(bitloss_nozzle);


            totalpressureloss = totalsurfacelosses+totalpipeloss+totalannularpressureloss+totalbitpressureloss
            surface_pecentage = totalsurfacelosses/totalpressureloss*100
            drillstring_pecentage = totalpipeloss/totalpressureloss*100
            annular_pecentage = totalannularpressureloss/totalpressureloss*100
            bit_percentage = totalbitpressureloss/totalpressureloss*100

            var summary="";
            summary +="<table class='table card p-3 card-mg'>";
            summary +="<thead>";
            summary +="<tr><th><h4 class='text-center phase_det_head'>Summary Of Pressure Loss</h4></th></tr>";
            summary +="</thead>";
            summary +="<tbody>";
            summary +='<tr><th class="text-danger">Surface Pressure Loss</th><td>'+(totalsurfacelosses).toFixed()+pressure+'</td><td>'+surface_pecentage.toFixed()+'% </td></tr>'; 
            summary +='<tr><th class="text-danger">Drill String Pressure Loss</th><td>'+(totalpipeloss).toFixed()+pressure+'</td><td>'+drillstring_pecentage.toFixed()+'%</td></tr>';   
            summary +='<tr><th class="text-danger">Bit Pressure Loss</th><td>'+(totalbitpressureloss).toFixed()+pressure+'</td><td>'+bit_percentage.toFixed()+'%</td></tr>';  
            summary +='<tr><th class="text-danger">Annular Pressure Loss</th><td>'+(totalannularpressureloss).toFixed()+pressure+'</td><td>'+annular_pecentage.toFixed()+'%</td></tr>';  
            summary +='<tr><th class="text-danger">Total Pressure Loss</th><td>'+(totalpressureloss).toFixed()+pressure+'</td></tr>';  
 

            summary +='</tbody></table>'; 
            $('#summary_pressureloss').html(summary)
            annularpressureloss=parseInt(allannularloss,10)
            surfacelosses=parseInt(totalsurfacelosses,10)
            pipeloss=parseInt(allpipeloss,10)
            bitloss=parseInt(totalbitpressureloss,10)
            var pressureloss_datatable="";
            var chart_details=[];
            var slipvelocity_data=[];
            var annularvelocity_data=[];
            if (obj.unit=='API'){
                pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Pressure Loss Table</h4></tr><tr><th>Pressure loss (kPa)</th><th>MD(m)</th></tr></thead><tbody>";
                for(var i=obj.chart_data.length-1;i>=0;i--){
                    pressureloss_datatable +='<tr><td>'+(obj.chart_data[i].x/6.894757).toFixed()+'</td><td>'+obj.chart_data[i].y+'</td></tr>';
                    chart_details.push({'x':obj.chart_data[i].x/6.894757,'y':obj.chart_data[i].y});
                }
                for(var i=obj.slipvelocity.length-1;i>=0;i--){
                    slipvelocity_data.push({'x':obj.slipvelocity[i].x,'y':obj.slipvelocity[i].y/3.281})
                }
                for(var i=obj.annularvelocity.length-1;i>=0;i--){
                    annularvelocity_data.push({'x':obj.annularvelocity[i].x,'y':obj.annularvelocity[i].y/3.281})
                }
            }else{
                pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Pressure Loss Table</h4></tr><tr><th>Pressure loss (psi)</th><th>MD(ft)</th></tr></thead><tbody>";
                for(var i=obj.chart_data.length-1;i>=0;i--){
                    pressureloss_datatable +='<tr><td>'+(obj.chart_data[i].x*6.894757).toFixed()+'</td><td>'+obj.chart_data[i].y+'</td></tr>';
                    chart_details.push({'x':obj.chart_data[i].x*6.894757,'y':obj.chart_data[i].y});
                }
                for(var i=obj.slipvelocity.length-1;i>=0;i--){
                    slipvelocity_data.push({'x':obj.slipvelocity[i].x,'y':obj.slipvelocity[i].y*3.281})
                }
                for(var i=obj.annularvelocity.length-1;i>=0;i--){
                    annularvelocity_data.push({'x':obj.annularvelocity[i].x,'y':obj.annularvelocity[i].y*3.281})
                }
            }
            pressureloss_datatable +="</tbody></table></div>";
            $('#pressureloss_datatable').html(pressureloss_datatable);

            var rheology_mud_parameters=''
            rheology_mud_parameters +='<table class="mud-reh-det">'
            if(obj.unit == 'API'){
                rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+(obj.mudweight/8.345).toFixed(2)+'('+mud_weight+')</td>'
                rheology_mud_parameters +='<th>PV / YP:</th><td>'+(obj.pv/1000).toFixed(2)+'('+viscocity+')/ '+(obj.yp/0.4788).toFixed(2)+'('+yeildpoint+')</td></tr>'
                rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+obj.selected_model+'</td>'
                rheology_mud_parameters +='<th>n / K:</th><td>'+(obj.n).toFixed(2)+' / '+(obj.K).toFixed(2)+'</td></tr>'
            }
            else{
                rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+(obj.mudweight*8.345).toFixed(2)+'('+mud_weight+')</td>'
                rheology_mud_parameters +='<th>PV / YP:</th><td>'+(obj.pv*1000).toFixed(2)+'('+viscocity+')/ '+(obj.yp*0.4788).toFixed(2)+'('+yeildpoint+')</td></tr>'
                rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+obj.selected_model+'</td>'
                rheology_mud_parameters +='<th>n / K:</th><td>'+(obj.n).toFixed(2)+' / '+(obj.K).toFixed(2)+'</td></tr>'
            }
            rheology_mud_parameters +='</table>'
            $('#rheology_mud_parameters').html(rheology_mud_parameters)
            $('.totalpressure').html(Math.round(totalpressureloss)+pressure)

            if(obj.unit == 'API'){
                pressureloss_charts(chart_details,obj.pre_md,obj.pre_liner,depth,pressure);
                containers(surfacelosses,pipeloss,bitloss,annularpressureloss,pressure);
                slipvelocitycharts(slipvelocity_data,annularvelocity_data,obj.min_scale,obj.max_scale,depth)
            }
            else{
                pressureloss_charts(chart_details,obj.pre_md,obj.pre_liner,depth,pressure);
                containers(surfacelosses,pipeloss,bitloss,annularpressureloss,pressure);
                slipvelocitycharts(slipvelocity_data,annularvelocity_data,obj.min_scale,obj.max_scale,depth)
            }
    if(obj.unit == 'API'){
            $('#ecd_td_without_bitdepth').html((obj.bitdepth_td_without/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_td_with_bitdepth').html((obj.bitdepth_td_with/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_csg_without_bitdepth').html((obj.bitdepth_csg_without/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_csg_with_bitdepth').html((obj.bitdepth_csg_with/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_td_without').html((obj.alongwell_td_without/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_td_with').html((obj.alongwell_td_with/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_csg_without').html((obj.alongwell_csg_without/8.345).toFixed(2)+' (g/cc)')
            $('#ecd_csg_with').html((obj.alongwell_csg_with/8.345).toFixed(2)+' (g/cc)')
            // $('#cuttings_size').val((cuttings_size*1000/3.281/12).toFixed(2))
            // $('#cuttings_density').val((obj.cuttings_density/8.33).toFixed(2))
        }
        else{
            $('#ecd_td_without_bitdepth').html((obj.bitdepth_td_without*8.345).toFixed(2)+' (ppg)')
            $('#ecd_td_with_bitdepth').html((obj.bitdepth_td_with*8.345).toFixed(2)+' (ppg)')
            $('#ecd_csg_without_bitdepth').html((obj.bitdepth_csg_without*8.345).toFixed(2)+' (ppg)')
            $('#ecd_csg_with_bitdepth').html((obj.bitdepth_csg_with*8.345).toFixed(2)+' (ppg)')
            $('#ecd_td_without').html((obj.alongwell_td_without*8.345).toFixed(2)+' (ppg)')
            $('#ecd_td_with').html((obj.alongwell_td_with*8.345).toFixed(2)+' (ppg)')
            $('#ecd_csg_without').html((obj.alongwell_csg_without*8.345).toFixed(2)+' (ppg)')
            $('#ecd_csg_with').html((obj.alongwell_csg_with*8.345).toFixed(2)+' (ppg)')
            // $('#cuttings_size').val((cuttings_size/1000*3.281*12).toFixed(2))
            // $('#cuttings_density').val((obj.cuttings_density*8.33).toFixed(2))
        }
            

    
   

}
function pressureloss_charts(chartdata,previous_measured_depth,previous_linear,depth,pressure){
    var unit='{%display_depthunit request.session.unit%}';
    directchart = Highcharts.chart('pressurelosschart', {
        chart: {
            reflow: false,
        },
        title: {
            text: ''
        },

        xAxis: {
            labels: {
            format:'{value}'
        },

            opposite: false,
            title: {
                enabled: true,
                text: 'Pressure Loss ('+pressure+')'
            },
            tickInterval : 200,

        },
        credits: {
        enabled: false
       },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD ('+depth+')'
            },
            labels: {
                format: '{value}'
            },
            tickInterval : 1000,

        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    // pointFormat: '{point.x} cm, {point.y} kg'
                }
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
            
        }
        },
        
        series: [
        {
            type: 'line',
            name: 'Pressure Loss',
            color: 'rgb(22,96,178)',
            data: chartdata,
            dashStyle: 'Solid',
        },
        {
            type:'line',
            name:'Casing',
            color:'black',
            data:[{
                x:-30,
                y: 0,
                marker: {
                    enabled: false,
                    symbol: ''
                }
            },{
                x:-30,
                y:previous_measured_depth
            }],
            marker: {
                enabled: true,
                // symbol:"triangle",
                symbol: 'url(../../../../static/images/chart/casing.png)',
                width: 30,
                height: 30,

            },
            label: {
                    connectorAllowed: true,
                    enabled:false
            }
        }
      ]
    });
}
function containers(surfaceloss,drillstringloss,bitloss,annularloss,pressure){
        Highcharts.chart('container', {
        chart: {
            type: 'bar',
            // borderWidth:0,
            marginLeft:89,
            marginRight:-30,
            groupPadding: 0,
            spacingBottom: -80,
            spacingTop: -120,
        },
        title:{
            text:''
        },
        exporting: {
    enabled: false
  },
    credits: {
        enabled: false
       },
        
       legend:{
        align: 'right',
        verticalAlign: 'top',
        x: -40,
        y: 120,  
        reversed: true,
        enabled: false            
        },
          plotOptions: {              
              bar:{
                  pointWidth:35,
                  dataLabels: {
                    format: '{y}'+pressure,
                      enabled: true,
                    },
                    animation:true,
                },
                series: {
                    showInLegend: true,
                    reversed: true,
                    shadow:false,
                    borderWidth:0,
                    stacking:true
                }
    //dataLabels: {
           //enabled: true,
        //},
 },
        xAxis:{
            categories:[''],
            lineColor:'transparant',
            // lineWidth:1,
            tickColor:'#666',
            // tickLength:3,
            

        },
         yAxis: {
            reversed: false,
            labels: {
            enabled: false,
            },	
            
            gridLineWidth: 0,
            lineColor: 'transparant',
            // lineWidth:1,
            tickColor:'transparant',
            tickWidth:1,
            tickLength:3,
            gridLineColor:'#ddd',
            title:{
                text:'',
                rotation:0,
                margin:50
            }
        },
        series: [{
            color:'#FFF3CE',
            name:'Surface',
            // legendIndex:8,
            data: [surfaceloss],
            borderRadiusTopRight: '20px',
            borderRadiusTopLeft: '20px',
            // borderRadiusBottomLeft: '20px',
        },{
            name:'Drillstring',
            color:'#F9C7C8',
            // legendIndex:7,
            data: [drillstringloss]
        },{
            name:'Bit Nozzle',
            color:'#BDD9E7',
            // legendIndex:0,
            data: [bitloss]
        },{
            // showInLegend: false,
            name:'Annular',
            color:'#C7ECD0',
            // legendIndex:0,
            data: [annularloss],
            borderRadiusBottomRight: '20px',
            borderRadiusBottomLeft: '20px',
             
        }] 
    });
};
function slipvelocitycharts(slipvelocitychart,annularvelocitychartdata,min_scale,max_scale,depth){
    directchart = Highcharts.chart('slipvelocity_chart', {
        chart: {
            reflow: false,
        },
        title: {
            text: 'Slip Velocity'
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            title: {
                enabled: true,
                text: 'Velocity ('+depth+'/min)'
            },
            tickInterval : 10,
            min:min_scale-10,
            max:max_scale+10,
        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD ('+depth+')'
            },
            labels: {
                format: '{value}'
            },
            tickInterval : 1000,

        },
        legend: { 
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                }
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
        }
        },
        
        series: [
        {
            type: 'spline',
            color: 'rgb(22,96,178)',
            data: slipvelocitychart,
            dashStyle: 'Solid',
            name:'Slip Velocity'
        },
        {
            type: 'spline',
            color: 'red',
            data: annularvelocitychartdata,
            dashStyle: 'Solid',
            name:'Annular Velocity'
        },
      ]
    });

}