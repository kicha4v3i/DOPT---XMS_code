//call when blur flowrate in hydraulics result page
var slipvelocity_chart
var ecdalongwell_chart
var directchart_ecdalong
var allpressure_barchart
var allpressureloss_chart
$('#pressureloss_data').hide();
$('#ecd_alonghole_data').hide();
$('#ecd_bitdepth_data').hide();
$('#slip_annular_data').hide();
$('#cuttings_concentration').hide();
var cuttings_density=$('#cuttings_density').val();
var cuttings_size=$('#cuttings_size').val();
$('#original_cs').val(cuttings_size)
$('#original_cd').val(cuttings_density)
slipvelocity_chart = Highcharts.chart('slipvelocity_chart', {
    
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
            text: 'Velocity ('+unit+'/min)'
        },
        tickInterval : 10,
        // min:min_scale-10,
        // max:max_scale+10,

    },
    yAxis: {
        reversed: true,
        opposite: false,
        title: {
            text: 'MD '+unit
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
    
    series: []
});


allpressure_barchart=Highcharts.chart('container', {
    chart: {
        type: 'bar',
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
            format: '{y} {%display_pressureunit request.session.unit%}',
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

    },
    xAxis:{
        categories:[''],
        lineColor:'transparant',
        tickColor:'#666',
    },
    yAxis: {
        reversed: false,
        labels: {
        enabled: false,
        },	
        gridLineWidth: 0,
        lineColor: 'transparant',
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
    series: [] 
});


$(document).on("blur", ".flowrate" , function() {
   
    var flowrate=$(this).val();
    var rpm=$('#rpm_userenter').val()
    var rop=$('#rop_userenter').val()
    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    $('#original_rop').val(rop)
    
    if (unit == 'API'){
        $(".flowrate_lable").html('Flowrate (GPM)');
        $(".rop_lable").html('ROP (ft/hr)');
        $(".bitdepth_lable").html('Bit Depth (ft)');
    }else{
        $(".flowrate_lable").html('Flowrate (LPM)');
        $(".rop_lable").html('ROP (m/hr)');
        $(".bitdepth_lable").html('Bit Depth (m)');
    }
    $('#flowrate').val(flowrate).change();
    if(flowrate!='' && rpm!='' && rop!=''){
  
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
        
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)


    }
});
//call when blur rpm in hydraulics result page
$(document).on("blur", ".rpm" , function() {
    var rpm=$(this).val();
    var flowrate=$('#flowrate_userenter').val()
    var rop=$('#rop_userenter').val()

    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
   
    if (unit == 'API'){
        $(".flowrate_lable").html('Flowrate (GPM)');
        $(".rop_lable").html('ROP (ft/hr)');
        $(".bitdepth_lable").html('Bit Depth (ft)');
    }else{
        $(".flowrate_lable").html('Flowrate (LPM)');
        $(".rop_lable").html('ROP (m/hr)');
        $(".bitdepth_lable").html('Bit Depth (m)');
    }
    $('#rpm').val(rpm).change();
    setsession(rpm,'rpm_input')

    if(flowrate!='' && rpm!='' && rop!=''){
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
       
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
    }  
});
//call when blur cutting density in hydraulics result page
$(document).on("blur", "#cuttings_density" , function() {
    var cuttings_density=$(this).val();
    var cuttings_size=$('#cuttings_size').val()
    var flowrate=$('#flowrate_userenter').val();
    var rpm=$('#rpm_userenter').val()
    var rop=$('#rop_userenter').val()
    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');

    if(cuttings_density!='' && cuttings_density!=''){
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
        
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
    }
});
//call when blur cutting size in hydraulics result page
$(document).on("blur", "#cuttings_size" , function() {
    var cuttings_size=$(this).val();
    var cuttings_density=$('#cuttings_density').val()
    var flowrate=$('#flowrate_userenter').val();
    var rpm=$('#rpm_userenter').val()
    var rop=$('#rop_userenter').val()
    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');

    if(cuttings_density!='' && cuttings_density!=''){
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
        
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
    }
});
//call when blur rop in hydraulics result page
$(document).on("blur", ".rop" , function() {
    var rop=$(this).val();
    var flowrate=$('#flowrate_userenter').val()
    var rpm=$('#rpm_userenter').val()
    $('#rop').val(rop).change();
    setsession(rop,'rop_input')
    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');

    if(flowrate!='' && rpm!='' && rop!=''){
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
        
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
    }  
});
//call when blur bitdepth in hydraulics result page
$(document).on("blur", ".bitdepth" , function() {
    var bitdepth=$(this).val();
    var flowrate=$('#flowrate_userenter').val()
    var rpm=$('#rpm_userenter').val()
    var rop=$('#rop_userenter').val()
    $('#bitdepth ').val(bitdepth ).change();
    var bitdepth=$('#bitdepth_userenter').val()
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');


    if (unit == 'API'){
        $(".flowrate_lable").html('Flowrate (GPM)');
        $(".rop_lable").html('ROP (ft/hr)');
        $(".bitdepth_lable").html('Bit Depth (ft)');
    }else{
        $(".flowrate_lable").html('Flowrate (LPM)');
        $(".rop_lable").html('ROP (m/hr)');
        $(".bitdepth_lable").html('Bit Depth (m)'); 
    }
    if(flowrate!='' && rpm!='' && rop!=''){
        while (slipvelocity_chart.series.length > 0) {
            slipvelocity_chart.series[0].remove();
        }
        
        Promise.all([getbitlosses(rpm,flowrate,rop),getsurfacelosses(rpm,flowrate,rop),getannular_drillstring_loss(rpm,flowrate,rop)])
        .then(() => {
            pressureloss_chart(rpm,flowrate,rop)
        })
        .catch(error => {
            console.error(error);
        });
        slipvelocity_table(rpm,flowrate,rop)
        bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
        ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth)
    }  
});

$(document).on("click",".pressureloss_data",function(){
    $('.pressureloss-modal').modal('show');
});
$(document).on("click",".slip_annular_data",function(){
    $('.slipvelocity-modal').modal('show');
});
$(document).on("click",".ecd_alonghole_data",function(){
    $('.ecd_alonghole-modal').modal('show');    
});
$(document).on("click",".ecd_bitdepth_data",function(){
    $('.ecd_bitdepth-modal').modal('show');
});
$(document).on("click",".cuttings_concentration",function(){
    $('.cutting_concentration-modal').modal('show');
}); 

$(document).on("click",".transport_ratio",function(){
    $('.transportratio-modal').modal('show');
});

$(document).on("click",".cci",function(){
    $('.cci-modal').modal('show');
});

// $(document).on("click","#pressureloss_chart_download",function(){
//     // createSVGFromChart(allpressureloss_chart, 'pressurelosschart_canvas','pressureloss_chart');

//     allpressureloss_chart.exportChartLocal({ type: 'image/png' });


// });




 $(document).on("click","#modals-close",function(){
    $('.pressureloss-modal').modal('hide');
    $('.ecd_alonghole-modal').modal('hide');
    $('.ecd_bitdepth-modal').modal('hide');
    $('.slipvelocity-modal').modal('hide');
    $('.cutting_concentration-modal').modal('hide');
});


function pressureloss_chart(rpm,flowrate,rop){
    var pressurelosschart_url = $('#pressurelosschart-url').data('base-url');
    pressurelosschart_url = pressurelosschart_url.replace('charttype', 'pressureloss');


    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    pressurelosschart_url = pressurelosschart_url.replace(0, wellphase_id);

    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    var bitdepth=$('#bitdepth_userenter').val();
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
        url:"/pressureloss/pressurelosschart",
        cache: false,  
        data:data,
        success: function(data) {
            $('#pressureloss_data').show();
            pressurelosschart(data.chartdata,data.previous_measured_depth,data.previous_linear) 
            obj['chart_data']=data.chartdata
            var pressureloss_datatable="";
            pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Pressure Loss</h4></tr><tr><th>Pressure loss ("+display_pressureunit+")</th><th>MD ("+display_depthunit+")</th></tr></thead><tbody>";
            for(var i=data.chartdata.length-1;i>=0;i--){
            pressureloss_datatable +='<tr><td>'+data.chartdata[i].x+'</td><td>'+data.chartdata[i].y+'</td></tr>';
            }
            pressureloss_datatable +="</tbody></table></div>";
            pressureloss_datatable +='<button id="pressureloss_chart_download" class="download-press-loss"><a href="' + pressurelosschart_url + '">Download<i class="fa fa-download icon-down"></a></button>';

            $('#pressureloss_datatable').html(pressureloss_datatable);
            createSVGFromChart(allpressureloss_chart, 'pressurelosschart_canvas','pressure_chart-'+wellphase_id+'-'+section_name);
            



        },
        error: function (err) {
            console.log('Error',err)
        }, 
    })
    
}



