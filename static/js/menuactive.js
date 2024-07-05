$(document).ready(function() {
    var storedArray = JSON.parse(sessionStorage.getItem("items"));
    var well_id="{{well_id}}"
    if(storedArray!=null){
        if(well_id == storedArray[1]){
            $('.warning').show();
        }else{
            $('.warning').hide();
        }
    }


    var toggler = document.getElementsByClassName("nested_list");
    var i;

    for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        this.classList.toggle("caret-down");
    });
    }

    $('.allmultiple-menu').click(function(){
        var type=$(this).attr('data-menu')
        var id=$(this).attr('data-id')

        $.ajax({
            type: "GET",
            url:"/wells/muddata/setsession",
            data:{
                val:parseInt(id),
                typename:type
                
            },
            success: function(data) {
            }
        });
    })
    $('.block_name').click(function(){
        $('.block_name').removeClass('caret-down');
        $('.block_name').siblings('ul').removeClass('active');
        $(this).addClass('caret-down');
        $(this).siblings('ul').addClass('active')
    })
    $('.field_name').click(function(){
        $('.field_name').removeClass('caret-down');
        $('.field_name').siblings('ul').removeClass('active');
        $(this).addClass('caret-down');
        $(this).siblings('ul').addClass('active')

    })
    
    $('.country_name').click(function(){
        // alert('county');
        $('.nested').removeClass('active');
        $('.nested_list').removeClass('caret-down');
        $(this).addClass('caret-down')
        $(this).siblings('ul').addClass('active')

    })
    $('.project-navigation').click(function(){
        Swal.fire({
            title: 'Do you want to create project?',
            showCancelButton: true,
            allowOutsideClick: false,
            confirmButtonText: `Create`,
            cancelButtonText:'No',
            }).then((result) => {
            if (result.isConfirmed) {
                window.location.href=projecturl;
            } else {
                window.location.href=wellurl

            }
      }) 
    })
    // Create well
    // $('.well-create').click(function(){
    //     Swal.fire({
    //             title: 'Do you want to create a well?',
    //             showCancelButton: true,
    //             confirmButtonText: `Create`,
    //         }).then((result) => {
    //         /* Read more about isConfirmed, isDenied below */
    //         if (result.isConfirmed) {
    //                 window.location.href=wellurl;
    //             } else if (result.isDenied) {
    //                 Swal.fire('Changes are not saved', '', 'info')
    //             }
    //     })
    // });
    $('.hide-show').on('click',function(){   
        $('.side-section').animate({
            width: "toggle"
          });
        $('.main-section').toggleClass('col-10');
        $('.main-section').toggleClass('col-md-12');
        $('.side-section').toggleClass('showbar');
        // sa added js
        if($('.main-section').hasClass("col-md-8")){
            $('.main-section').removeClass('col-10'); 
            $('.main-section').removeClass('col-md-12');  
            $('.main-section').toggleClass('col-md-10');  
        }
        if ($(this).hasClass("fa fa-long-arrow-right")) {
            $(this).removeClass('fa fa-long-arrow-right') 
            $(this).addClass('fa fa-long-arrow-left')
            $('.well-name-list').hide();
            
        }else{
            $(this).removeClass('fa fa-long-arrow-left') 
            $(this).addClass('fa fa-long-arrow-right') 
            $('.well-name-list').show();
        }
        
    });

})
$('body').on('focus',".start_date", function(){
    $(this).flatpickr({
        // minDate: "today",
        dateFormat: "d-m-Y",
        defaultDate: $(this).val()!=''?$(this).val():new Date()
    });
});
$('body').on('focus',".start_time", function(){
    $(this).flatpickr({
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        defaultDate: $(this).val()!=''?$(this).val():"12:00"
    });
});
