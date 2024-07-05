/*=========================================================================================
    File Name: data-list-view.js
    Description: List View
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(document).ready(function() {
  "use strict"
  // init list view datatable
  var dataListView = $(".company-data-list-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
       // checkboxes: { selectRow: true }
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[10, 15, 20], [ 10, 15, 20]],
  
    order: [["desc"]],
    bInfo: false,
    pageLength: 10,
    buttons: [
      // {
      //   text: "<i class='feather icon-plus'></i> Add New",
      //   action: function() {
      //     $(this).removeClass("btn-secondary")
      //     $(".add-new-data").addClass("show")
      //     $(".overlay-bg").addClass("show")
      //     $("#data-name, #data-price").val("")
      //     $("#data-category, #data-status").prop("selectedIndex", 0)
      //   },
      //   className: "btn-outline-primary"
      // }
    ],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });

  // var dataListView = $(".master-data-list-view").DataTable({
  //   responsive: false,
  //   columnDefs: [
  //     {
  //       orderable: true,
  //       targets: 0,
  //      // checkboxes: { selectRow: true }
  //     }
  //   ],
  //   dom:
  //     '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
  //   oLanguage: {
  //     sLengthMenu: "_MENU_",
  //     sSearch: ""
  //   },
  //   aLengthMenu: [[10, 15, 20], [ 10, 15, 20]],
  
  //   order: [[1, "asc"]],
  //   bInfo: false,
  //   pageLength: 10,
  //   buttons: [
  //     {
  //       text: "<i class='feather icon-plus'></i> Add New",
  //       action: function() {
  //         var loc = location.href;              
  //         location.href = loc + "/create";
      
  //       },
  //       className: "btn-outline-primary"
  //     }
  //   ],
  //   initComplete: function(settings, json) {
  //     $(".dt-buttons .btn").removeClass("btn-secondary")
  //   }
  // });





  var projectdataListView = $(".project-data-list-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[10, 15, 20], [ 10, 15, 20]],
  
    order: [[1, "asc"]],
    bInfo: false,
    pageLength: 10,
    buttons: [
      {
        text: "<i class='feather icon-plus'></i> Add Project",
        action: function ( e, dt, button, config ) {
          window.location = 'create';
        },  
        className: "btn-outline-primary"
      }
    ],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });



  var welldataListView = $(".well-data-list-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[10, 15, 20], [ 10, 15, 20]],
  
    order: [[1, "asc"]],
    bInfo: false,
    pageLength: 10,
    buttons: [
      {
        text: "<i class='feather icon-plus'></i> Add Well",
        action: function ( e, dt, button, config ) {
          window.location = 'create';
        },  
        className: "btn-outline-primary"
      }
    ],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });


  // var welldataListView = $(".muddata-data-list-view").DataTable({
  //   responsive: false,
  //   columnDefs: [
  //     {
  //       orderable: true,
  //       targets: 0,
  //     }
  //   ],
  //   dom:
  //     '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
  //   oLanguage: {
  //     sLengthMenu: "_MENU_",
  //     sSearch: ""
  //   },
  //   aLengthMenu: [[10, 15, 20], [ 10, 15, 20]],
  
  //   order: [[1, "asc"]],
  //   bInfo: false,
  //   pageLength: 10,
  //   buttons: [
  //     {
  //       text: "<i class='feather icon-plus'></i> Add New",
  //       action: function ( e, dt, button, config ) {
  //         window.location = '/wells/muddata/create/';
  //       },  
  //       className: "btn-outline-primary"
  //     }
  //   ],
  //   initComplete: function(settings, json) {
  //     $(".dt-buttons .btn").removeClass("btn-secondary")
  //   }
  // });


  // init thumb view datatable

  // To append actions dropdown before add new button
  var actionDropdown = $(".actions-dropodown")
  actionDropdown.insertBefore($(".top .actions .dt-buttons"))


  // Scrollbar
  if ($(".data-items").length > 0) {
    new PerfectScrollbar(".data-items", { wheelPropagation: false })
  }

  // Close sidebar
  $(".hide-data-sidebar, .cancel-data-btn, .overlay-bg").on("click", function() {
    $(".add-new-data").removeClass("show")
    $(".edit-old-data").removeClass("show")
    $(".overlay-bg").removeClass("show")
    $("#data-name, #data-price").val("")
    $("#data-category, #data-status").prop("selectedIndex", 0)
  })


  // company user
  // $('.user-action-edit').on("click",function(e){
  //   alert('User Action-Edit')
  //   e.stopPropagation();
  //   var name = $(this).closest('tr').find('.name').data('value');
  //   var email = $(this).closest('tr').find('.email').data('value');
  //   var designation = $(this).closest('tr').find('.designation').data('value');
  //   var id = $(this).closest('tr').find('.name').data('id');
  //   $('#edit_name').val(name);
  //   $('#edit_id').val(id);
  //   $('#edit_email').val(email);
  //   $('#edit_designation').val(designation);
  //   $('.password').hide();
  //   $('.confirmpassword').hide();
  //   $(".edit-old-data").addClass("show");
  //   $(".overlay-bg").addClass("show");
  // });





  // mac chrome checkbox fix
  if (navigator.userAgent.indexOf("Mac OS X") != -1) {
    $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
  }
})
