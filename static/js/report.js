$(document).ready( function(){
    // alert("ggg")
    var section_name = $('ul.custom_active_list').find('li.active').attr('data-id');
    var wellphase_id=$('ul.custom_active_list').find('li.active').attr('wellphase_id');
    $.ajax({
        type: "GET",
        url:"/wells/muddata/getrheogrammodals",
        data:{
          wellphase_id:wellphase_id,
          section_name:section_name,
          well_id:well_id
        },
        success: function(data) {
        chart_type=data.charttype
          section_model = data.section_model
          rheogram_model=data.rheogram_model
          $('.plastic_viscocity').html(data.modalparameters.plastic_viscocity.toFixed(2)+' {%display_plastic_viscosity request.session.unit%}')
          $('.yield_point').html(data.modalparameters.yield_point.toFixed(2)+ ' {%display_gelstrengthunit request.session.unit%}')
          $('.k_value').html(data.modalparameters.K+' lbf.sec^n/100ft2')
          $('.n_value').html(data.modalparameters.n)
          $('.ty_value').html(data.modalparameters.Ty+' {%display_gelstrengthunit request.session.unit%}')
          $('.model-all').show()
          if(data.modalparameters.Ty<0){
            $("input[type=radio][value='4']").prop("disabled",true);
          }

          if(data.charttype=='direct'){
          rheogramchart(data,section_name,section_model)
          }else{
            indirectrheogramchart(data,section_name)
          }
      }

        
      });
})

function rheogramchart(data,containerid,section_model){
    minimumrmsmodal=data.minimumrmsmodal
    rheology_chart = Highcharts.chart('directchart_rheology', {
      chart: {
          backgroundColor: 'transparent',
          reflow: false,
      },
      credits: {
            enabled: false
          },
      title: {
          text: ''
      },
      xAxis: {
          title: {
              enabled: true,
              text: 'RPM'
          },
          tickInterval : 100 ,
  
      },
      yAxis: {
          title: {
              text: 'Dial'
          },
          tickInterval : 20,
  
      },
      legend: {
          visible: false
          
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
        showInLegend: false,
          type:'scatter',
          name: 'Shear Stress(dial)',
          color: '#0000ff',
          data: data.userdial,
          dashStyle: 'LongDashDot'
  
  
      }, 
      {
        showInLegend: false,
          type: 'spline',
          name: 'Newtonian',
          color: 'rgb(22,96,178)',
          data: data.newtoniondial.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
        showInLegend: false,
          type: 'spline',
          name: 'Bingham Plastic',
          color: '#2CB68B',
          data: data.binghammodal.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
        showInLegend: false,
          type: 'spline',
          name: 'Powerlaw',
          color: '#298f8a',
          data: data.powerlawmodal.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
        showInLegend: false,
          type: 'spline',
          name: 'Hershel Bulkley',
          color: 'rgb(245,173,43)',
          data: data.hershelmodal.modal,
          dashStyle: 'Solid',
          visible: false
          
    }
    ]
  },
  function (rheology_chart){
    var shearstress = rheology_chart.series[0];
    var newtonion = rheology_chart.series[1];
    var bingha = rheology_chart.series[2];
    var powerlaw = rheology_chart.series[3];
    var hershel = rheology_chart.series[4];
    if(section_model==null){
      if(minimumrmsmodal=='Hershel Bulkley')
      {
        min_rpm_index=4;
        hershel.update({visible: true});
        $('#hershel_model').show();
      }else if(minimumrmsmodal=='Powerlaw'){
        min_rpm_index=3;
        powerlaw.update({visible: true});
        $('#powerlaw_model').show();
      }else if(minimumrmsmodal=='Bingham Plastic'){
        min_rpm_index=2;
        bingha.update({visible: true});
        $('#bingham_model').show();
      }else if(minimumrmsmodal=='Newtonian Fluid'){
        min_rpm_index=1;
        newtonion.update({visible: true});
        $('#newtonian_model').show();
      } 
      rheology_chart.series[min_rpm_index].update({name:'<b style="font-size:15px;">'+minimumrmsmodal+'(Best Fit)</b>',rgb:'245,173,43'});
    }
    else if(section_model=='1'){
      shearstress.update({visible:false});
      newtonion.update({visible: true});
      $('#newtonian_model').show();
      $('#bingham_model').hide();
      $('#powerlaw_model').hide();
      $('#hershel_model').hide();
    }
    else if(section_model=='2'){
      shearstress.update({visible:false});
      bingha.update({visible: true});
      $('#newtonian_model').hide();
      $('#bingham_model').show();
      $('#powerlaw_model').hide();
      $('#hershel_model').hide();
    }
    else if(section_model=='3'){
      shearstress.update({visible:false});
      powerlaw.update({visible: true});
      $('#newtonian_model').hide();
      $('#bingham_model').hide();
      $('#powerlaw_model').show();
      $('#hershel_model').hide();
    }
    else if(section_model=='4'){
      shearstress.update({visible:false});
      hershel.update({visible: true});
      $('#newtonian_model').hide();
      $('#bingham_model').hide();
      $('#powerlaw_model').hide();
      $('#hershel_model').show();
    }


  });

}
function indirectrheogramchart(data,containerid){
    var minimumrmsmodal=data.minimumrmsmodal
    var lastrpm=data.last_rpm
    rheogram_model=data.rheogram_model
    // alert(rheogram_model)
    rheology_chart = Highcharts.chart('directchart_rheology', {
      chart: {

      },
      title: {
          text: 'Shear Rate(dial) Line Fit Plot'
      },
      xAxis: {
          title: {
              enabled: true,
              text: 'RPM'
          },
          tickInterval : 100 ,
  
      },
      yAxis: {
          title: {
              text: 'Dial'
          },
          tickInterval : 20,
  
      },
      legend: {
          visible: false
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
          name: 'Newtonian',
          color: 'rgb(22,96,178)',
          data: data.newtoniondial.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
          type: 'spline',
          name: 'Bingham Plastic',
          color: '#2CB68B',
          data: data.binghammodal.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
          type: 'spline',
          name: 'Powerlaw',
          color: '#298f8a',
          data: data.powerlawmodal.modal,
          dashStyle: 'Solid',
          visible: false
      },
      {
          type: 'spline',
          name: 'Hershel Bulkley',
          color: 'rgb(245,173,43)',
          data: data.hershelmodal.modal,
          dashStyle: 'Solid',
          visible: false
    }
    ]
  },
  function (chart){
    var newtonion = chart.series[0];
    var bingha = chart.series[1];
    var powerlaw = chart.series[2];
    var hershel = chart.series[3];
    if(rheogram_model == '1'){
      newtonion.update({visible: true});
      $('#newtonian_model').show();
    }
    else if(rheogram_model == '2'){
      bingha.update({visible: true});
      $('#bingham_model').show();
    }
    else if(rheogram_model == '3'){
      powerlaw.update({visible: true});
      $('#powerlaw_model').show();
    }
    else if(rheogram_model == '4'){
      hershel.update({visible: true});
      $('#hershel_model').show();
    }
    chart.redraw();
  }
  );
  }

