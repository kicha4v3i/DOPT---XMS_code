$(document).ready(function() {
    $("#welltrajectorytableRow2").validate({
        rules: {
          measured_depth:"required",
          inclination:"required",
          azimuth:"required",
          true_vertical_depth:"required",
          dls:"required",
          
        },
        messages: {
          measured_depth:"Please enter the Measured Depth",
          inclination:"please select the  Inclination",
          azimuth:"Please enter the Azimuth",
          true_vertical_depth:"Please enter the True Vertical Depth",
          dls:"Please enter the Dls",
         
        }
    });
    $(document).on("blur", ".azimuth" , function(){ 
      var current_index=$(this).closest('tr').index();
      prev_mds=[]
      prev_azimuths=[]
      prev_inclinations=[]
      md=[]
      azi=[]
      inc=[]
      $('#welltrajectoryaddtable tbody tr').each(function (index){
        if (index <= current_index) {
            prev_mds.push($(this).find(".measured_depth").val());
            prev_azimuths.push($(this).find(".azimuth").val());
            prev_inclinations.push($(this).find(".inclination").val());
        }
        else{
            return false;
        }
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
          'prev_mds':md,
          'prev_azimuths':azi,
          'prev_inclinations':inc,
          'csrfmiddlewaretoken':csrf,
          'well_id':well_id
        },
        success: function(data) { 
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.true_vertical_depth').val(data.tvd.toFixed(2));
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.converteddls').val(data.converteddls.toFixed(5));
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.dls').val(data.dls.toFixed(5));
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.east').val(data.e.toFixed(2));
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.north').val(data.n.toFixed(2));
         $('#welltrajectoryaddtable tbody tr:eq('+current_index+')').find('.vertical_section').val(data.vs.toFixed(2));
        // dynamicplanviewchart(data.chartdata)
        // dynamicelevationchart(data.chartdata_tvd_vs)
        }
    });
  });
})