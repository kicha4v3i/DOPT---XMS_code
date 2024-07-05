$(document).ready(function() {
    chartdata=[]
    chartdata_tvd_vs=[]
    // $("#welltrajectoryform").validate({
    //     rules: {
    //       measured_depth:"required",
    //       inclination:"required",
    //       azimuth:"required",
    //       true_vertical_depth:"required",
    //       dls:"required",
          
    //     },
    //     messages: {
    //       measured_depth:"Please enter the Measured Depth",
    //       inclination:"please select the  Inclination",
    //       azimuth:"Please enter the Azimuth",
    //       true_vertical_depth:"Please enter the True Vertical Depth",
    //       dls:"Please enter the Dls",
         
    //     }
    // });
        
 
    $(document).on("blur", ".azimuth" , function(){ 
        var current_azimuth = $(this).val()
        var cloesttr_index=$(this).closest('tr').index()-1;
        var current_index=$(this).closest('tr').index();
        var prev_inclination = $(this).closest("tr").prev().find(".inclination").val();
        var prev_azimuth = $(this).closest("tr").prev().find(".azimuth").val();
        var current_inclination = $(this).closest("tr").find(".inclination").val();
        var tvd=$(this).closest("tr").prev().find(".true_vertical_depth").val();
        var current_md=$(this).closest("tr").find(".measured_depth").val();
        var prev_md = $(this).closest("tr").prev().find(".measured_depth").val();
        var prev_east = $(this).closest("tr").prev().find(".east").val();
        var prev_north = $(this).closest("tr").prev().find(".north").val();
        var surface_easting = $('#surface_easting').val();
        var surface_northing = $("#surface_northing").val();
        var current_element=$(this);
        chartdata[0]={'x':0.00 ,'y':0.00}
        chartdata_tvd_vs[0]={'x':0 ,'y':0.00}
        prev_mds=[]
        prev_azimuths=[]
        prev_inclinations=[]
        md=[]
        azi=[]
        inc=[]
        $('#welltrajectoryaddtable tbody tr').each(function (){
        prev_mds.push($(this).find(".measured_depth").val());
        prev_azimuths.push($(this).find(".azimuth").val());
        prev_inclinations.push($(this).find(".inclination").val());
        }); 
        for (let i = 0; i < prev_mds.length; i++) {
        if(prev_mds[i]!='' && prev_mds[i]!= null){
            md.push(prev_mds[i]) 
            azi.push(prev_azimuths[i])
            inc.push(prev_inclinations[i])
        }
        } 
        var csrf=$("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            type: "POST",
            url:"/wells/welltrajectory/welltrajectorytvdcal",
            data: {
                // current_azimuth : current_azimuth,
                // prev_inclination : prev_inclination,
                // prev_azimuth : prev_azimuth,
                // current_inclination :  current_inclination,
                // tvd:tvd,
                // current_md:current_md,
                // prev_md:prev_md,
                // prev_east:prev_east,
                // prev_north:prev_north,
                // surface_easting:surface_easting,
                // surface_northing:surface_northing,
                'prev_mds':md,
                'prev_azimuths':azi,
                'prev_inclinations':inc,
                'csrfmiddlewaretoken':csrf,
                'well_id':well_id
            },
            success: function(data) { 
            console.log(data);
            
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.true_vertical_depth').val(data.tvd.toFixed(2));
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.converteddls').val(data.converteddls.toFixed(5));
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.dls').val(data.converteddls.toFixed(5));
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.east').val(data.e.toFixed(2));
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.north').val(data.n.toFixed(2));
            $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.vertical_section').val(data.vs.toFixed(2));

            dynamicplanviewchart(data.chartdata)
            dynamicelevationchart(data.chartdata_tvd_vs)
            }
        });
    });
   
})
function dynamicplanviewchart(data){
    Highcharts.chart('dynamic-welltractory-container', {  
      credits: {
        enabled: false
        },
        title: {
          text: ''
      },
        chart: {
          inverted: false,
      //    marginTop: 25
      },
      yAxis: {
        reversed: false,
        opposite: false,
        labels: {
          formatter: function () {
              return (this.value > 0 ? ' ' : '') + this.value ;
          }
      },
    //    align: 'top',
          title: {
              text: 'North(mN)'
          }    
      },
      xAxis: {
        categories: [],
        opposite : true,
        tickInterval : 1000 ,
        title: {
              text: 'East(mE)'
      },
   //     align: 'top',
          accessibility : {
              rangeDescription: ''
          }
      }, 
      title: {
              text: 'Plan View'
      },  
      legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'middle'
      },
      colors: [
      '#4572A7', 
      '#DB843D'
      ],
      plotOptions: {
          series: {
              label: [],                
          }
      }, 
      series: [{
          name: '',
          data: data,
          tooltip: {
              valueSuffix: '(mN)'
          },
      }]
  });
  }
  function dynamicelevationchart(data){

    Highcharts.chart('dynamic-welltractory-tvd-vs', {  
      
      credits: {
        enabled: false
        },
        title: {
          text: ''
      },
        chart: {
          inverted: false,
      //    marginTop: 25
      },
      yAxis: {
        reversed: true,
        opposite: false,
        labels: {
          formatter: function () {
              return (this.value > 0 ? ' ' : '') + this.value ;
          }
      },
        tickInterval : 2000, 
    //    align: 'top',
          title: {
              text: 'TVD'+unit,
          }   
           
      },
      
      xAxis: {
        categories: [],
        opposite : true,
        tickInterval : 1000, 
        title: {
              text: 'Vertical Section'+unit,
      },  
   //     align: 'top',
          accessibility : {
              rangeDescription: 'Elevation View'
          }
      }, 
         title: {
              text: 'Elevation View'
      }, 
      legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'middle'
      },
      colors: [
      '#4572A7', 
      '#DB843D'
      ],
      plotOptions: {
          series: {
              label: [] ,                
          }
      },
      series: [{
          name: '',
          data: data,
          tooltip: {
              valueSuffix: unit
          },
      }]
  });
  }