function pressure_chart_pdf(chartdata,previous_measured_depth,last_data){
    pressure_chart = Highcharts.chart('pressureloss_charts', {
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
                text: 'Pressure Loss (psi)'
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
                text: 'MD (ft)'
            },
            labels: {
                format: '{value}'
            },
            tickInterval : 1000,

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
            type:'spline',
            name:'Casing',
            color:'black',
            data:[{
                x:-30,
                y: previous_measured_depth,
                
            },{
                x:last_data,
                y:previous_measured_depth,
            }],
            marker: {
                enabled: false,
            },
            dashStyle: 'dot',
            label: {
                    connectorAllowed: true,
                    enabled:true
            }
        }
      ]
    });

}

function ecdalonghole_chart_pdf(ecdalongwelldata,previous_measured_depth,mudweight,todepth,ecd_alonghole_max,ecdalongwellincreased,ecd_fracturepressure){
    ecdalong_chart = Highcharts.chart('ecdalonghole_chart_pdf', {
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
            // tickAmount: 6,
            gridLineWidth:1,
            title: {
                enabled: true,
                text: 'ECD{ppg}'
            },
            tickInterval : 0.20,
            min:mudweight-0.5,
            max:ecd_alonghole_max+1

        },
        yAxis: {
            reversed: true,
            opposite: false,
            title: {
                text: 'MD(ft)'
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
            type:'spline',
            name:'Casing',
            color:'black',
            data:[{
                x:-30,
                y: previous_measured_depth,
                
            },{
                x:ecd_alonghole_max+1,
                y:previous_measured_depth,
            }],
            marker: {
                enabled: false,
            },
            dashStyle: 'dot',
            label: {
                    connectorAllowed: true,
                    enabled:true
            }
        }
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
}

function ecdbitchart_pdf(ecdchartdata,previous_measured_depth,mudweight,todepth,ecd_chart_max,increasedecdchartdata,ecd_fracturepressure){
    var categories=[]
    for(var i=0;i<ecdchartdata.length;i++){
        categories.push(ecdchartdata[i]['x'].toFixed(2))
    }
    ecdbit_chart = Highcharts.chart('ecdbitchart_pdf', {
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
                text: 'ECD (ppg)'
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
                text: 'MD(ft)'
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
            type:'spline',
            name:'Casing',
            color:'black',
            data:[{
                x:-30,
                y: previous_measured_depth,
                
            },{
                x:ecd_chart_max+1,
                y:previous_measured_depth,
            }],
            marker: {
                enabled: false,
            },
            dashStyle: 'dot',
            label: {
                    connectorAllowed: true,
                    enabled:true
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
function ccichart_pdf(ccichartdata,maxcci){
    cci_chart = Highcharts.chart('ccichart_pdf', {
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
                text: 'MD (ft)',
                enabled: true,

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
function transportratiochart_pdf(transportratiochartdata){
    tr_chart = Highcharts.chart('transportratiochart_pdf', {
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
                text: 'MD (ft)',
                enabled: true,

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