function getannuluspressurelaw(rpm,flowrate,rop){
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    var bitdepth=$('#bitdepth_userenter').val();

    data={}
    if(($('#torque').val()==undefined | $('#torque').val()=='') && ($('#wob').val()==undefined | $('#wob').val()=='')){
        data.rpm=rpm
        data.flowrate=flowrate
        data.wellphase_id=wellphase_id
        data.section_name=section_name
        data.rop=rop
        data.cuttings_density=cuttings_density
        data.cuttings_size=cuttings_size
        data.bitdepth=bitdepth
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

    }

    $.ajax({
        type: "GET",
        url:"/wells/muddata/calculateallpressure_loss",
        cache: false,        

        data:data,
        beforeSend: function() {
       
        },
        success: function(data) {
            load_chart=true
            $('#cuttings_density').val(data.cuttings_density)
            $('#cuttings_size').val(data.cuttings_size)
            $('#mudweight_hidden').val(data.mudweight)
            $('#pv_hidden').val(data.pv)
            $('#yp_hidden').val(data.yp)
            $('#todepth_hidden').val(data.todepth)
            $('#original_flowrate').val(flowrate)
            $('#original_rop').val(rop)
            $('#original_cs').val(data.cuttings_size)
            $('#original_cd').val(data.cuttings_density)
            $('#original_pv').val(data.plastic_viscocity)
            $('#original_yp').val(data.yieldpoint)
            $('#section_name').val(data.section_name);

            var from_depth
            var todepth
            var totalpipeloss=0
            var totalsurfacelosses=0
            var totalannularpressureloss=0
            var phasedetails=''
            phasedetails +="<table class='hyd-from'><thead><tr><th><span class='sectiondetails'>From </span></th><th><span  class='sectiondetails'>To</span></th></tr><tr><th>MD / TVD</th><th>MD / TVD</th></tr></thead>"
            phasedetails +="<tbody><tr><td><span class='sectiondetails_value'>"+data.fromdepth.toFixed()+" "+display_depthunit+"/"+data.fromdepthtvd.toFixed()+" "+display_depthunit+"</span></td><td><span class='sectiondetails_value'>"+data.todepth.toFixed()+' '+display_depthunit+'/'+data.todepthtvd.toFixed()+' '+display_depthunit+'</span></td></tr></tbody></table>'
            $('#phase_details').html(phasedetails)


            var surface=""
            surface +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Surface Pressure Losses</h4></tr><tr><th>Element</th><th>ID</th><th>Length</th><th>Pressure Drop</th></tr></thead><tbody>"
            for(var i=0;i<data.surfacelosses.length;i++){
                surface +='<tr>';
                surface +='<td>'+data.surfacelosses[i].type+'</td>';
                surface +='<td>'+data.surfacelosses[i].id+' '+display_diameter+'</td>';
                surface +='<td>'+data.surfacelosses[i].length+' '+display_depthunit+'</td>';
                surface +='<td>'+Math.round(data.surfacelosses[i].pressureloss)+' '+display_pressureunit+'</td>';
                surface +='</tr>'
                totalsurfacelosses=totalsurfacelosses+Math.round(data.surfacelosses[i].pressureloss)
            }
            surface +='</tbody></table>';
            surface +='<div class="text-center"><div class="text-danger pressure-ttl">Total Surface Pressure Loss   '+totalsurfacelosses+' '+display_pressureunit+'</div></div>'
            $('#surface-loss').html(surface)
            
            change_surface.push(data.surfacelosses);
            // if(data.linercount==0){
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
                for(var i=data.annularpressureloss.length-1;i>=0;i--){
                    cumulative_length=cumulative_length+data.annularpressureloss[i].length_against
                    annuluspressureloss +='<tr>';
                    annuluspressureloss +='<td><span class='+data.annularpressureloss[i].element_type+'>'+data.annularpressureloss[i].element_type+'</span></td>';
                    annuluspressureloss +='<td>'+data.annularpressureloss[i].element+'</td>';
                    annuluspressureloss +='<td>'+data.annularpressureloss[i].od+' '+display_diameter+'/'+data.annularpressureloss[i].id+' '+display_diameter+'</td>';
                    annuluspressureloss +='<td>'+data.annularpressureloss[i].length_against.toFixed(0)+' '+display_depthunit+'</td>';
                    annuluspressureloss +='<td>'+cumulative_length.toFixed(0)+' '+display_depthunit+'</td>';
                    annuluspressureloss +='<td>'+Math.round(data.annularpressureloss[i].drillstringloss)+' '+display_pressureunit+'</td>';
                    annuluspressureloss +='<td>'+Math.round(data.annularpressureloss[i].pressureloss)+' '+display_pressureunit+'</td>';
                    annuluspressureloss +='<td>'+data.annularpressureloss[i].flowregime+'</td>';

                    annuluspressureloss +='</tr>'
                    totalannularpressureloss=totalannularpressureloss+Math.round(data.annularpressureloss[i].pressureloss)
                    totalpipeloss=totalpipeloss+Math.round(data.annularpressureloss[i].drillstringloss)

                }
                allannularloss=totalannularpressureloss
                allpipeloss=totalpipeloss
                annuluspressureloss +='</tbody></table>';
                annuluspressureloss +='<div class="text-center"><div class="pressure-ttl text-danger">Total Annular Pressure Loss   '+allannularloss+' '+display_pressureunit+'</div><div class="pressure-ttl text-danger">Total Drillstring Pressure Loss   '+allpipeloss+' '+display_pressureunit+'</div></div></div>'
                $('#Annular-loss').html(annuluspressureloss)

                annularpressure_values.push(data.annularpressureloss,data.type_name,data.bit_od,data.bit_length);
            
         
            var bitloss=""
            bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable'><thead><tr><h4 class='phase_det_head'>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
            for(var i=0;i<data.bitpressurelosses.length;i++){
                bitloss +='<tr>';
                bitloss +='<td>'+data.bitpressurelosses[i].tfa_value+' '+display_diameter+'<sup>2</sup></td>';
                bitloss +='<td>'+data.bitpressurelosses[i].bit_pressure_loss.toFixed()+' '+display_pressureunit+'</td>';
                bitloss +='<td>'+data.bitpressurelosses[i].bhhp.toFixed()+' '+display_bhhp+'</td>';
                bitloss +='<td>'+data.bitpressurelosses[i].hsi.toFixed(2)+' '+display_bhhp+'/'+display_diameter+'<sup>2</sup></td>';
                bitloss +='<td>'+data.bitpressurelosses[i].impact_forces.toFixed()+' '+display_impactforce+'</td>';
                bitloss +='<td>'+data.bitpressurelosses[i].jet_velocity.toFixed()+' '+display_depthunit+'/sec</td>';
                bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
                bitloss +='</tr>';

                totalbitpressureloss=data.bitpressurelosses[i].bit_pressure_loss
            }      
            bitloss +='</tbody></table>';
            bitloss +=`<div class="collapse first"><div class="block__content" id='nozzle-element'></div></div>`;
            $('#bit-loss').html(bitloss);

            var bitloss_nozzle=""
            bitloss_nozzle +="<table class='table noz-tbl'><thead><tr><th>Nozzle Size<br>{%display_nozzle_size_unit request.session.unit%}</th></thead><tbody>";
            for(var i=0;i<data.bitpressurelosses.length;i++){
            for(var j=0;j<data.bitpressurelosses[i].nozzle_size.length;j++){
                bitloss_nozzle +='<tr>';
                bitloss_nozzle +='<td>'+data.bitpressurelosses[i].nozzle_size[j]+'</td>';
                bitloss_nozzle +='</tr>';
            }}
            bitloss_nozzle +='</tbody></table></div>';
            $('#nozzle-element').html(bitloss_nozzle);
            bitloss_values.push(data.bitpressurelosses)
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
            summary +='<tr><th class="text-danger">Surface Pressure Loss</th><td>'+Math.round(totalsurfacelosses)+' '+display_pressureunit+'</td><td>'+surface_pecentage.toFixed()+'% </td></tr>'; 
            summary +='<tr><th class="text-danger">Drill String Pressure Loss</th><td>'+Math.round(totalpipeloss)+' '+display_pressureunit+'</td><td>'+drillstring_pecentage.toFixed()+'%</td></tr>';   
            summary +='<tr><th class="text-danger">Bit Pressure Loss</th><td>'+Math.round(totalbitpressureloss)+' '+display_pressureunit+'</td><td>'+bit_percentage.toFixed()+'%</td></tr>';  
            summary +='<tr><th class="text-danger">Annular Pressure Loss</th><td>'+Math.round(totalannularpressureloss)+' '+display_pressureunit+'</td><td>'+annular_pecentage.toFixed()+'%</td></tr>';  
            summary +='<tr><th class="text-danger">Total Pressure Loss</th><td>'+Math.round(totalpressureloss)+' '+display_pressureunit+'</td></tr>';  
 

            summary +='</tbody></table>'; 
            // $('#summary_pressureloss').html(summary)
            annularpressureloss=parseInt(allannularloss,10)
            surfacelosses=parseInt(totalsurfacelosses,10)
            pipeloss=parseInt(allpipeloss,10)
            bitloss=parseInt(totalbitpressureloss,10)
            summary_values.push(totalsurfacelosses,totalpipeloss,totalbitpressureloss,totalannularpressureloss,totalpressureloss)
            var pressureloss_datatable="";
            pressureloss_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Pressure Loss Table</h4></tr><tr><th>Pressure loss ("+display_pressureunit+")</th><th>MD"+display_depthunit+"</th></tr></thead><tbody>";
            for(var i=data.chartdata.length-1;i>=0;i--){
            pressureloss_datatable +='<tr><td>'+data.chartdata[i].x+'</td><td>'+data.chartdata[i].y+'</td></tr>';
            }
            pressureloss_datatable +="</tbody></table></div>";
            $('#pressureloss_datatable').html(pressureloss_datatable);
            
            var slip = parseFloat(data.slipvelocitychart[0].x);
            var annular = parseFloat(data.annularvelocitychartdata[0].x);
            data.slipvelocitychart.unshift({x:slip,y:0})
            data.annularvelocitychartdata.unshift({x:annular,y:0})
            data.ecd_fracturepressure.unshift({x:data.middleValue,y:data.previous_measured_depth});

            // var slipvelocity_datatable="";
            // slipvelocity_datatable += "<div class=' p-3'><table class='popup-presstbl' ><thead><tr><h4 class='phase_det_head'>Slip Velocity Loss Table</h4></tr><tr><th>Velocity(ft/min)</th><th>MD(ft)</th></tr></thead><tbody>";
            // for(var i=0;i<data.slipvelocitychart.length;i++){
            // slipvelocity_datatable +='<tr><td>'+data.slipvelocitychart[i].x+'</td><td>'+data.slipvelocitychart[i].y+'</td></tr>';
            // }
            // slipvelocity_datatable +="</tbody></table></div>";
            // slipvelocity_datatable += "<div class=' p-3'><table class='popup-presstbl' ><thead><tr><h4 class='phase_det_head'>Annular Velocity Loss Table</h4></tr><tr><th>Velocity(ft/min)</th><th>MD(ft)</th></tr></thead><tbody>";
            // for(var i=0;i<data.annularvelocitychartdata.length;i++){
            // slipvelocity_datatable +='<tr><td>'+data.annularvelocitychartdata[i].x+'</td><td>'+data.annularvelocitychartdata[i].y+'</td></tr>';
            // }
            // slipvelocity_datatable +="</tbody></table></div>";
            // $('#slipvelocity_datatable').html(slipvelocity_datatable);

            var ecdalongwell_datatable="";
            ecdalongwell_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>ECD Alonghole Table</h4></tr><tr><th>ECD"+display_densityunit+"</th><th>MD"+display_depthunit+"</th></tr></thead><tbody>";
            for(var i=0;i<data.ecdchartdata.length;i++){
            ecdalongwell_datatable +='<tr><td>'+data.ecdchartdata[i].x+'</td><td>'+data.ecdchartdata[i].y+'</td></tr>';
            }
            ecdalongwell_datatable +="</tbody></table></div>";
            $('#ecd_alonghole_datatable').html(ecdalongwell_datatable);
            
            var ecd_bitdepth_datatable="";
            ecd_bitdepth_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>ECD Bitdepth Table</h4></tr><tr><th>ECD"+display_densityunit+"</th><th>MD"+display_depthunit+"</th></tr></thead><tbody>";
            for(var i=0;i<data.ecdalongwell.length;i++){
            ecd_bitdepth_datatable +='<tr><td>'+data.ecdalongwell[i].x+'</td><td>'+data.ecdalongwell[i].y+'</td></tr>';
            }
            ecd_bitdepth_datatable +="</tbody></table></div>";
            $('#ecd_bitdepth_datatable').html(ecd_bitdepth_datatable);

            var cutting_concentration_datatable="";
            cutting_concentration_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Cutting Concentration Table</h4></tr><tr><th>Percentage(%)</th><th>MD(ft)</th></tr></thead><tbody>";
            for(var i=0;i<data.cuttingsconcentration.length;i++){
            cutting_concentration_datatable +='<tr><td>'+data.cuttingsconcentration[i].x+'</td><td>'+data.cuttingsconcentration[i].y+'</td></tr>';
            }
            cutting_concentration_datatable +="</tbody></table></div>";
            $('#cutting_concentration_datatable').html(cutting_concentration_datatable);
            var rheology_mud_parameters=''
            rheology_mud_parameters +='<table class="mud-reh-det">'
            rheology_mud_parameters +='<tr><th>Mud Weight:</th><td>'+data.mudweight+' '+display_densityunit+'</td>'
            rheology_mud_parameters +='<th>PV / YP:</th><td>'+data.pv+' '+display_plastic_viscosity+'/'+data.yp+' '+display_gelstrengthunit+'</td></tr>'
            rheology_mud_parameters +='<tr><th>Rheology:</th><td>'+data.selected_modal+'</td>'
            rheology_mud_parameters +='<th>n / K:</th><td>'+data.m+' / '+data.K+'</td></tr>'
            rheology_mud_parameters +='</table>'
            $('#rheology_mud_parameters').html(rheology_mud_parameters)
            rheology_parameters.push(data.mudweight,data.pv,data.yp,data.selected_modal,data.K,data.m)
            $('.totalpressure').html(Math.round(totalpressureloss)+' '+display_pressureunit)
            $('.total_pressure_loss').val(Math.round(totalpressureloss));
            pressurelosschart(data.chartdata,data.previous_measured_depth,data.previous_linear)
            container(surfacelosses,pipeloss,bitloss,annularpressureloss)
            var min_scale=parseInt(data.slipvelocitychart[0].x.toFixed());
            var last_scale = $(data.annularvelocitychartdata).last()[0]
            var max_scale=parseInt(last_scale.x.toFixed());
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
            var cutting_min=parseInt(data.cuttingsconcentration[0].x.toFixed());
            var cutting_max=parseInt($(data.cuttingsconcentration).last()[0].x);
            
            // slipvelocitychart(data.slipvelocitychart,data.annularvelocitychartdata,min_scale,max_scale)
            ecdchart(data.ecdchartdata,data.previous_measured_depth,data.mudweight,data.todepth,ecd_chart_max,data.increasedecdchartdata,data.ecd_fracturepressure)
            ecdalongwellchart(data.ecdalongwell,data.previous_measured_depth,data.mudweight,data.todepth,ecd_alonghole_max,data.ecdalongwellincreased,data.ecd_fracturepressure)
            //cuttingsconcentration_chart(data.cuttingsconcentration,cutting_min,cutting_max)
            // transportratiochart(data.transportratio)
            // ccichart(data.cci,data.maxcci)
            $('#original_mudweight').val(data.mudweight)

            $('#ecd_td_without_bitdepth').html(data.bitdepth_td_without+' '+display_densityunit)
            $('#ecd_td_with_bitdepth').html(data.bitdepth_td_with+' '+display_densityunit)
            $('#ecd_csg_without_bitdepth').html(data.bitdepth_csg_without+' '+display_densityunit)
            $('#ecd_csg_with_bitdepth').html(data.bitdepth_csg_with+' '+display_densityunit)
            $('#ecd_td_without').html(data.alongwell_td_without+' '+display_densityunit)
            $('#ecd_td_with').html(data.alongwell_td_with+' '+display_densityunit)
            $('#ecd_csg_without').html(data.alongwell_csg_without+' '+display_densityunit)
            $('#ecd_csg_with').html(data.alongwell_csg_with+' '+display_densityunit)
            $('#ecd_with_bitdepth').val(data.bitdepth_td_with);
            // chart_data.push(data.chartdata,data.previous_measured_depth,data.previous_linear)
            obj["surface"]=change_surface;
            obj["summary"]=summary_values;
            obj["bit"]=bitloss_values;
            obj["annular"]=annularpressure_values;
            obj["rheology_parameters"]=rheology_parameters;
            obj['unit']=unit
            obj['fromdepth']=data.fromdepth
            obj['fromdepthtvd']=data.fromdepthtvd
            obj['todepth']=data.todepth
            obj['todepthtvd']=data.todepthtvd
            obj["chart_data"]=data.chartdata
            obj["slipvelocity"]=data.slipvelocitychart
            obj['annularvelocity']=data.annularvelocitychartdata
            obj['min_scale']=min_scale
            obj['max_scale']=max_scale
            obj["pre_md"]=data.previous_measured_depth
            obj["pre_liner"]=data.previous_linear
            obj['mudweight']=data.mudweight;
            obj['pv']=data.pv;
            obj['yp']=data.yp;
            obj['selected_model']=data.selected_modal;
            obj['K']=data.K;
            obj['n']=data.m;
            obj['bitdepth_td_without']=data.bitdepth_td_without
            obj['bitdepth_td_with']=data.bitdepth_td_with
            obj['bitdepth_csg_without']=data.bitdepth_csg_without
            obj['bitdepth_csg_with']=data.bitdepth_csg_with
            obj['alongwell_td_without']=data.alongwell_td_without
            obj['alongwell_td_with']=data.alongwell_td_with
            obj['alongwell_csg_without']=data.alongwell_csg_without
            obj['alongwell_csg_with']=data.alongwell_csg_with
            obj['cuttings_density']=data.cuttings_density
            obj['cuttings_size']=data.cuttings_size
        
        pressure_chart_pdf(data.chartdata,data.previous_measured_depth,data.chartdata[0].x)
        ecdbitchart_pdf(data.ecdchartdata,data.previous_measured_depth,data.mudweight,data.todepth,ecd_chart_max,data.increasedecdchartdata,data.ecd_fracturepressure)
        ecdalonghole_chart_pdf(data.ecdalongwell,data.previous_measured_depth,data.mudweight,data.todepth,ecd_alonghole_max,data.ecdalongwellincreased,data.ecd_fracturepressure)
        ccichart_pdf(data.cci,data.maxcci)
        transportratiochart_pdf(data.transportratio)

        createSVGFromChart(rheology_chart, 'pressurelosschart_canvas','rheogramchart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(pressure_chart, 'pressurelosschart_canvas','pressure_chart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(ecdbit_chart, 'ecdbit_canvas','ecdbit_chart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(ecdalong_chart, 'ecdalong_canvas','ecdalong_chart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(cci_chart, 'pressurelosschart_canvas','cci_chart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(tr_chart, 'pressurelosschart_canvas','tr_chart-'+wellphase_id+'-'+section_name);
        createSVGFromChart(directchart_slip, 'pressurelosschart_canvas','directchart_slip-'+wellphase_id+'-'+section_name);
        
        
        // createSVGFromChart(directchart_bar, 'pressurelosschart_canvas','directchart_bar-'+wellphase_id+'-'+section_name);
        // createSVGFromChart(directchart, 'pressurelosschart_canvas','direct-'+wellphase_id+'-'+section_name);
        // createSVGFromChart(directchart_cc, 'pressurelosschart_canvas','directchart_cc-'+wellphase_id+'-'+section_name);
        // createSVGFromChart(directchart_ecdalong, 'ecdalong_canvas','directchart_ecdalong-'+wellphase_id+'-'+section_name);
        // createSVGFromChart(directchart_ecdbit, 'ecdbit_canvas','directchart_ecdbit-'+wellphase_id+'-'+section_name);
    },
    error: function (err) {
        console.log(err)
    },   
    complete: function(){
       
    },
    
});
}


function getsurfacelosses(rpm,flowrate,rop){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    data = {
        rpm:rpm,
        flowrate:flowrate,
        wellphase_id:wellphase_id,
        section_name:section_name,
        rop:rop
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
            surface +="<div class='card p-3 card-mg'><table class='table surface-table'><thead><tr><h4 class='phase_det_head'>Surface Pressure Losses</h4></tr><tr><th>Element</th><th>ID</th><th>Length</th><th>Pressure Drop</th></tr></thead><tbody>"
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
            
            console.log("totalsurfacelosses"+totalsurfacelosses)
            var series={
                color:'#FFF3CE',
                name:'Surface',
                data: [totalsurfacelosses],
                // borderRadiusTopRight: '20px',
                // borderRadiusTopLeft: '20px',     
            }
            checkseries=isSeriesExists('Surface',allpressure_barchart)
            console.log("checkseries"+checkseries)
            if(checkseries==false){
                allpressure_barchart.addSeries(series)
            }

            updateallpressure_barchart()



           
        })
        .catch(error => {
        reject(error); 
        });
    });


    // $.ajax({
    //     type: "POST",
    //     url:"/wells/muddata/calculatesurfacelosses",
    //     cache: false,  
              
    //     data: {
    //         csrfmiddlewaretoken: csrf,
    //         'rpm':rpm,
    //         'flowrate':flowrate,
    //         'wellphase_id':wellphase_id,
    //         'section_name':section_name
    //     },

    //     success: function(data) {
    //         console.log(data)
    //         totalsurfacelosses=0

    //         var surface=""
    //         surface +="<div class='card p-3 card-mg'><table class='table'><thead><tr><h4 class='phase_det_head'>Surface Pressure Losses</h4></tr><tr><th>Element</th><th>ID</th><th>Length</th><th>Pressure Drop</th></tr></thead><tbody>"
    //         for(var i=0;i<data.length;i++){
    //             console.log("datya"+data[i].pressureloss)
    //             surface +='<tr>';
    //             surface +='<td>'+data[i].type+'</td>';
    //             surface +='<td>'+data[i].id+' '+display_diameter+'</td>';
    //             surface +='<td>'+data[i].length+' '+display_depthunit+'</td>';
    //             surface +='<td>'+Math.round(data[i].pressureloss)+' '+display_pressureunit+'</td>';
    //             surface +='</tr>'
    //             totalsurfacelosses=totalsurfacelosses+Math.round(data[i].pressureloss)
    //         }
    //         surface +='</tbody></table>';
    //         surface +='<div class="text-center"><div class="text-danger pressure-ttl">Total Surface Pressure Loss   '+totalsurfacelosses+' '+display_pressureunit+'</div></div>'
    //         $('#surface-loss').html(surface)
    //         $('#surface_loss_value').val(totalsurfacelosses)
    //     }
    // })
}



