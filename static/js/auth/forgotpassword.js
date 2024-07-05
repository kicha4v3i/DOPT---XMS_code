$(document).ready(function() {
    $("form[name='forgot_password_form']").validate({
        rules: {
            password: {
                required: true,
                customPassword:true

            },
            confirm_password:{
                required: true,
                equalTo : "#password",
            }
        },
        messages: {
            password: {
                required:"please enter your password",
            },
            confirm_password:{
                required:"please enter your password",
                equalTo:"Password Mismatch",
            },
           
        }
    });

    $.validator.addMethod("customPassword", function(value, element) {
        return this.optional(element) || passwordregex.test(value);
    }, "Password should have minimum 8 letters, consisting of atleast one from A-Z, a-z, 0-9 and Special Characters.");


    $('.show-password').click(function(){
        var passwordtype=$(this).closest('span').attr('data-type')
        if($(this).closest('span').find('i').hasClass('icon-eye-off')){
           
          $(this).closest('span').find('i').removeClass('icon-eye-off');
          
          $(this).closest('span').find('i').addClass('icon-eye');
          
          $('.'+passwordtype).attr('type','text');
            
        }else{

         
          $(this).closest('span').find('i').removeClass('icon-eye');
          
          $(this).closest('span').find('i').addClass('icon-eye-off');  
          
          $('.'+passwordtype).attr('type','password');
        }
    });
    
})



  