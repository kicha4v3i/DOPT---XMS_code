$(document).ready(function() {
    // console.log(depth)
    flowratedepth=[];
    ropdepth=[];
    rpmdepth=[];
    ecddepth=[];
    surface_pumpdepth=[];
    flowrate_time=[];
    rop_time=[];
    rpm_time=[];
    ecd_time=[];
    surface_pumptime=[];
    for(var i=0; i<depth.length;i++){
        flowratedepth.push({'x':flowrate[i],'y':depth[i]});
        ropdepth.push({'x':rop[i],'y':depth[i]});
        rpmdepth.push({'x':rpm[i],'y':depth[i]});
        ecddepth.push({'x':ecd[i],'y':depth[i]});
        surface_pumpdepth.push({'x':pump_pressure[i],'y':depth[i]});
    }
    last_depth=depth[depth.length-1];
    console.log(last_depth)
    surface_plan=[];
    ecd_plan=[]
    plan_surface=[];
    plan_ecd=[];
    $.ajax({
        type: "GET",
        url:"/wells/muddata/get_planwell_data",
        cache: false,        
        data:{
            planwell_id:planwell_id,
            well_id:well_id,
            wellphase_id:wellphase_id,
            last_depth:last_depth

        },
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },
        success: function(data) {    
            console.log(data);
            // total_annularloss=0
            // totalpipeloss=0
            // totalsurfacelosses=0
            // totalbore_pressurelosses=0
            // totalbit_losses=0

            // for(var i=data.annular_data.length-1;i>=0;i--){
            //     total_annularloss=total_annularloss+Math.round(data.annular_data[i].pressureloss)
            //     totalpipeloss=totalpipeloss+Math.round(data.annular_data[i].drillstringloss)
            // }
            // // for(var i=0;i<data.bore_pressure_data.length;i++){
            // //     totalbore_pressurelosses=totalbore_pressurelosses+Math.round(data.bore_pressure_data[i].pressureloss)
            // // }
            // for(var i=0;i<data.surface_losses.length;i++){
            //     totalsurfacelosses=totalsurfacelosses+Math.round(data.surface_losses[i].pressureloss)
            // }
            // for(var i=0;i<data.bit_losses.length;i++){
            //     totalbit_losses=Math.round(data.bit_losses[i].bit_pressure_loss)
            // }
            // totalpressureloss = totalsurfacelosses+totalpipeloss+total_annularloss+totalbit_losses
            
            // for(var i=0; i<data.surface_pressure.length;i++){
            //     surface_plan.push({'x':data.surface_pressure[i],'y':depth[i]});
            // }
            for(var i=0; i<depth.length;i++){
                plan_surface.push({'x':data.plan_surface[i],'y':depth[i]});
            }
            // for(var i=0; i<depth.length;i++){
            //     plan_ecd.push({'x':data.ecdchartdata[i],'y':depth[i]});
            // }
            
            // console.log(totalpressureloss);
            // console.log(ecd_plan);
            // console.log(plan_surface);
            // console.log(plan_ecd)
            surfacepressure_depth_chart(surface_pumpdepth,plan_surface,wellphase_id);
            ecd_depth_chart(ecddepth,data.ecdchartdata,wellphase_id);
            // createSVGFromChart(ecd_chart, 'pressurelosschart_canvas','ecd_chart-'+wellphase_id);
        },
        complete: function(){
            $('#loader').addClass('hidden')

        },
    })
    flowratedepth_chart(flowratedepth,wellphase_id);
    ropdepth_chart(ropdepth,wellphase_id);
    rpmdepth_chart(rpmdepth,wellphase_id);
    $('#user_depth').val(depth[depth.length-1]);
    surface_pumpdepth_chart(surface_pumpdepth);
    ecddepth_chart(ecddepth);

     
})
$(document).on('change','.report_chart_type',function() {
    var current_chart_type=$(this).val()
    var wellphase_id=$(this).attr('wellphase_id')
    var url=$('#phase_report_hidden').attr('href')
    $('.report_chart_type:checked').each(function(index,value){
        console.log($(this).val())
        console.log(index)
        if(index==0){
            url= url+'?'+$(this).val()+'=1'
        }
        else{
            url= url+'&'+$(this).val()+'=1'
        }
    })

    $("#phase_report").prop("href", url)
})
$(document).on('blur','#user_depth',function() {
    var depth=$(this).val();
    var selected_model=$('.user_selected').val();
    var cutting_density=$('#user_cutting_density').val();
    var cutting_size=$('#user_cutting_size').val();
    get_calculated_data(cutting_density,cutting_size,selected_model,depth);
})
$(document).on('change','.user_modalselect',function() {
    var selected_model=$(this).val();
    $('.user_selected').val(selected_model);
    $.ajax({
        type: "GET",
        url:"/wells/muddata/addselected_data",
        cache: false,        
        data:{
            well_id:well_id,
            wellphase_id:wellphase_id,
            selected_model:selected_model
        }, 
        success: function(data) {       
        }
    })
    var cutting_density=$('#user_cutting_density').val();
    var cutting_size=$('#user_cutting_size').val();
    var user_depth = $('#user_depth').val();
    get_calculated_data(cutting_density,cutting_size,selected_model,user_depth);
})