function getbitlosses(rpm,flowrate,rop){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    data={
        rpm:rpm,
        flowrate:flowrate,
        wellphase_id:wellphase_id,
        section_name:section_name,
        bitdepth:$('#bitdepth_userenter').val(),
        rop:rop

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
            bitloss_values.push(data.bit_losses)
            obj["bit"]=bitloss_values;
            obj['K']=data.K;
            obj['n']=data.m;
            $('#pv_hidden').val(data.pv)
            $('#yp_hidden').val(data.yp)
            $('#todepth_hidden').val(data.todepth)
            $('#original_mudweight').val(data.mudweight)

            var bitloss=""
            bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable bit-hydra-tabl'><thead><tr><h4 class='phase_det_head '>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
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
                totalbitpressureloss=Math.round(bitpressureloss[i].bit_pressure_loss)
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
            var bitlosses={
                name:'Bit Nozzle',
                color:'#BDD9E7',
                data: [totalbitpressureloss]
            }

            checkbit=isSeriesExists('Bit Nozzle',allpressure_barchart)
            if(checkbit==false){
                allpressure_barchart.addSeries(bitlosses)
            }
            updateallpressure_barchart()

        })
        .catch(error => {
        reject(error); 
        });
    });
}




// function getbitlosses(rpm,flowrate,rop){
//     var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
//     var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
//     data={}
//     data.rpm=rpm
//     data.flowrate=flowrate
//     data.wellphase_id=wellphase_id
//     data.section_name=section_name
//     console.log(data)
//     $.ajax({
//         type: "POST",
//         url:"/wells/muddata/calculatebitpressureloss",
//         cache: false,     
        
