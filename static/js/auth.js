
$(document).ready(function() {
    $('#message').summernote({
      toolbar:false
    })
 
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


   $("form[name='companyform']").validate({
    errorClass: "red-outline",
    errorPlacement: function(error, element) {
      if (element.attr("name") === "password" || element.attr("name") === "confirmpassword") {
        error.addClass("password-error");
        element.removeClass('red-outline')
        error.insertAfter(element);  
      }
    
    },
 

    rules: {
      gender: "required",
      firstname: "required",
      lastname: "required",
      subscription_type:"required",
      country:"required",
      email: {
        required: true,
        email: true,
        customEmail:true,
        remote:{
          url: "/usermailexists",
          type: "get",
          data:
          {
              email: function()
              {
                  return $('#inputEmail').val();
              },      
              id: function()
              {
                  return $('#id').val();
              }
          },
          dataFilter: function(data) {
            var json = JSON.parse(data);
            return !json.email;
          }
        }
      },
      password: {
        required: true,
        customPassword:true
      },
      confirmpassword : {
        required: true,
        equalTo : "#password",

      },
    },
    messages: {
      firstname: {
        required:"Please enter your firstname",
      },
      subscription_type:{
        required:"Please Choose Subscription Type",

      },
      lastname: {
        required:"Please enter your lastname"
      },
      gender: {
        required:"This Field is required"
      },
      password: {
        required: "Please provide a password",
      },
      confirmpassword: {
          required: "Please provide a password",
          minlength: "Your password must be at least 8 characters long",
          equalTo: "Password Mismatch"

        },
      email:{
        required: "Please provide an email",
        email: "Please provide a valid email",
        
      },
    },
    submitHandler: function(form) {
      form.submit();
    }
  });

  $.validator.addMethod("customEmail", function(value, element) {
    return this.optional(element) || emailregex.test(value);
  }, "Please enter a valid email address.");
  
  $.validator.addMethod("customPassword", function(value, element) {
    console.log("check"+passwordregex.test(value))
    return this.optional(element) || passwordregex.test(value);
  }, "Password should have minimum 8 letters, consisting of atleast one from A-Z, a-z, 0-9 and Special Characters.");


  if($('#licence_name').val()=='CompanyPlan'){
    $('#designation').rules('add', {
      required: true,
      messages: {
          required: "Designation is required"
      }
    });
    $('#companyname').rules('add', {
      required: true,
      messages: {
          required: "Company Name is required"
      }
    });
    $('#noofusers').rules('add', {
      required: true,
      messages: {
          required: "Number of users is required"
      }
    });
  }

});