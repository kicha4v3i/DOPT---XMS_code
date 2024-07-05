$(document).ready(function() {
    
    if(group_id=='new'){
        $('.next-btn').show()
        $('.submit-btn').hide()
        $('.custom_role_div').show()
    }else{
        $('.next-btn').hide()
        $('.submit-btn').show()
        $('.custom_role_div').hide()

    }
    $(document).on('change','#group',function(){
        var role=$(this).val()
        if(role=='new'){
          $('.next-btn').show()
          $('.submit-btn').hide()
          $('.custom_role_div').show()
        }else{
          $('.custom_role_div').hide()
          $('.next-btn').hide()
          $('.submit-btn').show()
      
        }
  
    })
})