//         data: {
//             csrfmiddlewaretoken: csrf,
//             'rpm':rpm,
//             'flowrate':flowrate,
//             'wellphase_id':wellphase_id,
//             'section_name':section_name
//         },

//         success: function(data) {
//             console.log(data)
//             var bitloss=""
//             bitloss +="<div class='card p-3 bitloss-div card-mg'><table class='table bit-losstable'><thead><tr><h4 class='phase_det_head'>Bit Hydraulics</h4></tr><tr><th>TFA</th><th>ΔP<sub>bit</sub></th><th>BHHP</th><th>HSI</th><th>Impact Force</th><th>Jet Velocity</th></tr></thead><tbody>"
//             for(var i=0;i<data.length;i++){
//                 bitloss +='<tr>';
//                 bitloss +='<td>'+data[i].tfa_value+' '+display_diameter+'<sup>2</sup></td>';
//                 bitloss +='<td>'+data[i].bit_pressure_loss.toFixed()+' '+display_pressureunit+'</td>';
//                 bitloss +='<td>'+data[i].bhhp.toFixed()+' '+display_bhhp+'</td>';
//                 bitloss +='<td>'+data[i].hsi.toFixed(2)+' '+display_bhhp+'/'+display_diameter+'<sup>2</sup></td>';
//                 bitloss +='<td>'+data[i].impact_forces.toFixed()+' '+display_impactforce+'</td>';
//                 bitloss +='<td>'+data[i].jet_velocity.toFixed()+' '+display_depthunit+'/sec</td>';
//                 bitloss +=`<td><a class="btn btn__first noz-name" data-toggle="collapse" data-target=".collapse.first" data-text="Collapse"> Nozzle Details </a></td>`;
//                 bitloss +='</tr>';

