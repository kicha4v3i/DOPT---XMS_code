$(document).ready(function() {
    $(".pressure-phase").click(function(){
        $('.myDIV').removeClass('show');
        let btn = $(this).next();
        $('.myDIV').not(btn).removeClass('show');  
        if(btn.hasClass("show")){
            btn.removeClass('show');
        }else{
            btn.addClass('show');
        }
       
    });
    $(document).on("click",'.wellphase_sidemenu',function(){
        var section_name=$(this).attr('data-id')
        var wellphase_id=$(this).attr('wellphase_id')
        $.ajax({
            type: "GET",
            url:"/wells/muddata/checkmudmotor",
            cache: false,        

            data:{
                wellphase_id:wellphase_id,
                section_name:section_name
                
            },
            success: function(data) {
                var html=''
                if(data.status=='true'){
                    html +='<div class="row" id="torque_row">'
                    html +='<div class="col-2"><label>Torque</label></div>'
                    html +='<div class="col-3"><input type="text" name="torque" id="torque" class="form-control" placeholder="Torque"></div>'
                    html +='</div>'
                    html +='<div class="row" id="wob_row">'
                    html +='<div class="col-2"><label>Working WOB</label></div>'
                    html +='<div class="col-3"><input type="text" name="wob" id="wob" class="form-control" placeholder="WOB"></div>'
                    html +='</div>'
                    $('#drilling_parameters').append(html)
                }
                else{
                   $('#torque_row').remove() 
                   $('#wob_row').remove() 
                }
                $('#bitdepth_labels').val(data.rangelabels.toString())
                
                bitdepthrange()
                $('#bitdepth_slider').prop('min', data.sectionfromdepth );
                $('#bitdepth_slider').prop('max',  data.sectiontodepth);
                $('#bitdepth_slider').rangeslider('update', true);
            }
        })
    })
    $('#calculate_optimization').click(function(){
        calculateoptimization()
    })
    $('#no_of_nozzle').blur(function(){
        calculateoptimization()
    })
})
function calculateoptimization(){
    var optimization_code=$('input[name="optimization_code"]:checked').val();
    var pump_spm=$('#pump_spm').val()
    var maximum_pressure=$('#maximum_pressure').val()
    var pump_efficiency=$('#pump_efficiency').val()
    var mechanical_efficiency=$('#mechanical_efficiency').val()
    var max_flowrate=$('#max_flowrate').val()
    var min_flowrate=$('#min_flowrate').val()
    var no_of_nozzle=$('#no_of_nozzle').val()
    var original_tfa=$('#original_tfa').val()
    newoptimizecalculation(optimization_code,pump_spm,maximum_pressure,pump_efficiency,mechanical_efficiency,max_flowrate,min_flowrate,rpm_input,rop_input,wellphase_id,section_name,no_of_nozzle,original_tfa)

}
function newoptimizecalculation(optimization_code,pump_spm,maximum_pressure,pump_efficiency,mechanical_efficiency,max_flowrate,min_flowrate,rpm_input,rop_input,wellphase_id,section_name,no_of_nozzle,original_tfa,increased_tfa='',final_opt_flowrate='',optimum_flowrate_pressure='',type=''){
    $.ajax({
        type: "GET",
        url:"/pressureloss/calculateoptimization",
        cache: false,        
        data:{
            optimization_code:optimization_code,
            pump_spm:pump_spm,
            maximum_pressure:maximum_pressure,
            pump_efficiency:pump_efficiency,
            mechanical_efficiency:mechanical_efficiency,
            max_flowrate:max_flowrate,
            min_flowrate:min_flowrate,
            rpm_input:rpm_input,
            rop_input:rop_input,
            wellphase_id:wellphase_id,
            section_name:section_name,
            no_of_nozzle:no_of_nozzle,
            original_tfa:original_tfa,
            final_opt_flowrate:final_opt_flowrate,
            optimum_flowrate_pressure:optimum_flowrate_pressure,
            type:type,
            increased_tfa:increased_tfa
        },
        beforeSend: function() {
        $('#loader').removeClass('hidden')
        },
        success: function(data) {
           
            // console.log(data.optimum_nozzle_size.length)
            if(data.calculated_nozzle_count<no_of_nozzle){
                $('#error').html('You cannot set number of nozzle '+no_of_nozzle+'')
            }
            else if(data.final_optimum_nozzle_size.length>0){
                if(data.final_pump_pressure<=maximum_pressure){
                    hsichart(data.hsi_chartdata,data.original_hsi_chartdata,data.minlimit,data.maxlimit,data.maximum_hsi)
                    impactforcechart(data.impactforce_chartdata,data.original_impactforce_chartdata,data.minlimit,data.maxlimit,data.max_IF)
                    flowratechart(data.bitpressure_chartdata,data.totalpressure_chartdata,maximum_pressure,data.final_opt_flowrate,data.min_flowrate_chart,data.max_flowrate_chart,data.max_pressureloss,data.original_bitpressure_chartdata,data.original_totalpressure_chartdata,data.surface_rating)
                    $('#no_of_nozzle').val(data.nozzle_size)
                    var  html=''
                    $.each(data.final_optimum_nozzle_size,function(key,value){                 
                        // console.log(key)
                        html +=value.countt+'X'+value.nozzle_size
                        if(key<data.final_optimum_nozzle_size.length-1){
                          html +=','  
                        }
                    })
                       // console.log(data.impact_force)
                    $('#nozzle_size').html(html)
                    $('#opt_flowrate').html(data.final_opt_flowrate+' gpm')
                    $('#tfa').html(data.final_tfa+' in <sup>2</sup>')
                    $('#pump_pressure').html(data.final_pump_pressure+' psi')
                    $('#bhhp').html(data.final_hsi+' hp/in<sup>2</sup>')
                    $('#impact_force_value').html(data.final_impact_forces+' lbf')
                }
                else{
                    Swal.fire({
                        title: 'In order to achieve the optimum flowrate,the surface pressure exceeds the set maximum circulating pressure.\nwould you like to increase the maximum circulating pressure to '+data.final_pump_pressure+'psi',
                        showCancelButton: true,
                        confirmButtonText: `Yes`,
                        cancelButtonText: "No",
                        allowOutsideClick: false,
                        }).then((result) => {
                        /* Read more about isConfirmed, isDenied below */
                        if (result.isConfirmed) {
                            hsichart(data.hsi_chartdata,data.original_hsi_chartdata,data.minlimit,data.maxlimit,data.maximum_hsi)
                            impactforcechart(data.impactforce_chartdata,data.original_impactforce_chartdata,data.minlimit,data.maxlimit,data.max_IF)
                            flowratechart(data.bitpressure_chartdata,data.totalpressure_chartdata,data.final_pump_pressure,data.final_opt_flowrate,data.min_flowrate_chart,data.max_flowrate_chart,data.max_pressureloss,data.original_bitpressure_chartdata,data.original_totalpressure_chartdata,data.surface_rating)
                            $('#no_of_nozzle').val(data.nozzle_size)
                            var  html=''
                            $.each(data.final_optimum_nozzle_size,function(key,value){                 
                                // console.log(key)
                                html +=value.countt+'X'+value.nozzle_size
                                if(key<data.final_optimum_nozzle_size.length-1){
                                html +=','  
                                }
                            })
                            // console.log(data.impact_force)
                            $('#nozzle_size').html(html)
                            $('#opt_flowrate').html(data.final_opt_flowrate+' gpm')
                            $('#tfa').html(data.final_tfa+' in <sup>2</sup>')
                            $('#pump_pressure').html(data.final_pump_pressure+' psi')
                            $('#bhhp').html(data.final_hsi+' hp/in<sup>2</sup>')
                            $('#impact_force_value').html(data.final_impact_forces+' lbf')

                        } else {                            
                            increased_tfa=data.final_tfa+0.1
                            newoptimizecalculation(optimization_code,pump_spm,maximum_pressure,pump_efficiency,mechanical_efficiency,max_flowrate,min_flowrate,rpm_input,rop_input,wellphase_id,section_name,no_of_nozzle,original_tfa,increased_tfa,data.final_opt_flowrate,data.optimum_flowrate_pressure,'increased')
                           


                        }
                    })
                }
                
            }
            else{
                $('#error').html('You cannot set number of nozzle '+data.nozzle_size+'')
            }
            
         
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
     
    });

}
function flowratechart(bitpressure_chartdata,totalpressure_chartdata,maximum_pressure,opt_flowrate,min_flowrate_chart,max_flowrate_chart,max_pressureloss,original_bitpressure_chartdata,original_totalpressure_chartdata,surface_rating){
    console.log(surface_rating)
    console.log(maximum_pressure)
    plotLineId = 'myPlotLine'; 
    opt_flowrate_plot_id='opt_flowrate'
    surface_rating_plot_id='surface_rating'
    plotLineOptions = {
        color: '#FF0000',
        id: plotLineId, 
        width: 2,
        value: maximum_pressure,
        dashStyle: 'solid'
    }
    surfaceplotoptions={
        color: '#FF0000',
        id: surface_rating_plot_id, 
        width: 2,
        value: surface_rating,
        dashStyle: 'solid' 
    }
    opt_flowrate_plot = {
        color: 'blue',
        id: opt_flowrate_plot_id, 
        width: 2,
        value: opt_flowrate,
        dashStyle: 'ShortDash'
    };
    var chart=Highcharts.chart('flowrate_chart', {
        title: {
            text: 'Pressure'
        },
       
        xAxis: {
            title: {
                enabled: true,
                text: 'Flowrate(gpm)'
            },
            tickInterval : 50,
            plotLines: [ opt_flowrate_plot],
            min:min_flowrate_chart,
            max:max_flowrate_chart

    
        },
        yAxis: {
            title: {
                text: 'Pressure(psi)'
            },
            tickInterval : 1000,
            labels: {
                format: '{value}'
            },
            plotLines: [ plotLineOptions,surfaceplotoptions],
            min:0,
            max:surface_rating+1000
    
        },
    
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        
        series: [
        {
            color: '#FF0000',
            name: 'Max Pressure',
            marker: {
                enabled: false
            },
            events: {
                legendItemClick: function(e) {
                    if(this.visible) {
                        this.chart.yAxis[0].removePlotLine(plotLineId);
                    }
                    else {
                        this.chart.yAxis[0].addPlotLine(plotLineOptions);
                    }
                }
            }
        },
        {
            color: 'blue',
            name: 'Optimum Flowrate',
            marker: {
                enabled: false
            },
            events: {
                legendItemClick: function(e) {
                    if(this.visible) {
                        this.chart.xAxis[0].removePlotLine(opt_flowrate_plot_id);
                    }
                    else {
                        this.chart.xAxis[0].addPlotLine(opt_flowrate_plot);
                    }
                }
            }
        },
        {
            type: 'spline',
            name: 'Optimum TFA',
            color: 'brown',
            data: bitpressure_chartdata,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
            visible:false
        },
        {
            type: 'spline',
            name: 'Original TFA',
            color: 'brown',
            data: original_bitpressure_chartdata,
            dashStyle: 'ShortDash',
            marker: {
                enabled: false
            },
            visible:false
        },
        {
            type: 'spline',
            name: 'Optimum TFA',
            color: 'Blue',
            data: totalpressure_chartdata,
            dashStyle: 'Solid',
        },
        {
            type: 'spline',
            name: 'Original TFA',
            color: 'Blue',
            data: original_totalpressure_chartdata,
            dashStyle: 'ShortDash',
        },
      ]
    });
}
function impactforcechart(impactforce_chartdata,original_impactforce_chartdata,minlimit,maxlimit,max_IF){
    Highcharts.chart('impactforce_chart', {
        title: {
            text: 'Optimum Impact Force'
        },
       
        xAxis: {
            title: {
                enabled: true,
                text: 'Flowrate(gpm)'
            },
            tickInterval : 50,
            min:minlimit,
            max:maxlimit
    
        },
        yAxis: {
            title: {
                text: 'ImpactForce'
            },
            tickInterval : 100,
            labels: {
                format: '{value}'
            },
            min:0,
            max:max_IF
          
    
        },
    
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        
        series: [
        {
            type: 'spline',
            name: 'Optimum TFA',
            color: 'rgb(22,96,178)',
            data: impactforce_chartdata,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },
        {
            type: 'spline',
            name: 'Original TFA',
            color: 'rgb(22,96,178)',
            data: original_impactforce_chartdata,
            dashStyle: 'ShortDash',
            marker: {
                enabled: false
            },
        },
      ]
    });

}
function hsichart(hsi_chartdata,original_hsi_chartdata,minlimit,maxlimit,maximum_hsi){
    Highcharts.chart('hsi_chart', {
        title: {
            text: 'Optimum Hsi'
        },
       
        xAxis: {
            title: {
                enabled: true,
                text: 'Flowrate(gpm)'
            },
            tickInterval : 50,
            min:minlimit,
            max:maxlimit
    
        },
        yAxis: {
            title: {
                text: 'HSI'
            },
            tickInterval : 2,
            labels: {
                format: '{value}'
            },
            min:0,
            max:maximum_hsi
            
    
        },
    
        plotOptions: {
            spline: {
                marker: {
                    enabled: false
                }
            }
        },
        
        series: [
        {
            type: 'spline',
            name: 'Optimum TFA',
            color: 'rgb(22,96,178)',
            data: hsi_chartdata,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },
        {
            type: 'spline',
            name: 'Original TFA',
            color: 'rgb(22,96,178)',
            data: original_hsi_chartdata,
            dashStyle: 'ShortDash',
            marker: {
                enabled: false
            },
        },
      ]
    });

}