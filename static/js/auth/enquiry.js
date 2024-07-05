$(document).ready( function () {   
   $("form[name='enquiry_form']").validate({
        errorClass: "red-outline",
        errorPlacement: function(error, element) {
            return true; 
        },
        rules: {
            name: "required",
            gender:"required",
            firstname:"required",
            lastname:"required",
            country:"required",
            companyname:"required",
            email: {
                required: true,
                email: true,
                remote:{
                    url: '/usermailexists',
                    type: "get",
                    data:
                    {
                        email: function()
                        {
                            return $('#email').val();
                        }
                    },
                    dataFilter: function(data) {
                        var json = JSON.parse(data);
                        return !json.email;
                    }
                }
            },
            message:"required",
        },
        
        messages: {
            name:"Please enter your name",
            gender: "Please select a prefix",
            email:{
                required: "Please provide a email ",
                email: "Please provide a valid email",
                remote: jQuery.validator.format("{0} is already taken.")
            },
            message: "Please enter your message",
        },
        submitHandler: function(form) {
            var messageContent = $.trim($('#message').summernote('code'));
            if (messageContent !== '' && messageContent !== '<p><br></p>') {
               form.submit()
            }else{
                $(".summernote-container").addClass("red-outline");

            } 
        }
    })
    
})