//                 totalbitpressureloss=data[i].bit_pressure_loss
//                 $('#bit_loss_value').val(totalbitpressureloss)

//             }      
//             bitloss +='</tbody></table>';
//             bitloss +=`<div class="collapse first"><div class="block__content" id='nozzle-element'></div></div>`;
//             $('#bit-loss').html(bitloss);
//         }
//     })
// }


function setsession(value,type){

    var data={
        val:value,
        typename:type   
    }
    $.ajax({
    type: "POST",
    url:"/pressureloss/setsession",
    data: {
        csrfmiddlewaretoken: csrf,
        data:JSON.stringify(data)
    },
    success: function(data) {
       console.log()
    }
});

}


function getannular_drillstring_loss(rpm,flowrate,rop){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var bitdepth=$('#bitdepth_userenter').val();
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    var annularvelocitychart_url = $('#pressurelosschart-url').data('base-url');
    annularvelocitychart_url = annularvelocitychart_url.replace('charttype', 'annular_velocity');
    annularvelocitychart_url = annularvelocitychart_url.replace(0,wellphase_id);
    data= {
        csrfmiddlewaretoken: csrf,
        'rpm':rpm,
        'flowrate':flowrate,
        'wellphase_id':wellphase_id,
        'section_name':section_name,
        'torque':$('#torque').val(),
        'wob':$('#wob').val(),
        'bitdepth':bitdepth,
        'rop':rop,
        'cuttings_density':cuttings_density,
        'cuttings_size':cuttings_size
    }
    return new Promise((resolve, reject) => {
        fetch("/pressureloss/calculate_annular_drillstring_loss",{method: 'POST', body:  JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        })
        .then(response => response.json())
        .then(data => {
            resolve(data)
            $('#slip_annular_data').show(); 
            annularpressure_values.push(data.allpressureloss,data.type_name,data.bit_od,data.bit_length);
            obj["annular"]=annularpressure_values;

            allpressure=data.allpressureloss
            var totalannularpressureloss=0
            var totalpipeloss=0
            var total_ann=0
            var total_pipe=0
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

            var annularvelocity_datatable="";
            annularvelocity_datatable += "<div class='p-3 '><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Annular Velocity</h4></tr><tr><th>Velocity(ft/min)</th><th>MD ("+display_depthunit+")</th></tr></thead><tbody>";
            for(var i=0;i<data.annularvelocitychartdata.length;i++){
                annularvelocity_datatable +='<tr><td>'+data.annularvelocitychartdata[i].x+'</td><td>'+data.annularvelocitychartdata[i].y+'</td></tr>';
            }
            annularvelocity_datatable +="</tbody></table></div>";
            annularvelocity_datatable += '<button class="ecd-button"><a href="' + annularvelocitychart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
            $('#annularvelocity_datatable').html(annularvelocity_datatable);

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

            var Annularseries={
                name:'Annular',
                color:'#C7ECD0',
                data: [allannularloss],
                // borderRadiusBottomRight: '20px',
                // borderRadiusBottomLeft: '20px',     
            }
            checkAnnular=isSeriesExists('Annular',allpressure_barchart)
            if(checkAnnular==false){
                allpressure_barchart.addSeries(Annularseries)
            }

            var drillStringseries={
                name:'Drillstring',
                color:'#F9C7C8',
                data: [allpipeloss]
            }

            checkdrillString=isSeriesExists('Drillstring',allpressure_barchart)
            if(checkdrillString==false){
                allpressure_barchart.addSeries(drillStringseries)
            }

            var last_scale = $(data.annularvelocitychartdata).last()[0]
            var max_scale=parseInt(last_scale.x.toFixed());
            obj['max_scale']=max_scale
            getsummary_pressure_loss()
            updateallpressure_barchart()

        })
        .catch(error => {
            reject(error); 
        });
    });
}

function getsummary_pressure_loss(){

    let totalsurfacelosses = parseInt($("#surface_loss_value").val());
    let totalannularpressurelosses = parseInt($("#annular_loss_value").val());
    let totaldrillstringpressurelosses = parseInt($("#drillstring_loss_value").val());
    let totalbitpressurelosses = parseInt($("#bit_loss_value").val());
    totalpressureloss = totalsurfacelosses+totalannularpressurelosses+totaldrillstringpressurelosses+totalbitpressurelosses
    surface_pecentage = totalsurfacelosses/totalpressureloss*100
    drillstring_pecentage = totaldrillstringpressurelosses/totalpressureloss*100
    annular_pecentage = totalannularpressurelosses/totalpressureloss*100
    bit_percentage = totalbitpressurelosses/totalpressureloss*100
    
    let summary="";
            
    summary +="<table class='table card p-3 card-mg'>";
    summary +="<thead>";
    summary +="<tr><th><h4 class='text-center phase_det_head'>Summary Of Pressure Loss</h4></th></tr>";
    summary +="</thead>";
    summary +="<tbody>";
    summary +='<tr><th class="text-danger">Surface Pressure Loss</th><td>'+Math.round(totalsurfacelosses)+' '+display_pressureunit+'</td><td>'+surface_pecentage.toFixed()+'% </td></tr>'; 
    summary +='<tr><th class="text-danger">Drill String Pressure Loss</th><td>'+Math.round(totaldrillstringpressurelosses)+' '+display_pressureunit+'</td><td>'+drillstring_pecentage.toFixed()+'%</td></tr>';   
    summary +='<tr><th class="text-danger">Bit Pressure Loss</th><td>'+Math.round(totalbitpressurelosses)+' '+display_pressureunit+'</td><td>'+bit_percentage.toFixed()+'%</td></tr>';  
    summary +='<tr><th class="text-danger">Annular Pressure Loss</th><td>'+Math.round(totalannularpressurelosses)+' '+display_pressureunit+'</td><td>'+annular_pecentage.toFixed()+'%</td></tr>';  
    summary +='<tr><th class="text-danger">Total Pressure Loss</th><td>'+Math.round(totalpressureloss)+' '+display_pressureunit+'</td></tr>';  


    summary +='</tbody></table>'; 
    $('#summary_pressureloss').html(summary)
    
}

function bitdepthcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var bitdepth=$('#bitdepth_userenter').val();
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();

    var ecdbitdepthchart_url = $('#pressurelosschart-url').data('base-url');
    ecdbitdepthchart_url = ecdbitdepthchart_url.replace('charttype', 'ecdbitdepth');
    ecdbitdepthchart_url = ecdbitdepthchart_url.replace(0, wellphase_id);

    $.ajax({
        type: "GET",
        url: "/pressureloss/ecdbitdepth_calculation",
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
        $('#ecd_bitdepth_data').show();
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

        var ecdbitdepth_datatable="";
        ecdbitdepth_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>ECD Bitdepth</h4></tr><tr><th>ECD"+display_densityunit+"</th><th>MD"+display_depthunit+"</th></tr></thead><tbody>";
        for(var i=0;i<data.ecdchartdata.length;i++){
            ecdbitdepth_datatable +='<tr><td>'+data.ecdchartdata[i].x+'</td><td>'+data.ecdchartdata[i].y+'</td></tr>';
        }
        ecdbitdepth_datatable +="</tbody></table></div>";
        ecdbitdepth_datatable += '<button class="ecd-button"><a href="' + ecdbitdepthchart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
        $('#ecd_bitdepth_datatable').html(ecdbitdepth_datatable);
        $('#ecd_td_without_bitdepth').html(data.bitdepth_td_without+display_densityunit)
        $('#ecd_csg_without_bitdepth').html(data.bitdepth_csg_without+display_densityunit)
        $('#ecd_td_with_bitdepth').html(data.bitdepth_td_with+display_densityunit)
        $('#ecd_csg_with_bitdepth').html(data.bitdepth_csg_with+display_densityunit)

        ecdchart(data.ecdchartdata,data.previous_measured_depth,data.mudweight,data.todepth,ecd_chart_max,data.increasedecdchartdata,data.ecd_fracturepressure) 
        createSVGFromChart(directchart_ecdbit,'pressurelosschart_canvas','ecdbitdepth-'+wellphase_id+'-'+section_name);
    },
        error: function (error) {
            console.log(error);
        },
        complete: function () {
        }
    });
}

function ecdalongwellcalculation(rpm,flowrate,rop,section_name,wellphase_id,bitdepth){
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var bitdepth=$('#bitdepth_userenter').val();
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    var ecdalongholechart_url = $('#pressurelosschart-url').data('base-url');
    ecdalongholechart_url = ecdalongholechart_url.replace('charttype', 'ecdalonghole');
    ecdalongholechart_url = ecdalongholechart_url.replace(0,wellphase_id);
    $.ajax({
        type: "GET",
        url: "/pressureloss/ecdalongwell_calculation",
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
            $('#ecd_alonghole_data').show();
            $('#mudweight_hidden').val(data.mudweight)
           if($(data.ecd_fracturepressure).last()[0].x ==0 && $(data.ecd_fracturepressure).last()[0].y == 0){
            var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            }
            else if($(data.ecd_fracturepressure).last()[0].x <= $(data.ecdalongwellincreased).last()[0].x){
                var ecd_alonghole_max=parseInt($(data.ecdalongwellincreased).last()[0].x);
            }
            else{   
                var ecd_alonghole_max=parseInt($(data.ecd_fracturepressure).last()[0].x);
            }

            var ecd_along_datatable="";
            ecd_along_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>ECD Alonehole</h4></tr><tr><th>ECD"+display_densityunit+"</th><th>MD ("+display_depthunit+")</th></tr></thead><tbody>";
            for(var i=0;i<data.ecdalongwell.length;i++){
                ecd_along_datatable +='<tr><td>'+data.ecdalongwell[i].x+'</td><td>'+data.ecdalongwell[i].y+'</td></tr>';
            }
            ecd_along_datatable +="</tbody></table></div>";
            ecd_along_datatable += '<button class="ecd-button"><a href="' + ecdalongholechart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#ecd_alonghole_datatable').html(ecd_along_datatable);
            $('#ecd_td_without').html(data.alongwell_td_without+display_densityunit)
            $('#ecd_csg_without').html(data.alongwell_csg_without+display_densityunit)
            $('#ecd_td_with').html(data.alongwell_td_with+display_densityunit)
            $('#ecd_csg_with').html(data.alongwell_csg_with+display_densityunit)



        
            ecdalongwellchart(data.ecdalongwell,data.previous_measured_depth,data.mudweight,data.todepth,ecd_alonghole_max,data.ecdalongwellincreased,data.ecd_fracturepressure)
            createSVGFromChart(directchart_ecdalong,'pressurelosschart_canvas','ecdalonghole-'+wellphase_id+'-'+section_name);
        


        },
        error: function (error) {
            console.log(error);
        },
        complete: function () {
        }
    });
}

function ecdalongwellcalculationincreased(rpm,flowrate,rop,section_name,wellphase_id,bitdepth){
    
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    $.ajax({
        type: "GET",
        url: "/wells/muddata/ecdalongwell_calculationincreased",
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
       
           var ecdalongwell_increased={
            type:'scatter',
            color: 'rgb(169,52,52)',
            data: data.ecdalongwellincreased,
            name:'ECD(with cuttings)',
            dashStyle: 'Solid', 
        }
        
        checkseries_increased=isSeriesExists('ECD(with cuttings)',ecdalongwell_chart)
        if(checkseries_increased==false){
            ecdalongwell_chart.addSeries(ecdalongwell_increased)
        } 
        
        // ecdalongwell_chart.xAxis[0].update({
        //     min:data.mudweight-0.5,
        //     max:ecd_alonghole_max+1
        // }); 
        },
        error: function (error) {
            console.log(error);
        },
        complete: function () {
        }
    });
}


