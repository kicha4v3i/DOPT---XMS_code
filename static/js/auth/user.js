$('.custom_role_div').hide()
$(document).on('click','.detail-button-reset',function(){
    $('#adduserform')[0].reset();
})

$(document).on('click','.submiteditadduserbtn',function(){
  $('form[name="editclientuserform"]').submit();
})


// $(document).on('change','#group',function(){
//   if($(this).val()=='new'){
//       $('.custom_role_div').show()
//       $('.editadduserform_btn').html(
//           '<button class="btn btn-primary mr-1 waves-effect waves-float waves-light detail-button nexteditadduserbtn">Next</button>'
  
//       )
//   }else{
//       $('.custom_role_div').hide()
//       $('.editadduserform_btn').html(
//           '<button class="btn btn-primary mr-1 waves-effect waves-float waves-light detail-button submiteditadduserbtn">Submit</button>'
  
//       )
//   }
// }) 

$(document).on('click','.nexteditadduserbtn',function() {
  $('.editadduserform').hide()
  $('.edituserrights_pg').show()
}
)




$(document).on('click','.action-edit',function(e){
close_form = $(this).closest('form')
$(this).attr('disabled',true)
close_form.submit();


})
// var editIcon = $(".edit-icon");
// var editForm = $(".edit-form");
// editIcon.on("click", function(event) {
//   event.preventDefault();
//   editForm.submit();
// });

// $(document).on('click','.action-edit',function(e){
//     e.stopPropagation();
//     var name = $(this).closest('tr').find('.name').data('value');
//     var email = $(this).closest('tr').find('.email').data('value');
//     var group = $(this).closest('tr').find('.role').data('value');
//     var designation = $(this).closest('tr').find('.designation').data('value');
//     var id = $(this).closest('tr').find('.name').data('id');
//     var role = $(this).closest('tr').find('.name').data('role');
//     var lastname = $(this).closest('tr').find('.lastname').data('value');
//     var title = $(this).closest('tr').find('.title').data('value');
//     $('#gender').val(title)
//     $('#name').val(name);
//     $('#id').val(id);
//     $('#email').val(email);
//     $('#designation').val(designation);
//     $('#last_name').val(lastname);
//     $('#group').val(group);
//     $('.password').hide();
//     $('#group').val(role)
//     $('.confirmpassword').hide();

//     $(".add-new-data").addClass("show");
//     $(".overlay-bg").addClass("show");
// });

$(".data-list-view").DataTable({
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
    sSearch: "",
    oPaginate: {
      sNext: "",
      sPrevious: ""
    },
    sEmptyTable: "---" 
  },
  aLengthMenu: [[10, 15, 20], [10, 15, 20]],
  bInfo: false,
  pageLength: 10,
  buttons: [],
  initComplete: function(settings, json) {
    $(".dt-buttons .btn").removeClass("btn-secondary")
  }
});

$(document).on('click','.add_user',function(e){
    $('#name').val("");
    $("#designation").val("");
    $('#id').val("");
    $('#email').val("");
    if ($('#group').prop('selectedIndex') === -1) {
        $('#group').prop('selectedIndex', 0);
    }
    $(".add-new-data").addClass("show")
    $(".overlay-bg").addClass("show")
})

$(document).on('click','.action-delete',function(e){
  var user_row=$(this).closest('td').closest('tr');
  var user_id=$(this).closest('span').attr('data-id')

  Swal.fire({
    title: 'Do you want to delete user?',
    showCancelButton: true,
    confirmButtonText: 'Yes',
    cancelButtonText: 'No',
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "GET",
          url:"/users/delete/"+user_id+"/",
          beforeSend: function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrf);
          },
          success: function(data) {
            user_row.hide();
            Swal.fire('Deleted!', 'User Deleted Successfully.', 'success')
          }
        });
      } 
      else if (result.isDenied) {
        Swal.fire('User not deleted')
      }
  }) 
})

$(document).on('click','.reset_password',function(e){
  var user_row=$(this).closest('td').closest('tr');
  var user_id=$(this).closest('span').attr('data-id')

  Swal.fire({
    title: 'Do you want to reset password?',
    showCancelButton: true,
    confirmButtonText: 'Yes',
    cancelButtonText: 'No',
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          type: "GET",
          url:"/reset_password/"+user_id+"/",
          beforeSend: function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrf);
          },
          success: function(data) {
            Swal.fire('Password Reset', 'Password Reset Successfully.', 'success')
          }
        });
      } 
      else if (result.isDenied) {
      }
  }) 
})



$(document).on('click','.user-delete',function(e){
  var user_id=$(this).closest('span').attr('data-id')
  var base_url = $('#migrateuser-url').data('base-url');
  var url = base_url.replace('0', user_id);
  var user_row=$(this).closest('td').closest('tr');
  $.ajax({
      type: "POST",
      url:"/projects/check_user_hasproject",
      data:{
        user_id:user_id
      },
      beforeSend: function(xhr){
        xhr.setRequestHeader('X-CSRFToken', csrf);
      },
      success: function(data) {
        if(data.status==true){
          Swal.fire({
            title: 'Do you want to migrate project?',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href=url
              } 
              else if (result.isDenied) {
                Swal.fire('User not deleted')
              }
            }) 

        }else{
          Swal.fire({
            title: 'Are you sure to delete the user?',
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes',
            showLoaderOnConfirm: true,
            preConfirm: function() {
                return new Promise(function(resolve) {
                  var csrf =$('.getcsrf').val();
                  $.ajax({
                    type: "GET",
                    url:"/users/delete/"+user_id+"/",
                    beforeSend: function(xhr){
                      xhr.setRequestHeader('X-CSRFToken', csrf);
                    },
                    success: function(data) {
                      user_row.hide();
                      Swal.fire('Deleted!', 'User Deleted Successfully.', 'success')
                    }
                  });
                });
            },
        });
        }
    
      }
  });
})

$(".is_allcountry").click(function() {
  if ($(".is_allcountry").is(":checked")) {
    $('#project_country_div').hide()
  } else {
    $('#project_country_div').show()
  }
})




