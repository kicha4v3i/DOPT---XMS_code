$(function() {
    var chart_type
    var rheogram_model
    var section_model
    var chart
    var min_rpm_index
    var minimumrmsmodal
    var indirectchart
    $(document).on("click",".nav-link" , function() { 
        $('#rheogram_allmodels_show').text("Display All Models");
        var section_name=$(this).attr('data-id');
        var series1=[]
        var series2=[]
        var rpm=[]
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
              // alert(section_model)
              rheogram_model=data.rheogram_model
              $('.plastic_viscocity').html(data.modalparameters.plastic_viscocity.toFixed(2)+display_plastic_viscosity)
              $('.yield_point').html(data.modalparameters.yield_point.toFixed(2)+ display_gelstrengthunit)
              $('.n_value').html(data.modalparameters.n)
              if (data.modalparameters.K !== undefined) {
                  $('.k_value').html(data.modalparameters.K+' lbf.sec^n/100ft2')
              } else {
                  $('.k_value').html("")
              }
              if (data.modalparameters.Ty !== undefined) {
                $('.ty_value').html(data.modalparameters.Ty + display_gelstrengthunit);
              } else {
                  $('.ty_value').html(""); 
              }
              $('.model-all').show()
              if(data.modalparameters.Ty<0){
                $("input[type=radio][value='4']").prop("disabled",true);
              }
    
              if(data.charttype=='direct'){
                rheogramchart(data,section_name,section_model)
                createSVGFromChart(chart,'rheogramchart_canvas','rheogramchart-'+wellphase_id+'-'+section_name);

              }else{
                indirectrheogramchart(data,section_name)
                createSVGFromChart(indirectchart,'rheogramchart_canvas','rheogramchart-'+wellphase_id+'-'+section_name);

              }
            }  
        });
    })

    $('.section_name').click(function(){
        var selected_model=$(this).val();
        var section_name=$(this).attr('data-id');
        $.ajax({ 
          type: "GET",                      
          url: "/wells/muddata/modelselected",                    
          data: {
            wellphase_id:wellphase_id,
            selected_model:selected_model,
            section_name:section_name
          },
          dataType: "json",
          success: function (data) { 
            if(selected_model == '1'){
              $('#newtonian_model').show();
              $('#bingham_model').hide();
              $('#powerlaw_model').hide();
              $('#hershel_model').hide();
              bingha.update({visible: false});
              newtonion.update({visible: true});
              powerlaw.update({visible: false});
              hershel.update({visible: false});
              shearstress.update({visible:false})
            }else if(selected_model == '2'){
              $('#newtonian_model').hide();
              $('#bingham_model').show();
              $('#powerlaw_model').hide();
              $('#hershel_model').hide();
              newtonion.update({visible: false});
              bingha.update({visible: true});
              powerlaw.update({visible: false});
              hershel.update({visible: false});
              shearstress.update({visible:false})
            }else if(selected_model == '3'){
              $('#newtonian_model').hide();
              $('#bingham_model').hide();
              $('#powerlaw_model').show();
              $('#hershel_model').hide();
              newtonion.update({visible: false});
              bingha.update({visible: false});
              powerlaw.update({visible: true});
              hershel.update({visible: false});
              shearstress.update({visible:false})
            }else if(selected_model == '4'){
              $('#newtonian_model').hide();
              $('#bingham_model').hide();
              $('#powerlaw_model').hide();
              $('#hershel_model').show();
              newtonion.update({visible: false});
              bingha.update({visible: false});
              powerlaw.update({visible: false});
              hershel.update({visible: true});
              shearstress.update({visible:false})
            }
          }
        });
    })

    $('#rheogram_allmodels_show').click(function () {
        $('#hershel_model').hide();
        $('#powerlaw_model').hide();
        $('#bingham_model').hide();
        $('#newtonian_model').hide();
        if(chart_type=="indirect"){
          if($(this).text()=="Display All Models"){
            $('#hershel_model').show();
            $('#powerlaw_model').show();
            $('#bingham_model').show();
            $('#newtonian_model').show();
            
          indirectchart.series[0].update({visible: true})
          indirectchart.series[1].update({visible: true})
          indirectchart.series[2].update({visible: true})
          indirectchart.series[3].update({visible: true})
          }else{
            if(rheogram_model=="1"){
              $('#newtonian_model').show();
            }
            else if(rheogram_model=="2"){
              $('#bingham_model').show();
            }
            else if(rheogram_model=="3"){
              $('#powerlaw_model').show();
            }
            else{
              $('#hershel_model').show();
            }
            var selected_model=rheogram_model-1
            for(var i=0;i<=3;i++){
              if(selected_model==i){
                indirectchart.series[i].update({visible: true})
              }
              else{
                indirectchart.series[i].update({visible: false})
              }
            }
          }
        }else{
          if($(this).text()=="Display All Models"){
            // alert("dgf")
            $('#hershel_model').show();
            $('#powerlaw_model').show();
            $('#bingham_model').show();
            $('#newtonian_model').show();
          chart.series[0].update({visible: true})
          chart.series[1].update({visible: true})
          chart.series[2].update({visible: true})
          chart.series[3].update({visible: true})
          chart.series[4].update({visible: true})
          }
          else{
            $('#hershel_model').show();
            $('#powerlaw_model').hide();
            $('#bingham_model').hide();
            $('#newtonian_model').hide();
            // alert(min_rpm_index)
           for(var i=0;i<=4;i++){
            // selected=rheogramchart(data,section_name,section_model)
             if(i==section_model){
              chart.series[0].update({visible:false})
              chart.series[i].update({visible: true})
              if(i==1){
                $('#hershel_model').hide();
                $('#powerlaw_model').hide();
                $('#bingham_model').hide();
                $('#newtonian_model').show();
              }else if(i==2){
                $('#hershel_model').hide();
                $('#powerlaw_model').hide();
                $('#bingham_model').show();
                $('#newtonian_model').hide();
              }else if(i==3){
                $('#hershel_model').hide();
                $('#powerlaw_model').show();
                $('#bingham_model').hide();
                $('#newtonian_model').hide();
              }else if(i==4){
                $('#hershel_model').show();
                $('#powerlaw_model').hide();
                $('#bingham_model').hide();
                $('#newtonian_model').hide();
              }
              // chart.legend.allItems[i].update({name:'<b style="font-size:15px;">'+minimumrmsmodal+'(Best Fit)</b>',rgb:'245,173,43'});
             }
             else if(i==min_rpm_index){
              chart.series[i].update({visible: true})
             }else{
               if(i!=0){
                 chart.series[i].update({visible: false}) 
                }else{
                chart.series[i].update({visible: true}) 
               }
             }
           }
          }
        } 
        $(this).text($(this).text() == "Display All Models" ? "Hide All Models" : "Display All Models");
      
      });

    function rheogramchart(data,containerid,section_model){
        // alert(section_model)
        minimumrmsmodal=data.minimumrmsmodal
        var lastrpm=data.last_rpm
        chart = Highcharts.chart(containerid+'-rheogramchart', {
          chart: {
              //type: 'spline',
              // zoomType: 'xy'
              backgroundColor: 'transparent',
              reflow: false,
              
      
          },
          credits: {
                enabled: false
              },
          title: {
              text: ''
          },
          // subtitle: {
          //     text: 'Source: Heinz  2003'
          // },
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
      function (chart){
        var shearstress = chart.series[0];
        var newtonion = chart.series[1];
        var bingha = chart.series[2];
        var powerlaw = chart.series[3];
        var hershel = chart.series[4];
        // console.log(hershel);
        // var min_rpm_index
        // console.log(hershel);
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
          chart.series[min_rpm_index].update({name:'<b style="font-size:15px;">'+minimumrmsmodal+'(Best Fit)</b>',rgb:'245,173,43'});
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
        console.log(data.low_shear_rate)
        var minimumrmsmodal=data.minimumrmsmodal
        var lastrpm=data.last_rpm
        rheogram_model=data.rheogram_model
        indirectchart = Highcharts.chart(containerid+'-rheogramchart', {
          chart: {
              //type: 'spline',
              // zoomType: 'xy'
          },
          title: {
              text: 'Shear Rate(dial) Line Fit Plot'
          },
          // subtitle: {
          //     text: 'Source: Heinz  2003'
          // },
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
              // layout: 'vertical',
              // align: 'left',
              // verticalAlign: 'top',
              // x: 100,
              // y: 70,
              // floating: true,
              // backgroundColor: Highcharts.defaultOptions.chart.backgroundColor,
              // borderWidth: 1
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
        if(!data.low_shear_rate){
            var lastSeriesIndex = chart.series.length - 1;
            chart.series[lastSeriesIndex].remove();
        }


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
        // $('#rheogram_allmodels_show').click(function () {
        // newtonion.update({visible: true});
        // bingha.update({visible: true});
        // powerlaw.update({visible: true});
        // hershel.update({visible: true});
        // });
      
      }
      );
      
      
      }
      

})