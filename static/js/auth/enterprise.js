$(document).ready( function () {
    $('.table_css').DataTable({
        language : {
        sLengthMenu: "Show Entry _MENU_"
        }
    });

    $("form[name='company_admin_form']").validate({
        errorClass: "red-outline",
        // debug: true, 
        errorPlacement: function(error, element) {
          if (element.attr("name") === "new_password1" || element.attr("name") === "new_password2") {
            error.addClass("password-error");
            element.removeClass('red-outline')
            error.insertAfter(element);  
          }
        
        },
        rules: {
          firstname: "required",
          lastname: "required",
          name: "required",
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
                                return $('#email').val();
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
    
          gender:"required",
          companyname:"required",
          designation:"required",
          noofusers:"required",
          concurrent_users:"required",
          subscription_type:"required",
          start_date:"required",
          end_date:"required",
          new_password1:{
            required:true,
            customPassword:true
          },
          new_password2:{
            required: true,
            equalTo : "#user-password",
          }
    
    
        },
        messages: {
          firstname:"Please enter your firstname",
          lastname:"Please enter your lastname",
          gender: "Please select a prefix",
          email:{
            required: "Please provide a email ",
            email: "Please provide a valid email",
            remote: jQuery.validator.format("{0} is already taken.")
          },
          companyname:"please enter companyname",
          designation:"please enter designation",
          noofusers:"Please enter no-of-users",
          concurrent_users:"please enter concurrent users",
          subscription_type:"please enter subscription type",
          start_date:"please select start date",
          end_date:"please select end date",
          new_password1:{
            required:"please enter your password",
          },
    
          new_password2:{
            required:"please enter your password",
            equalTo:"Password Mismatch",
          }
    
        },
        submitHandler: function(form) {
          form.submit();
        }
    })

    $.validator.addMethod("customPassword", function(value, element) {
        return this.optional(element) || passwordregex.test(value);
    }, "Password should have minimum 8 letters, consisting of atleast one from A-Z, a-z, 0-9 and Special Characters.");
    
    $.validator.addMethod("customEmail", function(value, element) {
        return this.optional(element) || emailregex.test(value);
    }, "Please enter a valid email address.");
      

    $('#start_date').flatpickr();
    $('#end_date').flatpickr();

    $(document).on("change","#start_date" , function() {
        var selectedOption = $('#subscription_type').find("option:selected");
        var subscription_type=$('#subscription_type').val()
        var days = selectedOption.data("days");
        var newdate=adddays(days,$(this).val())
        $('#end_date').val(newdate)



    })
})

function adddays(days,givenDate){
const [year, month, day] = givenDate.split('-');
const date = new Date(year, month - 1, day);
date.setDate(date.getDate() + days);
const updatedYear = date.getFullYear();
const updatedMonth = date.getMonth() + 1;
const updatedDay = date.getDate();
const updatedDate = `${updatedYear}-${updatedMonth.toString().padStart(2, '0')}-${updatedDay.toString().padStart(2, '0')}`;
return updatedDate
}