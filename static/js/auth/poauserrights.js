$(document).ready(function() {
    $('.poaselect_all').click(function(){
        if($(this).prop('checked')){
            $('.user_rights').prop('checked', true);
        }else{
            $('.user_rights').prop('checked', false);
        }
    });

})
