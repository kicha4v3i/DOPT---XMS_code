$(document).ready(function () {
  var selectedValues = [];
  var dashboard_table_1;
  var dashboard_table_2;
  var filter = "projects";
  var search = ""
  $('.well_dashboardtable').hide();

  initialize_projectDataTable(selectedValues,search);

  $('.apply_dropdown').on('click', function () {

    selectedValues = []
      $('.country-checkbox:checked').each(function() {
        selectedValues.push($(this).val());
      });
      

      $.ajax({
        url: '',
        method: 'POST',
        headers: { "X-CSRFToken": csrf_token },
        data: {
          selectedValues: selectedValues,
        },
        traditional: true,
        success: function (data) {
 
          var projectCountryHtml = '';  
          
          for (var i = 0; i < data.country_list.length; i++) {
            var projectCountry = data.country_list[i];
          
            
            var projectHtml = `
              <div class="item append-item">
                <div class="card summary_card cards_list_dashboard append-cards" data-id=${projectCountry.country_id} data-name=${projectCountry.country_name}>
                  <div class="location"><i class="ficon feather icon-map-pin"></i> ${projectCountry.country_name}</div>
                  <div class="row">
                    <div class="col-4">
                      <div class="count">${projectCountry.project_count}</div>
                      <div class="title">Projects</div>
                    </div>
                    <div class="col-4">
                      <div class="count">${projectCountry.block_count}</div>
                      <div class="title">Blocks</div>
                    </div>
                    <div class="col-4">
                      <div class="count">${projectCountry.wells_count}</div>
                      <div class="title">Wells</div>
                    </div>
                  </div>
                </div>
              </div>
            `;
            
            projectCountryHtml += projectHtml; 
          }
          
          // Append the accumulated projectCountryHtml to the existing content of dashboard_card
          $('#dashboard_card').html('<div class="project-country owl-carousel owl-theme">' + projectCountryHtml + '</div>');
      
          // Initialize Owl Carousel
          $('.project-country.owl-carousel').owlCarousel({
            // Your Owl Carousel configuration options here
          });
        },
      });
      
      
    if(filter === "wells"){
      if (dashboard_table_1) {
        dashboard_table_1.destroy();
      }
      initialize_wellDataTable(selectedValues,search);
    }
    else{
      if (dashboard_table_2) {
        dashboard_table_2.destroy();
      }
      initialize_projectDataTable(selectedValues,search);
    }
    var downloadLink = $('.download-link');
    downloadLink.attr('data-selected-values', selectedValues);
    downloadLink.attr('data-filter', filter);
    downloadLink.attr('data-search', search);

    // Update the href attribute with the new values
    var newHref = downloadLink.attr('href').split('?')[0] + '?selected_values=' + selectedValues + '&filter=' + filter + '&search=' + search;
    downloadLink.attr('href', newHref);

  });

  $('.select_filter').on('change', function () {
    filter = $(this).val();
    if (filter === "wells") {

      $('.project_dashboardtable').css('display', 'none');
      $('.well_dashboardtable').show();
      $('#DataTables_Table_1_wrapper').css('display', 'block');
      $('#DataTables_Table_0_wrapper').css('display', 'none');
      if(dashboard_table_1){
        dashboard_table_1.destroy();
      }
      initialize_wellDataTable(selectedValues,search);
    }
    if (filter === "projects") {
      $('.well_dashboardtable').hide();
      $('.project_dashboardtable').show();
      $('#DataTables_Table_0_wrapper').css('display', 'block');
      $('#DataTables_Table_1_wrapper').css('display', 'none');
      if (dashboard_table_2) {
        dashboard_table_2.destroy();
      }
      initialize_projectDataTable(selectedValues,search);
    }
    var downloadLink = $('.download-link');
    downloadLink.attr('data-selected-values', selectedValues);
    downloadLink.attr('data-filter', filter);
    downloadLink.attr('data-search', search);
    var newHref = downloadLink.attr('href').split('?')[0] + '?selected_values=' + selectedValues + '&filter=' + filter + '&search=' + search;
    downloadLink.attr('href', newHref);
  });

  function initialize_wellDataTable(selectedValues,search_value) {
    dashboard_table_1 = $('.well_dashboardtable').DataTable({
      serverSide: true,
      searching: false,
      lengthChange: false,
      responsive: true,
      language: {
        emptyTable: "---", 
    },
    drawCallback: function(settings) {
      if (dashboard_table_1.rows().count() === 0) {
          $('.dataTables_paginate, .dataTables_info').hide();
      } else {
          $('.dataTables_paginate, .dataTables_info').show();
      }
  },
      ajax: {
        url: "getwelldatas",
        data: {
          selected_values: selectedValues.join(","),
          filter_type: "wells",
          search_value:search_value
        },
        method: 'GET',
      },
      columns: [
        {data: null , 
          render: function(data){
            return '<p class="well-name-class">'+data.well_name+'</p>'
          }},
          {data: null , 
            render: function(data){
              if(data.well_type[0] == 'P'){
                return '<div class="well-name-ty"><p class="well-ptype-class">'+data.well_type[0]+'</p></div>'
              }
              else if(data.well_type[0] == 'A'){
                return '<div class="well-name-ty-2"><p class="well-atype-class">'+data.well_type[0]+'</p></div>'
              }
              else if(data.well_type[0] == 'O'){
                return '<div class="well-name-ty-3"><p class="well-otype-class">'+data.well_type[0]+'</p></div>'
              }
              
          }},
          {data: null ,
              render: function(data){
                return '<p class="project-name-class">'+data.project_name+'</p>'
          }},
          {data: null , 
            render: function(data){
              return '<p class="block-name-class">'+data.block_name+'</p>'
          }},
          {data: null ,
              render: function(data){
                return '<p class="field-name-class">'+data.field_name+'</p>'
          }},
          {data: null ,
                render: function(data){
                  return '<p class="environment-class">'+data.environment+'</p>'
          }},

        // { data: 'well_name',className: 'well-name-class' },
        // { data: 'well_type',className: 'well-type-class' },
        // { data: 'project_name', className: 'project-name-class' },
        // { data: 'block_name', className: 'block-name-class' },
        // { data: 'field_name', className: 'field-name-class' },
        // { data: 'environment', className: 'environment-class' },
        {
          data: null,
          render: function(data, type, row) {
              return '<div class="dashboardwell-action-icons">' +
              '<span class="action-icon icon-sp"><a href="/wells/edit/' + data.well_id + '"><i class="fa fa-edit"></i></a></span> ' +
              '<a onclick="confirmation(event)" href="/wells/delete/'+ data.well_id + '"> <span class="action-delete-well icon-sp"><i class="feather icon-trash"></i></span></a>' + 
              '</div>';
                     
        
          }
        }
        
      ]
    });
  }

  function initialize_projectDataTable(selectedValues,search_value) {

    dashboard_table_2 = $('.project_dashboardtable').DataTable({
      serverSide: true,
      searching: false,
      lengthChange: false,
      responsive: true,
      language: {
        emptyTable: "---", 
    },
    drawCallback: function(settings) {
      if (dashboard_table_2.rows().count() === 0) {
          $('.dataTables_paginate, .dataTables_info').hide();
      } else {
          $('.dataTables_paginate, .dataTables_info').show();
      }
  },
      ajax: {
        url: "getwelldatas",
        data: {
          selected_values: selectedValues.join(","),
          filter_type: "projects",
          search_value:search_value
        },
        method: 'GET',
      },
      columns: [
        {data: null ,
        render: function(data){
          return '<div><p class="project_name-class">'+data.project_name+'</p></div>'
        }},
        {data: null ,
          render: function(data){
            return '<div><p class="project_name-class">'+data.default_units+'</p></div>'
        }},
        {data: null ,  
            render: function(data){
              return '<div><p class="country-class">'+data.country+'</p></div>'
        }},
        {data: null ,
          render: function(data){
            return '<div class="total-circle"><p class="total_actual_wells-class">'+data.total_actual_wells+'</p></div>'
        }},
        {data: null ,
            render: function(data){
              return '<div class="total-circle"><p class="total_plan_wells-class">'+data.total_plan_wells+'</p></div>'
        }},
        {data: null ,
              render: function(data){
                return '<div class="total-circle"><p class="total_offset_wells-class">'+data.total_offset_wells+'</p></div>'
        }},
     
        // { data: 'project_name',className:'project_name-class' },
        // { data: 'default_units',className:'project_name-class' },
        // { data: 'country',className:'country-class' },
        // { data: 'total_actual_wells',className:'total_actual_wells-class' },
        // { data: 'total_plan_wells',className:'total_plan_wells-class' },
        // { data: 'total_offset_wells',className:'total_offset_wells-class' },
        // { data: 'status',className:'total_status-class' },
        {
          data: null, 
          render: function(data, type, row) {
            return '<div class="dashboardproj-action-icons">' +
            '<span class="action-icon icon-sp"><a href="/projects/' + data.project_id + '"><i class="fa fa-eye"></i></a></span> ' +
            '<span class="action-icon icon-sp"><a href="/projects/edit/' + data.project_id + '"><i class="fa fa-edit"></i></a></span> ' +
            '<span class="action-icon icon-sp"><a href="/projects/createprojectusers/' + data.project_id + '"><i class="feather icon-user-plus"></i></a></span> ' +
            '<a onclick="confirmation(event)" href="/projects/delete/' + data.project_id + '"> <span class="action-delete-project icon-sp"><i class="feather icon-trash-2"></i></span></a>' +
            '</div>';
          }
        }
      ]
    });

    var searchInput = $('#DataTables_Table_0_wrapper').find('.dataTables_filter input');
    console.log("searchInput"+searchInput)
    searchInput.attr('placeholder', 'Search...'); 
    searchInput.wrap('<div class="search-wrapper"></div>'); 
    $('.search-wrapper').prepend('<i class="fas fa-search search-icon"></i>');
    $('.search-icon').css({
      position: 'absolute',
      top: '60%',
      right: '7%',
      transform: 'translate(-50%,-50%)',
      color: '#rgb(170, 170, 170)'
    });
    searchInput.css({
        paddingLeft: '25px' 
    });
  }
  $(document).on("click",".cards_list_dashboard",function() {
    selectedValues = []
    selectedValues.push($(this).data('id'))
   
    var proj_well_filter = '<h2>'+$(this).data('name')+" "+filter+'</h2>'
    $('.proj-name-show').html(proj_well_filter)
    if (filter === "wells") {
      $('.project_dashboardtable').css('display', 'none');
      $('.well_dashboardtable').show();
      $('#DataTables_Table_1_wrapper').css('display', 'block');
      $('#DataTables_Table_0_wrapper').css('display', 'none');
      if(dashboard_table_1){
        dashboard_table_1.destroy();
      }
      initialize_wellDataTable(selectedValues,search);
    }
    if (filter === "projects") {
      $('.well_dashboardtable').hide();
      $('.project_dashboardtable').show();
      $('#DataTables_Table_0_wrapper').css('display', 'block');
      $('#DataTables_Table_1_wrapper').css('display', 'none');
      if (dashboard_table_2) {
        dashboard_table_2.destroy();
      }
      initialize_projectDataTable(selectedValues,search);
    }
    var downloadLink = $('.download-link');
    downloadLink.attr('data-selected-values', selectedValues);
    downloadLink.attr('data-filter', filter);
    downloadLink.attr('data-search', search);
    // Update the href attribute with the new values
    var newHref = downloadLink.attr('href').split('?')[0] + '?selected_values=' + selectedValues + '&filter=' + filter + '&search=' + search;
    downloadLink.attr('href', newHref);
    
 });


 $(".search-dashboard-table").on('keyup',function(){
  search = $(this).val()

  if (filter === "wells") {
    $('.project_dashboardtable').css('display', 'none');
    $('.well_dashboardtable').show();
    $('#DataTables_Table_1_wrapper').css('display', 'block');
    $('#DataTables_Table_0_wrapper').css('display', 'none');
    if(dashboard_table_1){
      dashboard_table_1.destroy();
    }
    initialize_wellDataTable(selectedValues,search);
  }
  else{
    $('.well_dashboardtable').hide();
    $('.project_dashboardtable').show();
    $('#DataTables_Table_0_wrapper').css('display', 'block');
    $('#DataTables_Table_1_wrapper').css('display', 'none');
    if (dashboard_table_2) {
      dashboard_table_2.destroy();
    }
    initialize_projectDataTable(selectedValues,search);
  }
  var downloadLink = $('.download-link');
  downloadLink.attr('data-selected-values', selectedValues);
  downloadLink.attr('data-filter', filter);
  downloadLink.attr('data-search', search);

  // Update the href attribute with the new values
  var newHref = downloadLink.attr('href').split('?')[0] + '?selected_values=' + selectedValues + '&filter=' + filter + '&search=' +search;
  downloadLink.attr('href', newHref);
})
});
$(document).ready(function () { 
  $('.project-country').owlCarousel({
    margin:10,
    dots:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:3
        },
        1200:{
          items:2
      },
      1500:{
        items:3
    },
    1700:{
      items:4
  },
    1800:{
      items:4
  }
    }
  })


  $('.dropdown-header').click(function() {
    $('.dropdown-card').slideToggle();
  });
  
  $('.dropdown-card li, .apply_dropdown, .cancel_dropdown ').click(function() {
    $('.dropdown-card').slideUp();
  });
  $('.cancel_dropdown ').click(function() {
    $('.country-checkbox').prop('checked', false);
  
  });

  function updateCountryDropdown() {
    var country_search_value = $('.country-search').val();
    $.ajax({
      url: "countrysearch/",
      method: 'POST',
      headers: { "X-CSRFToken": csrf_token },
      data: {
        country_search_value: country_search_value,
      },
      success: function (data) {
        var country_list = '';
        for (var i = 0; i < data.length; i++) {
          country_list += `<ul class="scroll-item">
          <span class="border-btm" style="display:flex">
            <input type="checkbox" class="check_options country-checkbox" value="${data[i].country_id}">
            <li>${data[i].country_name}</li>
          </span>
        </ul>`;
        }
        console.log()
        $('#list-dropdown-country').html(country_list);
      },
    });
  }

  $('.country-search').on('keyup', function() {
    updateCountryDropdown();
  });


  $("#checkAll").click(function () {
    $(".country-checkbox").prop('checked', $(this).prop('checked'));
});

$(".cards_list_dashboard").click(function() {
  // Remove active class from all items
  $(".cards_list_dashboard").removeClass("active");
  
  // Add active class to the clicked item
  $(this).addClass("active");
});
  
})
  
  
    
