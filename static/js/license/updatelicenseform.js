$(document).ready(function() {
    var license_type=$('#license_type').val()
    $('.no_of_users_div').hide(); 
    $(document).on("change", ".license_package" , function(){ 
        var license_package=$(this).val()
        if(license_package=='custom'){
            $('.no_of_users_div').show(); 
            $('#no_of_users').rules('add', {
                required: true,
                messages: {
                    required: "No Of Users is required"
                }
            });
              
        }else{
            $('.no_of_users_div').hide(); 
        }
      
    })

    $("form[name='licence_form']").validate({
        rules: {
            choose_package: {
                required: true
            }
        },
        messages: {
            choose_package: "Please select package."
        },
        submitHandler: function(form) {
          form.submit();
        }
      });

      if(license_type=='Individual'){
        $('#companyname').rules('add', {
            required: true,
            messages: {
                required: "Company Name is required"
            }
        });
        $('#designation').rules('add', {
            required: true,
            messages: {
                required: "Designation is required"
            }
        });
      }



    
})



  