function slipvelocity_table(rpm,flowrate,rop){

    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    var cuttings_density=$('#cuttings_density').val();
    var cuttings_size=$('#cuttings_size').val();
    var bitdepth=$('#bitdepth_userenter').val();
    var download_url = $('#pressurelosschart-url').data('base-url');
    var slipvelocitychart_url = download_url.replace('charttype', 'slip_velocity');
    slipvelocitychart_url = slipvelocitychart_url.replace(0, wellphase_id);
    var cuttingconcentrationchart_url=download_url.replace('charttype', 'cuttings_concentration');
    cuttingconcentrationchart_url = cuttingconcentrationchart_url.replace(0, wellphase_id);
    var ccichart_url=download_url.replace('charttype', 'cci');
    ccichart_url = ccichart_url.replace(0, wellphase_id);
    var transportratiochart_url=download_url.replace('charttype', 'transport_ratio');
    transportratiochart_url = transportratiochart_url.replace(0, wellphase_id);


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
        url:"/pressureloss/calculate_slipvelocity",
        cache: false,        
        data:data,
        beforeSend: function() {
        },
        success: function(data1) {
            load_chart=true
            $('#slip_annular_data').show()
            // var min_scale=parseInt(data.slipvelocitychart[0].x.toFixed());
            // var last_scale = $(data.annularvelocitychartdata).last()[0];
            // var max_scale=parseInt(last_scale.x.toFixed());
            var slip_data= data1.slipvelocitychart
            obj['slipvelocity']=data1.slipvelocitychart
            var min_scale=parseInt(data1.slipvelocitychart[0].x.toFixed());
            obj['min_scale']=min_scale


            var slipvelocity_datatable="";
            slipvelocity_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Slip Velocity</h4></tr><tr><th>Velocity(ft/min)</th><th>MD ("+display_depthunit+")</th></tr></thead><tbody>";
            for(var i=0;i<data1.slipvelocitychart.length;i++){
                slipvelocity_datatable +='<tr><td>'+data1.slipvelocitychart[i].x+'</td><td>'+data1.slipvelocitychart[i].y+'</td></tr>';
            }
            slipvelocity_datatable +="</tbody></table></div>";
            slipvelocity_datatable +='<button class="ecd-button"><a href="' + slipvelocitychart_url + '">Download <i class="fa fa-download icon-down"></a></button>';
            $('#slipvelocity_datatable').html(slipvelocity_datatable); 
            createSVGFromChart(slipvelocity_chart,'pressurelosschart_canvas','slip_velocity-'+wellphase_id+'-'+section_name);
            

            $.ajax({
                type: "GET",
                url: "/pressureloss/calculate_cci_trans_cutting",
                cache: false,
                data: {
                    slip_data: JSON.stringify(slip_data),
                    flowrate:flowrate,
                    section_name:section_name,
                    wellphase_id:wellphase_id,
                    rop:rop,
                    bitdepth:bitdepth,
                    rpm:rpm
                    
                },
                beforeSend: function () {
                    
                },
                success: function (data) {
                    $('#cuttings_concentration').show();
                    console.log("transportratiochart_url"+transportratiochart_url)
                    console.log("ccichart_url"+ccichart_url)
                    console.log("cuttingconcentrationchart_url"+cuttingconcentrationchart_url)


                    var cutting_min=parseInt(data.cuttingsconcentration[0].x.toFixed());
                    var cutting_max=parseInt($(data.cuttingsconcentration).last()[0].x);
                    ccichart(data.cci,data.maxcci)

                    cuttingsconcentration_chart(data.cuttingsconcentration,cutting_min,cutting_max)
                    transportratiochart(data.transportratio)

                    var cutting_concentration_datatable="";
                    cutting_concentration_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Cutting Concentration</h4></tr><tr><th>Percentage(%)</th><th>MD(ft)</th></tr></thead><tbody>";
                    for(var i=0;i<data.cuttingsconcentration.length;i++){
                    cutting_concentration_datatable +='<tr><td>'+data.cuttingsconcentration[i].x+'</td><td>'+data.cuttingsconcentration[i].y+'</td></tr>';
                    }
                    cutting_concentration_datatable +="</tbody></table></div>";
                    cutting_concentration_datatable += '<button class="ecd-button"><a href="' + cuttingconcentrationchart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
                    $('#cutting_concentration_datatable').html(cutting_concentration_datatable);
                    createSVGFromChart(directchart_cc,'pressurelosschart_canvas','cuttings_concentration-'+wellphase_id+'-'+section_name);
                    
                    var cci_datatable="";
                    cci_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>CCI</h4></tr><tr><th>Percentage(%)</th><th>MD(ft)</th></tr></thead><tbody>";
                    for(var i=0;i<data.cci.length;i++){
                        cci_datatable +='<tr><td>'+data.cci[i].x+'</td><td>'+data.cci[i].y+'</td></tr>';
                    }
                    cci_datatable +="</tbody></table></div>";
                    cci_datatable += '<button class="ecd-button"><a href="' + ccichart_url + '">Download<i class="fa fa-download icon-button"></a></button>';
                    $('#cci_datatable').html(cci_datatable);
                    createSVGFromChart(directchart_cci,'pressurelosschart_canvas','cci-'+wellphase_id+'-'+section_name);
                    var transportratio_datatable="";
                    transportratio_datatable += "<div class='p-3'><table class='popup-presstbl table-striped'><thead><tr><h4 class='phase_det_head'>Transport Ratio</h4></tr><tr><th>Percentage(%)</th><th>MD(ft)</th></tr></thead><tbody>";
                    for(var i=0;i<data.transportratio.length;i++){
                        transportratio_datatable +='<tr><td>'+data.transportratio[i].x+'</td><td>'+data.transportratio[i].y+'</td></tr>';
                    }
                    transportratio_datatable +="</tbody></table></div>";
                    transportratio_datatable += '<button class="ecd-button"><a href="' + transportratiochart_url + '">Download<i class="fa fa-download icon-down"></a></button>';
                    $('#transportratio_datatable').html(transportratio_datatable);
                    createSVGFromChart(directchart_tr,'pressurelosschart_canvas','transport_ratio-'+wellphase_id+'-'+section_name);
                    
                    
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


function ecdalongwellchart(ecdalongwelldata,previous_measured_depth,mudweight,todepth,ecd_alonghole_max,ecdalongwellincreased,ecd_fracturepressure){
   
    
    var minx=(parseFloat(mudweight) - 0.5)

    
    var unit=display_depthunit;
    directchart_ecdalong = Highcharts.chart('alongholeecd_chart', {
        chart: {
            reflow: false,
        },
        title: {
            text: ''
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            reversed: false,
            gridLineWidth:1,
            title: {
                enabled: true,
                text: 'ECD '+display_densityunit,
            },
            tickInterval : 0.2,
            tickPixelInterval: 80,
            min:minx,
            max:ecd_alonghole_max+1

        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD('+unit+')'
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
                    radius: 2,
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
                },
                lineWidth:2,
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
            
        },
        series: {
            marker: {
                enabled: false
            }
        },
        },
        
        series: [
        {
            type:'scatter',
            color: 'rgb(22,96,178)',
            data: ecdalongwelldata,
            name:'ECD(without cuttings)',
            dashStyle: 'Solid', 
        },
        {
            type:'scatter',
            color: 'brown',
            data: ecdalongwellincreased,
            name:'ECD(with cuttings)',
            dashStyle: 'Solid',
        },
        {
        name: 'Mud Weight',
        color:'#bb1111',
        data: [{
                x:mudweight,
                y:0,
                marker: {
                    enabled: false,
                    symbol: '',
                    radius: 0
                }
            },{
                x:mudweight,
                y:todepth
            }],
    },
    {
        name:'Fracture Pressure',
        color:'#DB843D',
        data:ecd_fracturepressure
    },
        {
            type:'line',
            name:'Casing',
            color:'black',
            lineWidth:4,
            data:[{
                x:minx,
                y:0,
                marker: {
                    enabled: false,
                    symbol: ''
                }
            },{
                x:minx,
                y:previous_measured_depth
            }],
            marker: {
                enabled: true,
                symbol: 'url(../../../../static/images/chart/casing.png)',
                width: 30,
                height: 30,
            },
            label: {
                    connectorAllowed: true,
                    enabled:false
            }
        },
        {
            name: 'Intersect',
            data: [],
            type: 'scatter',
            lineWidth: 0,
            color:'red',
            marker: {
                symbol: 'point',
                enabled: true,
                radius: 4
                }
        },
      ]
    },
    function(chart){
        var s0 = chart.series[1].points;
        var s1 = chart.series[3].points;
        var s2 = chart.series[5];
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

        var values=[t_line,well_id];
        sessionStorage.removeItem("items");
        window.sessionStorage.setItem("items", JSON.stringify(values));
        chart.redraw();
    });

    // createSVGFromChart(directchart_ecdalong, 'pressurelosschart_canvas','ecdalongwell_chart');

}

function ecdchart(ecdchartdata,previous_measured_depth,mudweight,todepth,ecd_chart_max,increasedecdchartdata,ecd_fracturepressure){
   
    var categories=[]
    for(var i=0;i<ecdchartdata.length;i++){
        categories.push(ecdchartdata[i]['x'].toFixed(2))
    }

    var unit=display_depthunit
    directchart_ecdbit = Highcharts.chart('ecd_chart', {
        chart: {
            reflow: false,
        },
        title: {
            text: ''
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            reversed: false,
            title: {
                enabled: true,
                text: 'ECD '+display_densityunit,
            },
            tickInterval : 0.20,
            min:mudweight-0.5,
            max:ecd_chart_max+1,
            gridLineWidth:1,
            // categories: categories

        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD('+unit+')'
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
                    radius: 2,
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
                },
                lineWidth:2,
            },
            series: {
            marker: {
                enabled: false
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
            type:'scatter',
            color: 'rgb(22,96,178)',
            data: ecdchartdata,
            name:'ECD(Without Cuttings)',
            dashStyle: 'Solid',

        },{
            type:'scatter',
            color: '#741413',
            data: increasedecdchartdata,
            name:'ECD(With Cuttings)',
            dashStyle: 'Solid',

        }
        ,{
        name: 'Mud Weight',
        color:'#bb1111',
        data: [{
                x:mudweight,
                y:0,
                marker: {
                    enabled: false,
                    symbol: '',
                    radius: 0
                }
            },{
                x:mudweight,
                y:todepth
            }],
    },
    {
        name:'Fracture Pressure',
        color:'#DB843D',
        data:ecd_fracturepressure
    },
        {
            name: 'Intersect',
            data: [],
            type: 'scatter',
            lineWidth: 0,
            color:'red',
            marker: {
                symbol: 'point',
                enabled: true,
                radius: 4
                }
        },
        {
            type:'line',
            name:'Casing',
            color:'black',
            lineWidth:4,
            data:[{
                x:mudweight-0.5,
                y:0,
                marker: {
                    enabled: false,
                    symbol: ''
                }
            },{
                x:mudweight-0.5,
                y:previous_measured_depth
            }],
            marker: {
                enabled: true,
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
    },
    function(chart){
        var s0 = chart.series[1].points;
        var s1 = chart.series[3].points;
        var s2 = chart.series[4];
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
        window.sessionStorage.setItem("items", JSON.stringify(t_line));
        if(s2.processedXData !=''){
            $('#warning').show();
        }
        else{
            $('#warning').hide();
        }
        chart.redraw();
    }
    );
}

function updateallpressure_barchart(){
    var allpressure_barchartseries = allpressure_barchart.series;

    if(allpressure_barchartseries.length==4){
        allpressure_barchartseries[3].update({
            borderRadiusBottomLeft: '20px',
            borderRadiusBottomRight: '20px'
        });
          
        var lastSeriesIndex = allpressure_barchartseries.length - 1;

        allpressure_barchartseries[0].update({
            borderRadiusTopLeft: '20px',
            borderRadiusTopRight: '20px'

        });
    }
   
}

function ccichart(ccichartdata,maxcci){
    var unit='{%display_depthunit request.session.unit%}';
    directchart_cci = Highcharts.chart('cci_chart', {
        chart: {
            reflow: false,
        },
        title: {
            text: 'CCI'
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            reversed: false,
            gridLineWidth:1,
            title: {
                enabled: true,
                text: 'CCI'
            },
            labels: {
                format: '{value}'
            },
            tickInterval : 1,
            min:0,
            max:maxcci,
            // categories: categories
        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD '+unit,
                enabled: false,

            },
            labels: {
                enabled: false
            },
            tickInterval : 1000,

        },
        legend: { 
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 2,
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
                },
                lineWidth:2,
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
            
        }
        },
        
        series: [
        {
            type:'scatter',
            color: 'rgb(22,96,178)',
            data: ccichartdata,
            name:'CCi',
            dashStyle: 'Solid',

        }
      ]
    });
}

function cuttingsconcentration_chart(cuttingconcentrationdata,cutting_min,cutting_max){
    var unit='{%display_depthunit request.session.unit%}';
    directchart_cc = Highcharts.chart('cuttingconcentration_chart', {
        chart: {
            reflow: false,
        },
        title: {
            text: 'Cuttings Concentration'
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            reversed: false,
            gridLineWidth:1,
            title: {
                enabled: true,
                text: 'Percentage (%)'
            },
            labels: {
                format: '{value} %'
            },
            tickInterval : 1,
            min:0,
            max:cutting_max+5,
            // categories: categories
            plotLines: [{
                color: '#FF0000',
                width: 2,
                zIndex: 3,
                value: 5
            }]
        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD '+unit,
                enabled: false,

            },
            labels: {
                format: '{value}',
                enabled: false,

            },
            tickInterval : 1000,

        },
        legend: { 
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 2,
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
                },
                lineWidth:2,
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
            
        }
        },
        
        series: [
        {
            type:'scatter',
            color: 'rgb(22,96,178)',
            data: cuttingconcentrationdata,
            name:'Cutting Concentration',
            dashStyle: 'Solid',

        }
      ]
    });
}

