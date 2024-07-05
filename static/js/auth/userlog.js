
$(document).ready(function () { 
  var userlog_table=$('.userlog_table').DataTable({ 
      serverSide: true,
      
      ajax: {
      
        url: "/userlog/getuserlog",
        data: function (d) { 
          d.activity = activity; 
          d.well_id = well_id; 
          d.user_id = user_id; 
          d.start_date = $('#startdate').val(); 
          d.end_date = $('#enddate').val(); 
        },
        type: 'GET',
      },
      language: {
        emptyTable: "---"
      },
      columns: [
        { data: 'user_name' },
        { data: 'name' },
        { data: 'message' },
        { data: 'time' },
        
      ],
    });
    flatpickr(".filter_dates", {
      enableTime: true,
      dateFormat: "Y-m-d H:i",
    });

    $('#submit_search').click(function() {
      userlog_table.ajax.reload(); 
    });



    

     


});



  