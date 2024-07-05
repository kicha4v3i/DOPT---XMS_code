$(document).ready(function() {
    $('.customselect_all').click(function(){
        if($(this).prop('checked')){
            $('.user_rights').prop('checked', true);
        }else{
            $('.user_rights').prop('checked', false);
        }
    });
    $('.mainmodule').click(function(){
        var mainmodule_id=$(this).val()
        if($(this).prop('checked')){
            $('.main_module'+mainmodule_id).prop('checked', true);
        }else{
            $('.main_module'+mainmodule_id).prop('checked', false);
        }
    });
    

})
