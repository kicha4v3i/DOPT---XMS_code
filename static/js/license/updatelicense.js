

$(document).ready(function(){

    $("#submit_license").click(function(event){
       alert(no_of_users)
        event.preventDefault();
        var selected_no_of_users = $("input[name='choose_package']:checked").data("attr");
       
        if (selected_no_of_users < parseInt(no_of_users)){
            Swal.fire({
                title: 'You have selected '+selected_no_of_users+' users. Do you want to upgrade or downgrade?',
                showCancelButton: true,
                allowOutsideClick: false,
                confirmButtonText: `Upgrade`,
                cancelButtonText:`Downgrade`,
                }).then((result) => {
                    if (result.isConfirmed) {
                      $("#submit_type").val("Upgrade")
                    } else  {
                      $("#submit_type").val("Downgrade")
                    } 
                    $("#queries_form").submit();
              })
        }
        else{
            $("#queries_form").submit();
        }

    })

//  $("#submit_license").click(function(event) {
//         event.preventDefault();
//         var selected_no_of_users = $("input[name='choose_package']:checked").data("attr");
//        console.log('users', selected_no_of_users, no_of_users);
//         if ((selected_no_of_users + parseInt(no_of_users)) > 15) {
//            console.log(selected_no_of_users + parseInt(no_of_users));
//            $('#changeToEnterprise').show();
//            $("#changeToEnterprise").html('You need to change to Enterprise');
//        } else {
 //           console.log(selected_no_of_users + parseInt(no_of_users));
//            $('#changeToEnterprise').hide();
//            $("#queries_form").submit();
 //       }
 //   }); 
  

    if(licence_type == "Enterprise"){
        $("#enterprise").prop("checked", true);
        $('.no_of_users_div').show(); 
        $("#no_of_users").val(no_of_users);
    }
});

function hoverborder(){
   let radios = document.querySelectorAll(".license_package");
   Object.values(radios).map((item)=>{
    if(item.checked == true){
        let card = item.parentElement.parentElement;
        card.classList.add("mystyle");
    }else{
        let card = item.parentElement.parentElement;
        card.classList.remove("mystyle");
    }
   })
}