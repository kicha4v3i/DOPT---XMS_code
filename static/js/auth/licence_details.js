$(document).ready(function(){
    var adduser_url = $('#createuser-url').data('base-url');
    var license_url = $('#license-url').data('base-url');
    if(licence_type =='individual'){
        alert("cdg")
        Swal.fire({
            title: 'Do you want to add client admin?', 
            showCancelButton: true,
            confirmButtonText: `Create`,
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href=adduser_url
            } 
            else if (result.isDenied) {
                window.location.href=license_url

            }

        })
    }
})