function get_calculated_data(cutting_density,cutting_size,selected_model,user_depth){
    $.ajax({
        type: "GET",
        url:"/wells/muddata/get_calculated_data",
        cache: false,        
        data:{
            planwell_id:planwell_id,
            well_id:well_id,
            wellphase_id:wellphase_id,
            selected_model:selected_model,
            cutting_density:cutting_density,
            cutting_size:cutting_size,
            user_depth:user_depth
        },
        
        success: function(data) {
            slipvel_chart(data.annular_data.slipvelocitychart,data.annular_data.annularvelocitychartdata)
            cci_chart(data.annular_data.cci,data.max_cci)
            var cutting_min=parseInt(data.annular_data.cuttingsconcentration[0].x.toFixed());
            var cutting_max=parseInt($(data.annular_data.cuttingsconcentration).last()[0].x);
            cutting_conc_chart(data.annular_data.cuttingsconcentration,cutting_min,cutting_max)
            transportratio_chart(data.annular_data.transportratio)
        }
    })
}



// Depth Charts
function surfacepressure_depth_chart(surface_pumpdepth,surface_plan,wellphase_id){

   surface_pressure_chart=Highcharts.chart('surfacepressure_depth_chart', {
            chart: {
                reflow: false,
                
            },
            title: {
                text: 'Surface Pressure'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} psi',
                    enabled: true
                    
                },
                    // categories: categories
                    // tickInterval : 500,

                },
                yAxis: {
                reversed: true,
                opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
    
                },
                labels: {
                    format: '{value} ft',
                    // enabled: false,
                    
                },
                
                // tickInterval : 500,
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
                    turboThreshold: 1000000      
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
                // data: [{'x':1922.66,'y':7496},{'x':1921.28,'y':7496.5},{'x': 1917.67, 'y': 7497},{'x': 1234.69, 'y': 7497.5},{'x': 1675.54, 'y': 7498},{'x': 1304.08, 'y': 7498.5}],
                data:surface_pumpdepth,
                name:'Surface pump',
                dashStyle: 'Solid',
    
            },
            {
                type:'line',
                color: 'rgb(128, 128, 128)',
                data: surface_plan,
                // data: [{'x': 556, 'y': 1700},{'x': 556, 'y': 3000}],
                name:'plan Surface pump',
                dashStyle: 'Solid',
    
            }
          ]
        });
        createSVGFromChart(surface_pressure_chart, 'pressurelosscharts_canvas','surface_pressure_chart'+wellphase_id);
}
function ecd_depth_chart(ecddepth,ecd_plan,wellphase_id){
    ecddepthchart=Highcharts.chart('ecd_depth_chart', {
        chart: {
            reflow: false,
           width:350
        },
        title: {
            text: 'ECD'
        },
        credits: {
        enabled: false
       },
        xAxis: {
            opposite: true,
            reversed: false,
            // gridLineWidth:1,
            title: {
                enabled: true,
                text: ''
            },
            labels: {
                format: '{value} GPM',
                enabled: true
                
            },
                // categories: categories

            },
            yAxis: {
                reversed: true,
                opposite: false,
            title: {
                text:'Depth',
                enabled: false,
                
            },
            labels: {
                format: '{value} ft',
                // enabled: false,
                
            },
            // tickInterval : 500,
            
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
                turboThreshold: 1000000      
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
            data: ecddepth,
            name:'ECD',
            dashStyle: 'Solid',

        },
            {
                type:'line',
                color: 'rgb(128, 128, 128)',
                data: ecd_plan,
                // data: [{'x': 556, 'y': 1700},{'x': 556, 'y': 3000}],
                name:'plan ECD',
                dashStyle: 'Solid',
    
            }
          ]
        });
        createSVGFromChart(ecddepthchart, 'ecdcharts_canvas','ecdchart'+wellphase_id);
}
function flowratedepth_chart(flowratedepth,wellphase_id){
    flowratechart=Highcharts.chart('flowratedepth_chart', {
            chart: {
                reflow: false,
               width:350
            },
            title: {
                text: 'Flowrate'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} GPM',
                    enabled: true
                    
                },
                    // categories: categories

                },
                yAxis: {
                    reversed: true,
                    opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
                    
                },
                labels: {
                    format: '{value} ft',
                    // enabled: false,
                    
                },
                // tickInterval : 500,
                
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
                    turboThreshold: 1000000      
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
                data: flowratedepth,
                name:'Flowrate',
                dashStyle: 'Solid',
    
            }
          ]
        });
        createSVGFromChart(flowratechart, 'pressurelosscharts_canvas','flowrate_chart'+wellphase_id);

}
function ropdepth_chart(ropdepth,ropdepth_chart){
    rop_chart=Highcharts.chart('ropdepth_chart', {
            chart: {
                reflow: false,
                width:350
            },
            title: {
                text: 'ROP'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} ft/h',
                    enabled: true
                    
                },
                    // categories: categories

                },
                yAxis: {
                reversed: true,
                opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
    
                },
                labels: {
                    format: '{value} ft',
                    enabled: false,
                    
                },
                tickInterval : 500,
                
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
                    turboThreshold: 1000000      
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
                data: ropdepth,
                name:'rop',
                dashStyle: 'Solid',
    
            }         
          ]
        });
        createSVGFromChart(rop_chart, 'pressurelosscharts_canvas','rop_chart'+wellphase_id);

}
function rpmdepth_chart(rpmdepth,wellphase_id){
    rpm_chart=Highcharts.chart('rpmdepth_chart', {
            chart: {
                reflow: false,
                width:350
            },
            title: {
                text: 'RPM'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} rpm',
                    enabled: true
                    
                },
                    // categories: categories

                },
                yAxis: {
                    reversed: true,
                opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
    
                },
                labels: {
                    format: '{value} ft',
                    enabled: false,
    
                },
    
                tickInterval : 500 ,
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
                    turboThreshold: 1000000      
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
                data: rpmdepth,
                name:'RPM',
                dashStyle: 'Solid',
    
            }
          ]
        });
        createSVGFromChart(rpm_chart, 'pressurelosscharts_canvas','rpm_chart'+wellphase_id);


}
function ecddepth_chart(ecddepth){
    Highcharts.chart('ecddepth_chart', {
            chart: {
                reflow: false,
                width:350
            },
            title: {
                text: 'ECD'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} ppg',
                    enabled: true
                    
                },
                    // categories: categories

                },
                yAxis: {
                reversed: true,
                opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
    
                },
                labels: {
                    format: '{value} ft',
                    enabled: false,
    
                },
                tickInterval : 500,
    
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
                    turboThreshold: 1000000      
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
                data: ecddepth,
                name:'ECD',
                dashStyle: 'Solid',
    
            }
          ]
        });
}
function surface_pumpdepth_chart(surface_pumpdepth){
    Highcharts.chart('surfacepressuredepth_chart', {
            chart: {
                reflow: false,
                width:350
            },
            title: {
                text: 'Surface Pressure'
            },
            credits: {
            enabled: false
           },
            xAxis: {
                opposite: true,
                reversed: false,
                // gridLineWidth:1,
                title: {
                    enabled: true,
                    text: ''
                },
                labels: {
                    format: '{value} psi',
                    enabled: true
                    
                },
                    // categories: categories

                },
                yAxis: {
                reversed: true,
                opposite: false,
                title: {
                    text:'Depth',
                    enabled: false,
    
                },
                labels: {
                    format: '{value} (ft',
                    enabled: false,
    
                },
                tickInterval : 500,
    
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
                    turboThreshold: 1000000      
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
                data: surface_pumpdepth,
                name:'Surface pump',
                dashStyle: 'Solid',
    
            }
          ]
        });
}

