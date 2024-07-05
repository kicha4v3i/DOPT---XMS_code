$('.change_sensitive_unit').click(function(){
    var unit = $('#change_units').val();
    var flowrate=$('.flowrate').val();
    var rpm=$('.rpm').val();
    var rop=$('#rop_userenter').val();
    var cuttings_density=$('#cuttings_density').val()
    var cuttings_size=$('#cuttings_size').val()
    var mudweight=$('#mudweight_hidden').val()
    var plastic_viscocity=$('#pv_hidden').val()
    var yieldpoint=$('#yp_hidden').val()
    var bitdepth=$('#todepth_hidden').val()
    if(unit == 'API'){
        $('#flowrate_sensitivity').val(Math.round(flowrate*3.78))
        $('#rop_sensitivity').val(Math.round(rop/3.281,2))
        $('#cs_sensitivity').val((cuttings_size*1000/3.281/12).toFixed(2))
        $('#cd_sensitivity').val((cuttings_density/8.33).toFixed(2))
        $('#mudweight_sensitivity').val(Math.round(mudweight/8.345,2))
        $('#pv_sensitivity').val(Math.round(plastic_viscocity/1000,2))
        $('#yp_sensitivity').val(Math.round(yieldpoint/0.4788,2))
        $('#flowrate-unit').html('(LPM)');
        $('#mudweight-unit').html('(g/cc)');
        $('#rop-unit').html('(m/h)');
        $('#cs-unit').html('(g/cc)');
        $('#cd-unit').html('(g/cc)');
        $('#pv-unit').html('(Pa.sec)');
        $('#yp-unit').html('(Pa)');
    }else{
        $('#flowrate_sensitivity').val((flowrate*0.2647).toFixed())
        $('#rop_sensitivity').val((rop*3.281).toFixed(2))
        $('#cs_sensitivity').val((cuttings_size/1000*3.281*12).toFixed(2))
        $('#cd_sensitivity').val((cuttings_density*8.33).toFixed(2))
        $('#mudweight_sensitivity').val((mudweight*8.345).toFixed(2))
        $('#pv_sensitivity').val((plastic_viscocity*1000).toFixed(2))
        $('#yp_sensitivity').val((yieldpoint*0.4788).toFixed(2))
        $('#flowrate-unit').html('(GPM)');
        $('#mudweight-unit').html('(ft/h)');
        $('#rop-unit').html('(LPM)');
        $('#cs-unit').html('(ppg)');
        $('#cd-unit').html('(ppg)');
        $('#pv-unit').html('(cP)');
        $('#yp-unit').html('(lbf/100ft2)');
    }
    sensitivity_unitchange(sensitivity)
    function sensitivity_unitchange(data){
        // console.log(data);
        
        if(unit == 'API'){
            var pressure = 'kPa';
            var flowrate = 'LPF';
            var mud_weight = 'g/cc';
            var tfa = 'mm<sup>2</sup>';
            var rop = 'm/hr';
            var viscocity = 'Pa.sec';
            var yeildpoint = 'Pa';
            var ecd = 'g/cc';

        }else{
            var pressure = 'psi';
            var flowrate = 'GPM';
            var mud_weight = 'ppg';
            var tfa = 'in<sup>2</sup>';
            var rop = 'ft/hr';
            var viscocity = 'cP';
            var yeildpoint = 'lbf/100ft^2';
            var ecd = 'ppg';

        }
        var sensitivity_yieldpoint=[];
        var sensitivity_viscocity=[];
        var sensitivity_mudweight=[];
        var sensitivity_tfa=[];
        var sensitivity_tfa_bit=[];
        var sensitivity_flowrate=[];
        var sensitivity_flowrate_ecd=[];
        var sensitivity_mudweight_ecd=[];
        var sensitivity_viscocity_ecd=[];
        var sensitivity_rop_withecd=[];
        var sensitivity_rop_withoutecd =[];
        var sensitivity_cd_withecd =[];
        var sensitivity_cd_withoutecd =[];

        if (unit == 'API'){
            for(var i=data.sensitivity_yieldpoint_chart.result.length-1;i>=0;i--){
                sensitivity_yieldpoint.push({'x':data.sensitivity_yieldpoint_chart.result[i].x/0.4788,'y':data.sensitivity_yieldpoint_chart.result[i].y*6.894757});
            }
            for(var i=data.sensitivity_viscocity_chart.result.length-1;i>=0;i--){
                sensitivity_viscocity.push({'x':data.sensitivity_viscocity_chart.result[i].x/1000,'y':data.sensitivity_viscocity_chart.result[i].y*6.894757});
            }
            for(var i=data.sensitivity_mudweight_chart.result.length-1;i>=0;i--){
                sensitivity_mudweight.push({'x':data.sensitivity_mudweight_chart.result[i].x/8.345,'y':data.sensitivity_mudweight_chart.result[i].y*6.894757});
            }
            for(var i=data.sensitivity_tfa_chart.result.length-1;i>=0;i--){
                sensitivity_tfa.push({'x':data.sensitivity_tfa_chart.result[i].x,'y':data.sensitivity_tfa_chart.result[i].y*6.894757});
            }
            for(var i=data.sensitivity_tfa_chart.bit_pressure_chart.length-1;i>=0;i--){
                sensitivity_tfa_bit.push({'x':data.sensitivity_tfa_chart.bit_pressure_chart[i].x,'y':data.sensitivity_tfa_chart.bit_pressure_chart[i].y*6.894757});
            }
            for(var i=data.sensitivity_flowrate_chart.result.length-1;i>=0;i--){
                sensitivity_flowrate.push({'x':data.sensitivity_flowrate_chart.result[i].x*3.78,'y':data.sensitivity_flowrate_chart.result[i].y*6.894757});
            }
            // ECD Calculation
            for(var i=data.sensitivity_flowrate_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_flowrate_ecd.push({'x':data.sensitivity_flowrate_chart.ecd_without[i].x*3.78,'y':data.sensitivity_flowrate_chart.ecd_without[i].y});
            }
            for(var i=data.sensitivity_mudweight_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_mudweight_ecd.push({'x':data.sensitivity_mudweight_chart.ecd_without[i].x/8.345,'y':data.sensitivity_mudweight_chart.ecd_without[i].y});
            }
            for(var i=data.sensitivity_viscocity_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_viscocity_ecd.push({'x':data.sensitivity_viscocity_chart.ecd_without[i].x/1000,'y':data.sensitivity_viscocity_chart.ecd_without[i].y});
            }
            for(var i=data.ropecdchart.ecd_with.length-1;i>=0;i--){
                sensitivity_rop_withecd.push({'x':data.ropecdchart.ecd_with[i].x/3.281,'y':data.ropecdchart.ecd_with[i].y});
            }
            for(var i=data.ropecdchart.ecd_without.length-1;i>=0;i--){
                sensitivity_rop_withoutecd.push({'x':data.ropecdchart.ecd_without[i].x/3.281,'y':data.ropecdchart.ecd_without[i].y});
            }
            // for(var i=data.cuttingsdensityecdchart.ecd_with.length-1;i>=0;i--){
            //     sensitivity_cd_withecd.push({'x':data.cuttingsdensityecdchart.ecd_with[i].x/3.281,'y':data.cuttingsdensityecdchart.ecd_with[i].y});
            // }
            // for(var i=data.cuttingsdensityecdchart.ecd_without.length-1;i>=0;i--){
            //     sensitivity_cd_withoutecd.push({'x':data.cuttingsdensityecdchart.ecd_without[i].x/3.281,'y':data.cuttingsdensityecdchart.ecd_without[i].y});
            // }
        }else{
            for(var i=data.sensitivity_yieldpoint_chart.result.length-1;i>=0;i--){
                sensitivity_yieldpoint.push({'x':data.sensitivity_yieldpoint_chart.result[i].x*0.4788,'y':data.sensitivity_yieldpoint_chart.result[i].y/6.894757});
            }
            for(var i=data.sensitivity_viscocity_chart.result.length-1;i>=0;i--){
                sensitivity_viscocity.push({'x':data.sensitivity_viscocity_chart.result[i].x*1000,'y':data.sensitivity_viscocity_chart.result[i].y/6.894757});
            }
            for(var i=data.sensitivity_mudweight_chart.result.length-1;i>=0;i--){
                sensitivity_mudweight.push({'x':data.sensitivity_mudweight_chart.result[i].x*8.345,'y':data.sensitivity_mudweight_chart.result[i].y/6.894757});
            }
            for(var i=data.sensitivity_tfa_chart.result.length-1;i>=0;i--){
                sensitivity_tfa.push({'x':data.sensitivity_tfa_chart.result[i].x,'y':data.sensitivity_tfa_chart.result[i].y/6.894757});
            }
            for(var i=data.sensitivity_tfa_chart.bit_pressure_chart.length-1;i>=0;i--){
                sensitivity_tfa_bit.push({'x':data.sensitivity_tfa_chart.bit_pressure_chart[i].x,'y':data.sensitivity_tfa_chart.bit_pressure_chart[i].y/6.894757});
            }
            for(var i=data.sensitivity_flowrate_chart.result.length-1;i>=0;i--){
                sensitivity_flowrate.push({'x':data.sensitivity_flowrate_chart.result[i].x*0.2647,'y':data.sensitivity_flowrate_chart.result[i].y/6.894757});
            }
            // ECD Calculation
            for(var i=data.sensitivity_flowrate_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_flowrate_ecd.push({'x':data.sensitivity_flowrate_chart.ecd_without[i].x*0.2647,'y':data.sensitivity_flowrate_chart.ecd_without[i].y});
            }
            for(var i=data.sensitivity_mudweight_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_mudweight_ecd.push({'x':data.sensitivity_mudweight_chart.ecd_without[i].x*8.345,'y':data.sensitivity_mudweight_chart.ecd_without[i].y});
            }
            for(var i=data.sensitivity_viscocity_chart.ecd_without.length-1;i>=0;i--){
                sensitivity_viscocity_ecd.push({'x':data.sensitivity_viscocity_chart.ecd_without[i].x*1000,'y':data.sensitivity_viscocity_chart.ecd_without[i].y});
            }
            for(var i=data.ropecdchart.ecd_with.length-1;i>=0;i--){
                sensitivity_rop_withecd.push({'x':data.ropecdchart.ecd_with[i].x*3.281,'y':data.ropecdchart.ecd_with[i].y});
            }
            for(var i=data.ropecdchart.ecd_without.length-1;i>=0;i--){
                sensitivity_rop_withoutecd.push({'x':data.ropecdchart.ecd_without[i].x*3.281,'y':data.ropecdchart.ecd_without[i].y});
            }
            // for(var i=data.cuttingsdensityecdchart.ecd_with.length-1;i>=0;i--){
            //     sensitivity_cd_withecd.push({'x':data.cuttingsdensityecdchart.ecd_with[i].x*3.281,'y':data.cuttingsdensityecdchart.ecd_with[i].y});
            // }
            // for(var i=data.cuttingsdensityecdchart.ecd_without.length-1;i>=0;i--){
            //     sensitivity_cd_withoutecd.push({'x':data.cuttingsdensityecdchart.ecd_without[i].x*3.281,'y':data.cuttingsdensityecdchart.ecd_without[i].y});
            // }
        }
        sensitivity_yieldpoint_charts(sensitivity_yieldpoint,pressure,yeildpoint);
        sensitivity_viscocity_charts(sensitivity_viscocity,pressure,viscocity);
        sensitivity_mudweight_charts(sensitivity_mudweight,pressure,mud_weight);
        sensitivity_tfa_charts(sensitivity_tfa,sensitivity_tfa_bit,pressure,tfa);
        sensitivity_flowrate_charts(sensitivity_flowrate,pressure,flowrate);
        flowrateecdcharts(sensitivity_flowrate_ecd,ecd,flowrate);
        mudweightecdcharts(sensitivity_mudweight_ecd,ecd,mud_weight);
        viscocityecdcharts(sensitivity_viscocity_ecd,ecd,viscocity);
        ropecdcharts(sensitivity_rop_withecd,sensitivity_rop_withoutecd,ecd,rop);
        // cuttingsdensityecdcharts(data)
        
    }
    
    
});

