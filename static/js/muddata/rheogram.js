$(function() {
    $('.modal-tables').hide()
    var directchart
    $(document).on("keyup", ".dial" , function() {
        
        var closesttable=$(this).closest('table').attr('id');
        var tabletype = closesttable.split("-")[0];
        var dial=[];
        var rpm=[];

        if(tabletype=="rheogram"){
            var section_name=$(this).closest('table').attr('data-id')
            $('#'+closesttable+ " .dial").each(function(){
                var closestrpm=$(this).closest('td').prev('td').find('.rpm').val();
                if($(this).val()!=''){
                rpm.push(closestrpm);
                dial.push($(this).val())
                }
            })
            $.ajax({
                type: "GET",
                url:"/wells/muddata/getdirectchart",
                data:{
                    wellphase_id:wellphase_id,
                    rpm:rpm,
                    dial:dial,
                    section_name:section_name,
                    well_id:well_id
                },
                success: function(data) {
                    console.log(data)
                    dynamicdirectchart(data,section_name)
                }
            });
        }
    });

    $(document).on("click",".nav-link" , function() { 
        $(".modalselect").change(function () {
            var selected_model = $(this).val();
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
                $(".modalselect").val(selected_model);
        
            }
            });
        })
    })

    $(document).on("click", ".modalselect" , function() {
        var selectedmodal=$(this).val();
        var tabindex=$(this).attr('tab-index')
        if(selectedmodal==1){
          $('#bingham-table'+tabindex).hide();
          $('#powerlaw-table'+tabindex).hide();
          $('#hershel-table'+tabindex).hide();
          $('#newtonian-table'+tabindex).show();
          rheogram_model_data(tabindex,"newtonian","#1660B2",'shortdot',"Newtonian Fluid")
        }else if(selectedmodal==2){
          $('#newtonian-table'+tabindex).hide();
          $('#powerlaw-table'+tabindex).hide();
          $('#bingham-table'+tabindex).show();
          $('#hershel-table'+tabindex).hide();
          rheogram_model_data(tabindex,"bingham","#2CB68B",'shortdot','Bingham Plastic')
        }else if(selectedmodal==3){
          $('#newtonian-table'+tabindex).hide();
          $('#bingham-table'+tabindex).hide();
          $('#hershel-table'+tabindex).hide();
          $('#powerlaw-table'+tabindex).show();
          rheogram_model_data(tabindex,"powerlaw","#298f8a","Solid",'Powerlaw')
        }else if(selectedmodal==4){
          $('#newtonian-table'+tabindex).hide();
          $('#bingham-table'+tabindex).hide();
          $('#powerlaw-table'+tabindex).hide();
          $('#hershel-table'+tabindex).show();
          rheogram_model_data(tabindex,"hershel","#F5AD2B","Solid",'Hershel Bulkley')
        } 
    })

    function rheogram_model_data(tabindex,modal,color,dashstyle,showname){
        var section_name=$('.modalselect').attr('data-id');
        var wellphase_id=$('.modalselect').attr('wellphase-id');
        var well_id=$('#well').val();
          $.ajax({
            type: "GET",
            data:{
              section_name:section_name,
              wellphase_id:wellphase_id,
              modal:modal,
              well_id:well_id
            },
            url:"/wells/muddata/calculatedial",
            success: function(data) {
              seperate_rheogramchart(data.new_dial,tabindex,modal,color,dashstyle,showname)
              
            }
          })
    }

    function seperate_rheogramchart(data,tabindex,modal,color,dashstyle,showname){
        var chart = Highcharts.chart('seperate_rheogramchart'+tabindex+'', {
          chart: {
              //type: 'spline',
              // zoomType: 'xy'
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
              name: showname,
              color: color,
              data: data,
              dashStyle: dashstyle
          },
        ]
        });
      
      }

    function dynamicdirectchart(data,containerid){
        directchart = Highcharts.chart(containerid+'-dynamicdirectchart', {
          chart: {
              //type: 'spline',
              // zoomType: 'xy'
              reflow: false,
  
          },
          title: {
              text: 'Shear Rate(dial) Line Fit Plot'
          },
          credits: {
            enabled: false
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
              type:'scatter',
              name: 'Shear Stress(dial)',
              color: '#0000ff',
              data: data.userdial,
              dashStyle: 'LongDashDot'
          }, 
          {
              type: 'spline',
              name: 'Newtonian',
              color: 'rgb(22,96,178)',
              data: data.newtoniondial,
              dashStyle: 'Solid',
          },
          {
              type: 'spline',
              name: 'Bingham Plastic',
              color: '#2CB68B',
              data: data.binghammodal,
              dashStyle: 'Solid',
          },
          {
              type: 'spline',
              name: 'Powerlaw',
              color: '#298f8a',
              data: data.powerlawmodal,
              dashStyle: 'Solid',
          },
          {
              type: 'spline',
              name: '<b style="color:green">hershel</b>',
              color: 'rgb(245,173,43)',
              data: data.hershelmodal,
              dashStyle: 'Solid',
              
        }
        ]
      });
    }

})