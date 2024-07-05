$(document).ready(function() {
    $('.add-project-user').click(function(){
        var adduser_url=$('#adduser_url').val()
        adduser_url=adduser_url.replace('0',project_id)
        console.log(adduser_url)
        if(usercount==1){
            toastr.success('Please Add User Details',{ "showDuration": 500});
            setTimeout(function(){
                window.location.href = '/user_create';
             }, 500); 
        }else{
            window.location.href = adduser_url;
  
        }

    })
    $('.add_well').click(function(){
        Swal.fire({
            title: 'Do you want to create a well?',
            showCancelButton: true,
            confirmButtonText: `Create`,
            }).then((result) => {
            if (result.isConfirmed) {
            $('#createwell')[0].click();
            } else if (result.isDenied) {
            Swal.fire('Changes are not saved', '', 'info')
            }
        })
    })
})