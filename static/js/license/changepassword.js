$(document).ready(function() {
    $("form[name='passwordchange_form']").validate({
        rules: {
            old_password:{
                required: true,
                remote:{
                    url: "checkoldpassword",
                    type: "get",
                    data:
                    {
                        old_password: function()
                        {
                            return $('#old_password').val();
                        },      
                    },
                    dataFilter: function(data) {
                      var json = JSON.parse(data);
                      return json.status;
                  }
                  }
            },
            password: {
                required: true,
                customPassword:true,
                notEqualToPassword: "#old_password" 


            },
            confirm_password:{
                required: true,
                equalTo : "#password",
            }
        },
        messages: {
            password: {
                required:"Enter  New Password",
            },
            confirm_password:{
                required:"Enter Confirm Password",
                equalTo:"Password Mismatch",
            },
            old_password:{
                required:"Enter Password",
                remote: "Old Password incorrect"

            },
        },
        highlight: function (element) {
            $(element).addClass("red-outline");
        },
        unhighlight: function (element) {
            $(element).removeClass("red-outline");
        },
        submitHandler: function(form) {
            if($(form).valid()){
                form.submit();
            }else{
                if ($(form).find("[name='password']").hasClass("error")) {
                    console.log("error")
                    if ($(form).find("[name='password']").hasClass("required")) {
                        console.log("required")
                    }
                    if ($(form).find("[name='password']").hasClass("customPassword")) {
                        console.log("customPassword")

                    }
                }

            }
        }
    });

    $.validator.addMethod("customPassword", function(value, element) {
        return this.optional(element) || passwordregex.test(value);
    }, "Password should have minimum 8 letters, consisting of atleast one from A-Z, a-z, 0-9 and Special Characters.");

    $.validator.addMethod("notEqualToPassword", function(value, element, param) {
        return value !== $(param).val();
    }, "Old Password and New Password can't be same.");

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



  