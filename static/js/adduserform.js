$(document).ready(function() {

    $('.next-btn').hide()
    $("form[name='usercreateform']").validate({
        errorClass: "red-outline",
        errorPlacement: function(error, element) {
          if (element.attr("name") === "password" || element.attr("name") === "confirmpassword") {
            error.addClass("password-error");
            element.removeClass('red-outline')
            error.insertAfter(element);  
          }
        
        },
        rules: {
            title: "required",
            name: "required",
            lastname: "required",
            group: "required",
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
        }

    })
    $.validator.addMethod("customEmail", function(value, element) {
        return this.optional(element) || emailregex.test(value);
    }, "Please enter a valid email address.");
   
    $(document).on('change','#group',function(){
      var role=$(this).val()
      if(role=='new'){
        $('.next-btn').show()
        $('.submit-btn').hide()
        $('.custom_role_div').show()
      }else{
    
        $('.custom_role_div').hide()
    
      }

    })
    
    if($('#licence_name').val() != 'Individual'){
        var designation = $('#designation');
        if (designation.length > 0) {
          $('#designation').rules('add', {
            required: true,
            messages: {
                required: "Designation is required"
            }
          });
        }
    }

    
})