function transportratiochart(transportratiochartdata){
    var unit='{%display_depthunit request.session.unit%}';
    directchart_tr = Highcharts.chart('transportratio_chart', {
        chart: {
            reflow: false,
        },
        credits: {
        enabled: false
       },
        title: {
            text: 'Transport Ratio'
        },
        xAxis: {
            opposite: true,
            reversed: false,
            gridLineWidth:1,
            title: {
                enabled: true,
                text: 'Percentage (%)'
            },
            labels: {
                format: '{value} %'
            },
            tickInterval : 1,
            min:0,
            max:100,
            // categories: categories
           
        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD '+unit,
                enabled: false,

            },
            labels: {
                enabled: false
            },
            tickInterval : 1000,

        },
        legend: { 
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 2,
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
                },
                lineWidth:2,
            },
            dataLabels: {
                    style: {
                      fontSize: "100px"
            }
            
        }
        },
        
        series: [
        {
            type:'scatter',
            color: 'rgb(22,96,178)',
            data: transportratiochartdata,
            name:'Transport Ratio',
            dashStyle: 'Solid',

        }
      ]
    });
}

function pressurelosschart(chartdata,previous_measured_depth,previous_linear){



    allpressureloss_chart = Highcharts.chart('pressurelosschart', {
        chart: {
            //type: 'spline',
            // zoomType: 'xy'
            reflow: false,
            // symbolPadding: 20,
        },
        exporting: {
        enabled: true,
        allowHTML: true,
        fallbackToExportServer: false
    },
        title: {
            text: ''
        },
        // subtitle: {
        //     text: 'Source: Heinz  2003'
        // },
        xAxis: {
            labels: {
            format:'{value}'
        },
        //     plotBands: [{
        //             color: 'orange', // Color value
        //             from: 5.58, // Start of the plot band
        //             to: 243 // End of the plot band
        //         }],
        //         events: {
        //   mouseover: function(e) {
        //     this.update({
        //       color: 'red'
        //     });
        //   },
        //   mouseout: function(e) {
        //     this.plotBands.color = '';
        //   }
        // },
            opposite: false,
            title: {
                enabled: true,
                text: 'Pressure Loss ('+display_pressureunit+')'
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
                text: 'MD ('+unit+')'
            },
            labels: {
                format: '{value}'
            },
            tickInterval : 1000,

        },
        legend: {
            // layout: 'vertical',
            // align: 'left',
            // verticalAlign: 'top',
            // x: 100,
            // y: 70,
            // floating: true,
            // backgroundColor: Highcharts.defaultOptions.chart.backgroundColor,
            // borderWidth: 1
            
        },
        plotOptions: {
            scatter: {
                marker: {
                    enabled: false,
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
            
        },
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
                // symbol: 'url(../../../../static/images/chart/casing.png)',
                symbol: 'url(' + casing_image_url + ')',
                width: 30,
                height: 30,

            },
            label: {
                    connectorAllowed: true,
                    enabled:false
            }
        }
      ],
      exporting: {
        pdf: {
          scale: 1,
        },
      },
    });

}

function  createSVGFromChart(chart,target,name = ''){
    let svgString = chart.getSVG();
    let parser = new DOMParser(); 
    let svgElem = parser.parseFromString(svgString, "image/svg+xml").documentElement;
    let s = new XMLSerializer().serializeToString(svgElem);
    let b64 = 'data:image/svg+xml;base64,';
    b64 += btoa(s);

    svgString2Image(b64, 800, 600, 'png', function (pngData) {
        img = pngData.replace('data:image/png;base64,', '');
        var data ={
            png:img,
            filename:name,
        }
        $.ajax({
        type: "POST",
        url: "/wells/muddata/chart_image",
        data: {
            csrfmiddlewaretoken: csrf,
            data:data
        },
        success: function(data){
            // alert(data);
        }
        });
    });






        
    
    

}

function svgString2Image(svgString, width, height, format, callback) {
    format = format ? format : 'png';
    var svgData = svgString

    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;
    var image = new Image();
    image.onload = function () { 
        context.clearRect(0, 0, width, height);
        context.drawImage(image, 0, 0, width, height);
        var pngData = canvas.toDataURL('image/' + format);
        callback(pngData);
    }; 
    image.src = svgData;
}


function isSeriesExists(seriesName,chart) {
    const series = chart.series;
    for (let i = 0; i < series.length; i++) {
      if (series[i].name === seriesName) {
        return true;
      }
    }
    return false;
}


