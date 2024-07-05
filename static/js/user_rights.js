$(document).on('click','.detail-button-reset',function(){
    $('#adduserform')[0].reset();
})



$(document).on('change', '.user_rights', function() {
    var nameAttr = $(this).attr('name');
    var isChecked = $(this).prop('checked');
    if (isChecked == true){
        $("."+nameAttr).prop('checked',true)
    }
    else{
        $("."+nameAttr).prop('checked',false)
    }
    
});