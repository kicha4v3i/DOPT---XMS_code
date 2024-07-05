$(document).ready(function() {
    $(document).on("change", "#license_type" , function(){ 
        var license_type=$(this).val()
        if(license_type=='Individual'){
            $('#noofusers_div').hide()
        }else{
            $('#noofusers_div').show()
        }
    })
})