// Slip velocity Chart
function slipvel_chart(slipvelocitychart,annularvelocitychartdata){
    directchart = Highcharts.chart('slipvel_chart', {
        chart: {
            reflow: false,
            width:350
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
                text: 'Velocity (ft)'
            },
            tickInterval : 10,


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
            tickInterval : 500,

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
            series: {
                turboThreshold: 1000000      
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
function cci_chart(ccichartdata,maxcci){
    var unit='{%display_depthunit request.session.unit%}';
    directchart = Highcharts.chart('cci_chart', {
        chart: {
            reflow: false,
            width:350
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
            max:maxcci+3,
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
            tickInterval : 500,

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
                turboThreshold: 1000000      
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
function cutting_conc_chart(cuttingconcentrationdata,cutting_min,cutting_max){
    var unit='{%display_depthunit request.session.unit%}';
    directchart = Highcharts.chart('cutting_conc_chart', {
        chart: {
            reflow: false,
            width:350
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
            series: {
                turboThreshold: 1000000      
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
function transportratio_chart(transportratiochartdata){
    var unit='{%display_depthunit request.session.unit%}';
    directchart = Highcharts.chart('tr_chart', {
        chart: {
            reflow: false,
            width:350
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
            series: {
                turboThreshold: 1000000      
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
function createSVGFromChart(chart,target,name = ''){
    // console.log('gfg',chart)
    var ret = chart.getSVGForExport().replace('<div aria-hidden="false" class="highcharts-a11y-proxy-container-before" style="top: 0px; left: 0px; white-space: nowrap; position: absolute;"></div>','');
    canvg(document.getElementById(target),ret);
    var canvas = document.getElementById(target)
    var img = canvas.toDataURL("image/png");
    img = img.replace('data:image/png;base64,', '');
        var data ={
            png:img,
            filename:name,
            type: 'image/png',
        }
        $.ajax({
        type: "POST",
        url: "/wells/muddata/chart_image",
        data: {
            csrfmiddlewaretoken: csrf_token,
            data:data
        },
        success: function(data){
            // alert(data);
        }
        });
}