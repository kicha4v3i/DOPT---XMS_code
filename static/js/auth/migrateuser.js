$(document).ready(function() {
    $("#migrateuser_form").validate({
            errorClass: "red-outline",
            errorPlacement: function(error, element) {
                return true; 
            }
        }
    );
    if(projects_length>0){
        $(".projectusers").each(function() {
            $(this).rules("add", {
                required: true,
                messages: {
                    required: "This field is required."
                }
            });
        });
    }
    if(wells_length>0){
        $(".well_users").each(function() {
            $(this).rules("add", {
                required: true,
                messages: {
                    required: "This field is required."
                }
            });
        });
    }
    

    $("#migrateuser_form").submit(function(event) {
        if (!$(this).valid()) {
            event.preventDefault(); 
        }
    });
})