function sensitivity_yieldpoint_charts(data,pressure,yeildpoint){
    Highcharts.chart('sensitivity_yieldpoint_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'Yield Point ('+yeildpoint+')'
        },
        tickInterval : 5,

    },
    yAxis: {
        title: {
            text: 'Pressure Loss ('+pressure+')'
        },
        tickInterval : 100,

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
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data,
        dashStyle: 'Solid',
    }
  ]
});
}
function sensitivity_viscocity_charts(data,pressure,viscocity){
    Highcharts.chart('sensitivity_viscocity_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'Plastic Viscocity ('+viscocity+')'
        },
        tickInterval : 5,

    },
    yAxis: {
        labels: {
            format:'{value}'
        },
        title: {
            text: 'Pressure Loss ('+pressure+')'
        },
        tickInterval : 100,

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
        name: 'Total Pressure Loss',
        color: 'rgb(245,173,43)',
        data: data,
        dashStyle: 'Solid',
    }
  ]
});
}
function sensitivity_mudweight_charts(data,pressure,mud_weight){
    mudweight_pressure_chart=Highcharts.chart('sensitivity_mudweight_chart', {
        title: {
            text: 'Pressure Loss'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Mudweight ('+mud_weight+')'
            },
            tickInterval : 0.5,

        },
        yAxis: {
            title: {
                text: 'Pressure Loss ('+pressure+')'
            },
            tickInterval : 100,

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
            name: 'Total Pressure Loss',
            color: 'rgb(245,173,43)',
            data: data,
            dashStyle: 'Solid',
        }
    ]
    });
   
}
function sensitivity_tfa_charts(sensitivity_tfa,sensitivity_tfa_bit,pressure,tfa){
    tfachart=Highcharts.chart('sensitivity_tfa_chart', {
    title: {
        text: 'Pressure Loss'
    },
    credits: {
        enabled: false
       },
    xAxis: {
        title: {
            enabled: true,
            text: 'TFA ('+tfa+')'
        },
        tickInterval : 0.1,

    },
    yAxis: {
        labels: {
            formatter: function () {
                return this.value / 1000;
            }
        },
        title: {
            text: 'Pressure Loss(*1000) ('+pressure+')'
        },
        tickInterval : 100,

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
        name: 'Bit Pressure Loss',
        color: 'rgb(22,96,178)',
        data: sensitivity_tfa_bit,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'Total Pressure Loss',
        color: 'rgb(22,96,178)',
        data: sensitivity_tfa,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function sensitivity_flowrate_charts(data,pressure,flowrate){
    flowrate_pressure_chart=Highcharts.chart('sensitivity_flowrate_chart', {
            title: {
                text: 'Pressure Loss'
            },
            credits: {
                enabled: false
               },
            xAxis: {
                title: {
                    enabled: true,
                    text: 'Flowrate ('+flowrate+')'
                },
                tickInterval : 50,

            },
            yAxis: {
                title: {
                    text: 'Pressure Loss ('+pressure+')'
                },
                tickInterval : 100,
                labels: {
                        format: '{value}'
                    },
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
                name: 'Total Pressure Loss',
                color: 'rgb(245,173,43)',
                data: data,
                dashStyle: 'Solid',
            }
        ]
        });
}
// ECD charts
function flowrateecdcharts(data,ecd,flowrate){
    flowrateecd=Highcharts.chart('flowrate_ecd_chart', {
        title: {
            text: 'ECD'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Flowrate ('+flowrate+')'
            },
            tickInterval : 50,

        },
        yAxis: {
            title: {
                text: 'ECD ('+ecd+')'
            },
            tickInterval : 0.5,

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
            name: 'ECD',
            color: 'rgb(22,96,178)',
            data: data,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },

    ]
    });
}
function mudweightecdcharts(data,ecd,mud_weight){
    mudweightecd_chart=Highcharts.chart('mudweight_ecd_chart', {
        title: {
            text: 'ECD'
        },
        credits: {
            enabled: false
           },
        xAxis: {
            title: {
                enabled: true,
                text: 'Mud Weight ('+mud_weight+')'
            },
            tickInterval : 0.5,
    
        },
        yAxis: {
            title: {
                text: 'ECD ('+ecd+')'
            },
            tickInterval : 0.5,
    
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
            name: 'ECD',
            color: 'rgb(22,96,178)',
            data: data,
            dashStyle: 'Solid',
            marker: {
                enabled: false
            },
        },
    
    ]
    });
    
}
function viscocityecdcharts(data,ecd,viscocity){
    Highcharts.chart('viscocity_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'Plastic Viscocity ('+viscocity+')'
        },
        tickInterval : 5,

    },
    yAxis: {
        title: {
            text:'ECD ('+ecd+')'
        },
        tickInterval : 0.5,

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
        name: 'ECD',
        color: 'rgb(22,96,178)',
        data: data,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
function ropecdcharts(sensitivity_rop_withecd,sensitivity_rop_withoutecd,ecd,rop){
    Highcharts.chart('rop_ecd_chart', {
    title: {
        text: 'ECD'
    },
    credits: {
      enabled: false
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'ROP ('+rop+')'
        },
        tickInterval : 10,
        min:0,
        max:200

    },
    yAxis: {
        title: {
            text: 'ECD ('+ecd+')'
        },
        tickInterval : 0.5,

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
        name: 'ECD(With Cuttings)',
        color: 'rgb(22,96,178)',
        data: sensitivity_rop_withecd,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },
    {
        type: 'spline',
        name: 'ECD(Without Cuttings)',
        color: 'rgb(22,96,178)',
        data: sensitivity_rop_withoutecd,
        dashStyle: 'Solid',
        marker: {
            enabled: false
        },
    },

  ]
});
}
// function cuttingsdensityecdcharts(data){
//     Highcharts.chart('cuttingsdensity_ecd_chart', {
//     title: {
//         text: 'ECD'
//     },
//     credits: {
//       enabled: false
//     },
//     xAxis: {
//         title: {
//             enabled: true,
//             text: 'Cuttings Density'
//         },
//         tickInterval : 0.5,
//         min:19,
//         max:25

//     },
//     yAxis: {
//         title: {
//             text: 'ECD'
//         },
//         tickInterval : 0.5,

//     },

//     plotOptions: {
//         spline: {
//             marker: {
//                 enabled: false
//             }
//         }
//     },
    
//     series: [
//     {
//         type: 'spline',
//         name: 'ECD(With Cuttings)',
//         color: 'rgb(22,96,178)',
//         data: data.ecd_with,
//         dashStyle: 'Solid',
//         marker: {
//             enabled: false
//         },
//     },
//     {
//         type: 'spline',
//         name: 'ECD(Without Cuttings)',
//         color: 'rgb(22,96,178)',
//         data: data.ecd_without,
//         dashStyle: 'Solid',
//         marker: {
//             enabled: false
//         },
//     },

//   ]
// });
// }