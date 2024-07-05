

$(function() {
// Login Form validation
$("form[name='login_form']").validate({
   
    rules: {
        email: "required",
        password: {
            required: true,
            // password_regex: true,
        }
    },
    messages: {
      email:"Please provide a email",
      password: {
            required: "Please provide a password",
            // password_regex: "Password should have minimum 8 letters consisting atleast one from A-Z, a-z, 0-9 and special characters",
        },
    },
})


const loginForm = $('form[name="login_form"]');
const emailInput = $('input[name="email"]');
const passwordInput = $('input[name="password"]');

loginForm.submit(function (event) {
    if (emailInput.val().trim() === '') {
        emailInput.css('border-color', 'rgb(124,2,1)'); 
        event.preventDefault(); 
    } else {
        emailInput.css('border-color', ''); 
    }

    if (passwordInput.val().trim() === '') {
        passwordInput.css('border-color', 'rgb(124,2,1)'); 
        event.preventDefault(); 
    } else {
        passwordInput.css('border-color', ''); 
    }
});





// Proposal form validation
$("form[name='proposal_form']").validate({
    rules: {
        company_name: "required",
        name:{
            required:true,
        },
        last_name:"required",
        contact_no:{
            required: true,
            valid_contactno: true,
            minlength:5,
            maxlength:20,
        },
        country_id:"required",
        email: {
            required: true,
            email: true,
            remote:{
                url: '/usermailexists',
                type: "get",
                data:
                {
                    email: function()
                    {
                        return $('#inputEmail').val();
                    }
                },
                dataFilter: function(data) {
                    var json = JSON.parse(data);
                    return !json.email;
                }
            }
        },
        password: {
            required: true,
            // password_regex: true,
            minlength: 8
        },
        license_type:"required",
        no_of_users:"required",
        concurrent_users:{
            required: true,
            checkuser:true,
        },
        cloudserver:"required",
    },
    messages: {
        company_name:"Please enter your company name",
        name:{
            required:"Please enter your first name",
        },
        last_name:"Please enter your last name",
        contact_no: {
            required: "Please provide a contact number",
            valid_contactno: "Please provide a valid contact number",
            minlength: "Please enter at least 5 numbers",
            maxlength: "Please enter no more than 20 numbers"
        },
        country_id:"Please select a country",
        email:{
            required: "Please provide a email",
            email: "Please provide a valid email",
            remote: jQuery.validator.format("{0} is already taken.")
          },
        password: {
            required: "Please provide a password",
            // password_regex: "Password should have minimum 8 letters consisting atleast one from A-Z, a-z, 0-9 and special characters",
        },
        license_type: "Please select a license type",
        no_of_users: "Please enter your number of users",
        concurrent_users: {
            required:"Please enter your concurrent users",
            checkuser:"Concurrent Users must be lesser than Number of Users"
        },
        
        cloudserver: "Please select a cloudserver",
    }
})
$.validator.addMethod("checkuser", function(value) {
    var users=$('#no_of_users').val();
    if(parseInt(value) > parseInt(users)){
        return false;
    }
    else{
        return true;
    }
});
$.validator.addMethod("email", function(value) {
    var emailReg = /^\w+([-+.'][^\s]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    if( !emailReg.test( value ) ) {
        return false;
    } else {
        return true;
    }
});

$.validator.addMethod("password_regex", function(value) {
    return /^.*(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).*$/.test(value);
});

$.validator.addMethod("valid_contactno", function(value) {
    var emailReg2 = /^[\d ]*$/;
    if( !emailReg2.test( value ) ) {
    return false;
    } else {
    space_count=value.replace(/\d/g, "").length;
    if(space_count>=3){
        return false;
    }
    else{
        return true;
    }
    }
});

// Surface form validation
// $('.surface_submit').click(function(){
//     var valid=true;
//     $('input[name^="rating"]').each(function(){
//         var rating= $(this).val();
//         if(rating==""){
//             $(this).css("border-color", "red");
//             $('.surface_rating').text("Enter the rating").css('color','red').css('float','left');
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $('.surface_rating').text("").css('color','');
//         }
//     })
//     $('input[name^="name"]').each(function(){
      
//         var name1= $(this).val();
//         if (name1 == "") {
//             $(this).css("border-color", "red");
//             $(this).closest('tr').find('.surface_name').text("Enter the name").css('color','red').css('float','left');
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('tr').find('.surface_name').text("").css('color','');
//         }
//     });
//     $('input[name^="length"]').each(function(){
//         var length= $(this).val();
//         if (length == "") {
//             $(this).css("border-color", "red");
//             $(this).closest('tr').find('.surface_length').text("Enter the length").css('color','red').css('float','left');
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('tr').find('.surface_length').text("").css('color','');
//         }
//     });
//     $('input[name^="identity"]').each(function(){
//         var identity= $(this).val();
//         if (identity == "") {
//             $(this).css("border-color", "red");
//             $(this).closest('tr').find('.surface_id').text("Enter the identity").css('color','red').css('float','left');
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('tr').find('.surface_id').text("").css('color','');
//         }
//     });
//     if(valid==false){
//         return false;
//     }else{
//         return true;
//     }
// })
$(document).on('keypress','#rating', function(){
    $(this).css("border-color", "");
    $('.surface_rating').text("").css('color','');
    valid=true;
});
$(document).on('keypress','#name', function(){
    $(this).css("border-color", "");
    $(this).closest('tr').find('.surface_name').text("").css('color','');
    valid=true;
});
$(document).on('keypress','#length', function(){
    $(this).css("border-color", "");
    $(this).closest('tr').find('.surface_length').text("").css('color','');
    valid=true;
});
$(document).on('keypress','#identity', function(){
    $(this).css("border-color", "");
    $(this).closest('tr').find('.surface_id').text("").css('color','');
    valid=true;
});
// Surface validation end
// Rig validations
$("form[name='rigform']").validate({
    rules: {
        rig_name:"required",
        rig_contractor:"required",
        rig_type:"required",
    },
    messages: {
        rig_name:"Please enter your Rig name",
        rig_contractor:"Please enter your rig contractor",
        rig_type: "Please enter your rig type"
    },
})

$(document).on('change','.pump_manufacturer', function(){
    $(this).css("border-color", "");
    $('.pump_manufacturer_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#stroke_length', function(){
    $(this).css("border-color", "");
    $('.stoke_length_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#linear_size', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.linersize_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.max_discharge_pressure', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.max_discharge_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#pump_speed', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.pump_speed_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#flowrate', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.flowrate_error').text("").css('color','');
    valid=true;
});
// Mudpump validation end

// WellPhase validation
$('.wellphase_submit').click(function(event){

    var valid=true;
    count_array = []
    var field_count = 0;
    $(".wellphase_row").each(function() {
        
        var phase_name = $(this).find('input[name^="phase_name"]').val()
        var casing_type = $(this).find('select[name^="casing_type"]').val()
        var hole_size = $(this).find('input[name^="hole_size"]').val()
        var casing_size = $(this).find('input[name^="casing_size"]').val()
        var measured_depth = $(this).find('input[name^="measured_depth"]').val()
        var true_vertical_depth = $(this).find('input[name^="true_vertical_depth"]').val()
        var lineartop = $(this).find('input[name^="lineartop"]').val() 
        console.log('jjjj'+field_count,phase_name,casing_type,hole_size,casing_size,measured_depth,true_vertical_depth,lineartop)
    
        if(phase_name == '' && casing_type == '' && hole_size == '' && casing_size == '' && measured_depth == '' && true_vertical_depth == '' && lineartop == ''){
            field_count=1
        } 
        else {
            
            if(phase_name == ''){
             valid = false
                $(this).find('input[name^="phase_name"]').css("border-color", "red");
                $(this).find('.phase_name_error').text("Enter the Pump name").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(casing_type == ''){
                valid = false
                $(this).find('input[name^="casing_type"]').css("border-color", "red");
                $(this).find('.casing_type_error').text("Enter the casing type").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(hole_size == ''){
                valid = false
                $(this).find('input[name^="hole_size"]').css("border-color", "red");
                $(this).find('.hole_size_error').text("Enter the Hole Size").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(casing_size == ''){
                valid = false
                $(this).find('input[name^="casing_size"]').css("border-color", "red");
                $(this).find('.casing_size_error').text("Enter the Casing Size").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(measured_depth == ''){
                valid = false
                $(this).find('input[name^="measured_depth"]').css("border-color", "red");
                $(this).find('.md_error').text("Enter the MD").css({'color':'red','float':'left','font-size': '13px'});
            }
    
            if(true_vertical_depth == ''){
                valid = false
                $(this).find('input[name^="true_vertical_depth"]').css("border-color", "red");
                $(this).find('.tvd_error').text("Enter the TVD").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(lineartop == ''){
                valid = false
                $(this).find('input[name^="lineartop"]').css("border-color", "red");
                $(this).find('.lineartop_error').text("Enter the Linear Top").css({'color':'red','float':'left','font-size': '13px'});
            }
        }
        
        
       



             
        });
        console.log(valid)
        if(valid == false){
            return false
        }
        else{
            return true
        }
        



    // console.log($(this).parent('td').parent('tr').css('display') == 'none')
    // $('input[name^="wellphase_startdate"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.start_date_error').text("Select the start date").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;field_count+=1
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.start_date_error').text("").css('color','');
    //         }
    //     }
            
    // })
    // $('input[name^="phase_name"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.phase_name_error').text("Enter the Pump name").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.phase_name_error').text("").css('color','');
    //         }
    //     }
            
    // })
    // $('select[name^="casing_type"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.casing_type_error').text("Enter the casing type").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.casing_type_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="hole_size"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.hole_size_error').text("Enter the Hole Size").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.hole_size_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="casing_size"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.casing_size_error').text("Enter the Casing Size").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.casing_size_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="measured_depth"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.md_error').text("Enter the MD").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.md_error').text("").css('color','');
    //         }
    //     }
    // })

    //     $('input[name^="true_vertical_depth"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.tvd_error').text("Enter the TVDss").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.tvd_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="lineartop"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'wellphasetableRow2'){
    //         if($(this).val()==""){
    //             valid=false;field_count+=1
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.lineartop_error').text("Enter the Linear Top").css({'color':'red','float':'left','font-size': '13px'});
                
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.lineartop_error').text("").css('color','');
    //         }
    //     }
    // })

    
    // if(valid==false){
    //     if(field_count==7){
    //         return true
    //     }
    //     else{
    //         return false
    //     }
    // }
    // else{
    //     return true
    // }
})
$(document).on('keyup','#wellphase_startdate', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.start_date_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#phase_name', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.phase_name_error').text("").css('color','');
    valid=true;
});
$(document).on('change','#casing_type', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.casing_type_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#hole_size', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.hole_size_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','#casing_size', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.casing_size_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#measured_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.md_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','#true_vertical_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.tvd_error').text("").css('color','');
    valid=true;
});
// Wellphase validation ends

// Casing validation 
// $('.casing_close').click(function(){
//     var valid=true;
//     $('input[name^="nominal_od"]').each(function(){
//         if($(this).val()==""){
//             $(this).css("border-color", "red");
//             $(this).closest('td').find('.casing_od_error').text("Enter the nominal od").css({'color':'red','float':'left','font-size': '13px'});
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('td').find('.casing_od_error').text("").css('color','');
//         }
//     })
//     $('input[name^="casing_weight"]').each(function(){
//         if($(this).val()==""){
//             $(this).css("border-color", "red");
//             $(this).closest('td').find('.casing_weight_error').text("Enter the Casing weight").css({'color':'red','float':'left','font-size': '13px'});
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('td').find('.casing_weight_error').text("").css('color','');
//         }
//     })
//     $('input[name^="grade"]').each(function(){
//         if($(this).val()==""){
//             $(this).css("border-color", "red");
//             $(this).closest('td').find('.casing_grade_error').text("Enter the grade").css({'color':'red','float':'left','font-size': '13px'});
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('td').find('.casing_grade_error').text("").css('color','');
//         }
//     })
//     $('input[name^="connection_type"]').each(function(){
//         if($(this).val()==""){
//             $(this).css("border-color", "red");
//             $(this).closest('td').find('.casing_type_error').text("Enter the grade").css({'color':'red','float':'left','font-size': '13px'});
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('td').find('.casing_type_error').text("").css('color','');
//         }
//     })
//     $('input[name^="casing_range"]').each(function(){
//         if($(this).val()==""){
//             $(this).css("border-color", "red");
//             $(this).closest('td').find('.casing_range_error').text("Enter the grade").css({'color':'red','float':'left','font-size': '13px'});
//             valid=false;
//         } else {
//             $(this).css("border-color", "");
//             $(this).closest('td').find('.casing_range_error').text("").css('color','');
//         }
//     })
//     if(valid==false){
//         return false;
//     }else{
//         return true;
//     }

// })

$('.trajectory_submit').click(function(){
    var valid=true;
    // console.log($(this).parent('td').parent('tr').css('display') == 'none')
    $('input[name^="trajectory_date"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.trajectory_date_error').text("Select the Date").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.trajectory_date_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="measured_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.measure_depth_error').text("Enter the MD").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.measure_depth_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="inclination"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.inclination_error').text("Enter the Inclination").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.inclination_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="azimuth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.azimuth_error').text("Enter the Azimuth").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.azimuth_error').text("").css('color','');
                // if($(this).closest('td').find('.true_vertical_depth').val() != ''){
                //     $(this).closest('td').find('.true_vertical_depth').text("").css('color','');
                // }
            }
        }
            
    })
    $('input[name^="true_vertical_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.tvd_error').text("Enter the TVD").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.tvd_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="converteddls"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.dls_error').text("Enter the DLS").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.dls_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="dls"]').each(function(){
        if($(this).closest('tr').attr('id') != 'welltrajectorytableRow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.dls_error').text("Enter the DLS").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.dls_error').text("").css('color','');
            }
        }
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('change','#date', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.trajectory_date_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#measured_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.measure_depth_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#inclination', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.inclination_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#azimuth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.azimuth_error').text("").css('color',''); 
    valid=true;
});

$(document).on('keyup','#true_vertical_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.tvd_error').text("").css('color','');
    if($(this).closest('td').parent('tr').find('.converteddls').val() != ""){
        $(this).closest('td').parent('tr').find('.converteddls').css("border-color", "");
        $(this).closest('td').parent('tr').find('.dls_error').text("").css('color','');
    };
    valid=true;
});
$(document).on('keyup','#converteddls', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.dls_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#dls', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.dls_error').text("").css('color','');
    valid=true;
});
// welltrajectory end
// Project validation
$('.project_submit').click(function(){
    var valid=true;
    $('input[name^="project_name"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $(this).closest('div').find('.project_name_error').text("Enter the Project name").css({'color':'red','float':'left','font-size': '15px'});
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).find('.project_name_error').text("").css('color','');
        }
        
    })

    if($('#project_country').val()==""){
        $('#project_country').css("border-color", "red");
        $('#project_country').closest('div').find('.country_error').text("Please select Country").css({'color':'red','float':'left','font-size': '15px'});
        valid=false;
    } else {
        $('#project_country').css("border-color", "");
        $('#project_country').closest('div').find('.country_error').text("").css('color','');
    }
        
    
    $('input[type=radio][name^="unit"]').each(function(){
        if($('input[type=radio][name^="unit"]:checked').length == 0){
            $(this).css("border-color", "red");
            $(this).closest('div').find('.unit_error').text("Please select unit").css({'color':'red','float':'left','font-size': '15px'});
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).find('.unit_error').text("").css('color','');
        }
        
    })
    $('input[name^="block"]').each(function(i){
        
        
        if($(this).closest('div').find('.block').val()==""){
            $(this).closest('div').find('.block').css("border-color", "red");
            $(this).closest('div').find('.block_error').text("Enter the block").css({'color':'red','float':'left','font-size': '15px'});
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).find('.block_error').text("").css('color','');
        }
        
    })
    $('input[name^="field"]').each(function(){
        if($(this).closest('td').find('.field').val()==""){
            $(this).closest('td').find('.field').css("border-color", "red");
            $(this).closest('td').find('.field_error').text("Enter the field").css({'color':'red','float':'left','font-size': '15px'});
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).find('.field_error').text("").css('color','');
        }
        
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('keyup','#project_name', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.project_name_error').text("").css('color','');
    valid=true;
});
$('#project_country').change(function(){
    $('#project_country').css("border-color", "");
    $('#project_country').closest('div').find('.country_error').text("").css('color','');
})
$('input[type=radio][name^="unit"]').click(function(){  
    $(this).closest('div').css("border-color", "");
    $(this).closest('div').find('.unit_error').text("").css('color','');
});
$(document).on('keyup','.block', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.block_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.field', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.field_error').text("").css('color','');
    valid=true;
});
// Project validation end

// Well validations 
$("form[name='wellcreateform']").validate({
    rules: {
        project: "required",
        block: "required",
        field: "required",
        well_type: "required",
        name: "required",
        datum: "required",
        environment:{ 
                required: true
          },
        coordinate_system: "required",
        projection: "required",
        longtitude_coords_degrees:{
            required : true,
        },
        longtitude_coords_minutes:{
            required : true,
        },
        longtitude_coords_seconds:{
            required : true,
        },
        longtitude_compass:{
            required : true,
        },
        latitude_coords_degrees:{
            required : true,
        },
        latitude_coords_minutes:{
            required : true,
        },
        latitude_coords_seconds:{
            required : true,
        },
        latitude_compass:{
            required : true,
        },
        // northing:{
        //     northing_val:true
        // },
        // easting:{
        //     easting_val:true
        // }
    },
    groups: {
        longtitudeGroup: "longtitude_coords_degrees longtitude_coords_minutes longtitude_coords_seconds longtitude_compass",
        latitudeGroup: "latitude_coords_degrees latitude_coords_minutes latitude_coords_seconds latitude_compass"
    },
    
    messages: {
        project:"Please select project",
        block:"Please select block",
        field:"Please select field",
        well_type:"Please select well type",
        name:"Please enter name",
        datum:"Please select datum",
        environment:{
            required:"Please select environment",
        },
        coordinate_system:"Please select coordinate system",
        projection:"Please select projection",
        // northing:"Please select northing",
        // easting:"Please select easting",
    },
})
// $.extend($.validator.messages, {
//     required: "Fill all the fields"
// });
$('.drillbit_submit').click(function(){

    var valid=true;  
    $('select[name^="bit_type"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.bittype_error').text("Enter the bit type").css({'color':'red','float':'left','font-size': '13px'});
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.bittype_error').text("").css('color','');
        }
    })  
    $('input[name^="manufacture"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.manufacture_error').text("Enter the Manufacturer").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.manufacture_error').text("").css('color','');
        }
    })
    $('input[name^="no_of_nozzle"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.nozzle_error').text("Enter the number of nozzle").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.nozzle_error').text("").css('color','');
        }
    })
    $('checkbox[name^="external_nozzle"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.external_nozzle_error').text("Enter the External nozzle").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.external_nozzle_error').text("").css('color','');
        }
    })
    $('input[name^="nozzles-0-nozzle_size"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.nozzle_size_error').text("Enter the nozzle size").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.nozzle_size_error').text("").css('color','');
        }
    })
    $('input[name^="nozzle_size"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.nozzle_size').closest('td').find('.nozzle_size_error').text("Enter the nozzle size").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('td').find('.nozzle_size_error').text("").css('color','');
        }
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$('#bit_type').change(function(){
    $(this).css("border-color", "");
    $('.bittype_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#manufacture', function(){
    $(this).css("border-color", "");
    $('.manufacture_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#no_of_nozzle', function(){
    $(this).css("border-color", "");
    $('.nozzle_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.nozzle_size', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.nozzle_size_error').text("").css('color','');
    valid=true;
});

// Bha validations 
$('.bhadata_submit').click(function(event){
    var valid=true;
    count_array = []
    var field_count = 0;
    $(".bhadatarowcls").each(function() {
        
        var type_name = $(this).find('select[name^="type_name"]').val()
        var element = $(this).find('input[name^="element"]').val()
        var od = $(this).find('input[name^="od"]').val()
        var identity = $(this).find('input[name^="identity"]').val()
        var length = $(this).find('input[name^="length"]').val()
        var length_onejoint = $(this).find('input[name^="length_onejoint"]').val()
        console.log('bhadatarowcls',type_name,element,od,identity,length,length_onejoint)
        if(type_name == '' && element == '' && od == '' && identity == '' && length == '' && length_onejoint == '' ){
            field_count=1
        } 
        else {
            
            if(type_name == ''){
             valid = false
                $(this).find('input[name^="type_name"]').css("border-color", "red");
                $(this).find('.type_error').text("Select the Type").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(element == ''){
                valid = false
                $(this).find('input[name^="element"]').css("border-color", "red");
                $(this).find('.element_error').text("Enter the BHA element").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(od == ''){
                valid = false
                $(this).find('input[name^="od"]').css("border-color", "red");
                $(this).find('.od_error').text("Enter the OD").css({'color':'red','float':'left','font-size': '13px'});
            }
            if(type_name != 'Bit'){
                if(identity == ''){
                    valid = false
                    $(this).find('input[name^="identity"]').css("border-color", "red");
                    $(this).find('.identity_error').text("Enter the identity").css({'color':'red','float':'left','font-size': '13px'});
                }
            }

            if(length == ''){
                valid = false
                $(this).find('input[name^="length"]').css("border-color", "red");
                $(this).find('.length_error').text("Enter the length").css({'color':'red','float':'left','font-size': '13px'});
            }
    
            if(length_onejoint == ''){
                valid = false
                $(this).find('input[name^="length_onejoint"]').css("border-color", "red");
                $(this).find('.length_onejoint_error').text("Enter the Cumulative Length").css({'color':'red','float':'left','font-size': '13px'});
            }

        }
         
        });
        console.log(valid)
       
        if(valid == false){
            return false
        }
        else{
            return true
        } 

    // $('select[name^="type_name"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.type_error').text("Select the Type").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.type_error').text("").css('color','');
    //         }
    //     }
    // }) 
    // $('input[name^="element"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.element_error').text("Enter the BHA element").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.element_error').text("").css('color','');
    //         }
    //     }
    // }) 
    // $('input[name^="od"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.od_error').text("Enter the OD").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.od_error').text("").css('color','');
    //         }
    //     }
    // }) 
    // $('input[name^="identity"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).closest('td').find('.first_id').hasClass('first_id')!=true){
    //             if($(this).val()==""){
    //                 $(this).css("border-color", "red");
    //                 $(this).closest('td').find('.identity_error').text("Enter the identity").css({'color':'red','float':'left','font-size': '13px'});
    //                 valid=false;
    //             } else {
    //                 $(this).css("border-color", "");
    //                 $(this).closest('td').find('.identity_error').text("").css('color','');
    //             }
    //         }
    //     }
    // }) 
    // $('input[name^="length"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.length_error').text("Enter the length").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.length_error').text("").css('color','');
    //         }
    //     }
    // }) 
    // $('input[name^="length_onejoint"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'bhadatarow1'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.length_onejoint_error').text("Enter the Cumulative Length").css({'color':'red','float':'left','font-size': '13px'});
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.length_onejoint_error').text("").css('color','');
    //         }
    //     }
    // }) 
    // if(valid==false){
    //     return false;
    // }else{
    //     return true;
    // }
})
$(document).on('change','.type_name', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.type_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.element', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.element_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.od', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.od_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.identity', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.identity_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.length', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.length_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#length_onejoint', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.length_onejoint_error').text("").css('color','');
    valid=true;
});
// Pore pressure anf fracture pressure
$('.pressure_submit').click(function(){
    var valid=true;
    $('input[name^="measured_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'pressurerow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.md_error').text("Enter the MD").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.md_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="true_vertical_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'pressurerow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.tvd_error').text("Enter the TVD").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.tvd_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="pore_pressure"]').each(function(){
        if($(this).closest('tr').attr('id') != 'pressurerow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.pore_pressure_error').text("Enter the Pore pressure").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.pore_pressure_error').text("").css('color','');
            }
        }
            
    })
    $('input[name^="fracture_pressure"]').each(function(){
        if($(this).closest('tr').attr('id') != 'pressurerow2'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.fracture_pressure_error').text("Enter the Fracture pressure").css({'color':'red','float':'left','font-size': '13px'});
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.fracture_pressure_error').text("").css('color','');
            }
        }
            
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
 })
 $(document).on('keyup','#measured_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.md_error').text("").css('color','');
    valid=true;
});
 $(document).on('keyup','#true_vertical_depth', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.tvd_error').text("").css('color','');
    valid=true;
});
 $(document).on('keyup','#pore_pressure', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.pore_pressure_error').text("").css('color','');
    valid=true;
});
 $(document).on('keyup','#fracture_pressure', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.fracture_pressure_error').text("").css('color','');
    valid=true;
});
// Hydraulics validation
$('.hydraulics_submit').click(function(){
    var valid=true;  
    // console.log($(this).closest('div').parent().attr("id") != "new_row")
    $('input[name^="md"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.md_error').text("Enter the MD").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.md_error').text("").css('color','');
        }
        
    })
    $('input[name^="rop"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.rop_error').text("Enter the ROP").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.rop_error').text("").css('color','');
        }
        
    })
    $('input[name^="rpm"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.rpm_error').text("Enter the RPM").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.rpm_error').text("").css('color','');
        }
    
    })
    $('input[name^="flowrate"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.flowrate_error').text("Enter the Flowrate").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.flowrate_error').text("").css('color','');
        }
    
    })
    $('input[name^="pump_pressure"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.pump_pressure_error').text("Enter the Pump pressure").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.pump_pressure_error').text("").css('color','');
        }
        
    })
    $('input[name^="annular_pressure"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.annular_pressure_error').text("Enter the Annular pressure").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.annular_pressure_error').text("").css('color','');
        }
        
    })
    $('input[name^="ecd"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.ecd_error').text("Enter the ECD").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.ecd_error').text("").css('color','');
        }
        
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('blur','.md', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.md_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.flowrate', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.flowrate_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.rop', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.rop_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.rpm', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.rpm_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.pump_pressure', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.pump_pressure_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.annular_pressure', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.annular_pressure_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.ecd', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.ecd_error').text("").css('color','');
    valid=true;
});
// Optimization validation
$('#calculate_optimization').click(function(){
    var valid=true;  
    $('input[name^="original_tfa"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.tfa_error').text("Enter the TFA").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.tfa_error').text("").css('color','');
        }
    })
    $('input[name^="min_flowrate"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.min_flowrate_error').text("Enter the Min Flowrate").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.min_flowrate_error').text("").css('color','');
        }
    })
    $('input[name^="max_flowrate"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.max_flowrate_error').text("Enter the Max Flowrate").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.max_flowrate_error').text("").css('color','');
        }
    })
    $('input[name^="mechanical_efficiency"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.mechanical_efficiency_error').text("Enter the Mechanical Efficiency").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.mechanical_efficiency_error').text("").css('color','');
        }
    })
    $('input[name^="pump_efficiency"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.pump_efficiency_error').text("Enter the Pump Efficiency").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.pump_efficiency_error').text("").css('color','');
        }
    })
    $('input[name^="maximum_pressure"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.maximum_pressure_error').text("Enter the Maximum Pressure").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.maximum_pressure_error').text("").css('color','');
        }
    })
    $('select[name^="liner_size"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.liner_size_error').text("Select the Liner Size").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.liner_size_error').text("").css('color','');
        }
    })
    $('input[name^="liner_length"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.liner_length_error').text("Enter the Liner length").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.liner_length_error').text("").css('color','');
        }
    })
    $('input[name^="pump_spm"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.pump_spm_error').text("Enter the Pump SPM").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.pump_spm_error').text("").css('color','');
        }
    })
    $('input[name^="no_of_nozzle"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.no_on_nozzle_error').text("Enter the number of nozzle").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.no_on_nozzle_error').text("").css('color','');
        }
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('keyup','#original_tfa', function(){
    $(this).css("border-color", "");
    $('.tfa_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#min_flowrate', function(){
    $(this).css("border-color", "");
    $('.min_flowrate_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#max_flowrate', function(){
    $(this).css("border-color", "");
    $('.max_flowrate_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#mechanical_efficiency', function(){
    $(this).css("border-color", "");
    $('.mechanical_efficiency_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#pump_efficiency', function(){
    $(this).css("border-color", "");
    $('.pump_efficiency_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#maximum_pressure', function(){
    $(this).css("border-color", "");
    $('.maximum_pressure_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#liner_size', function(){
    $(this).css("border-color", "");
    $('.liner_size_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#liner_length', function(){
    $(this).css("border-color", "");
    $('.liner_length_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#pump_spm', function(){
    $(this).css("border-color", "");
    $('.pump_spm_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','#no_of_nozzle', function(){
    $(this).css("border-color", "");
    $('.no_on_nozzle_error').text("").css('color','');
    valid=true;
});


// Actual Mud data validation
$('.Actual_muddata_submit').click(function(){
    var valid=true;
    $('input[name^="depth"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('tr').find('.depth_error').text("Enter the Depth").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('tr').find('.depth_error').text("").css('color','');
            }
        }
    })
    $('input[name^="mud_weight"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('tr').find('.mud_weight_error').text("Enter the Mud weight").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('tr').find('.mud_weight_error').text("").css('color','');
            }
        }
    })
    $('select[name^="mudtype"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('tr').find('.mudtype_error').text("Enter the Mud type").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('tr').find('.mudtype_error').text("").css('color','');
            }
        }
    })
    // $('input[name^="plastic_viscosity"]').each(function(){
    //     if($(this).closest('tr').attr('class')!='new-row'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('tr').find('.pv_error').text("Enter the PV").css('color','red').css('float','left');
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('tr').find('.pv_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="yield_point"]').each(function(){
    //     if($(this).closest('tr').attr('class')!='new-row'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('tr').find('.yp_error').text("Enter the YP").css('color','red').css('float','left');
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('tr').find('.yp_error').text("").css('color','');
    //         }
    //     }
    // })
    $('input[name^="low_shear_rate"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('tr').find('.lsryp_error').text("Enter the LSRYP").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('tr').find('.lsryp_error').text("").css('color','');
            }
        }
    })
    
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('keyup','.depth', function(){
    $(this).css("border-color", "");
    $('.depth_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.mud_weight', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.mud_weight_error').text("").css('color','');
    valid=true;
});
$(document).on('change','.mudtype', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.mudtype_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.plastic_viscosity', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.pv_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.yield_point', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.yp_error').text("").css('color','');
    valid=true;
});
$(document).on('keyup','.low_shear_rate', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.lsryp_error').text("").css('color','');
    valid=true;
});

// Actual BHA Validation 
$('.actual_bha_submit').click(function(){
    var valid=true;
    $('input[name^="depth"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('div').find('.depth_error').text("Enter the Depth").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('div').find('.depth_error').text("").css('color','');
            }
        
    })
    $('input[name^="bhaname"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('div').find('.bhaname_error').text("Enter the Bhaname").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('div').find('.bhaname_error').text("").css('color','');
            }
        
    })
    $('select[data-id^="actual_type_name"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
        // console.log('$(this).val()');
                if($(this).val()==""){
                    $(this).css("border-color", "red");
                    $(this).closest('td').find('.type_name_error').text("Enter the Type name").css('color','red').css('float','left');
                    valid=false;
                } else {
                    $(this).css("border-color", "");
                    $(this).closest('td').find('.type_name_error').text("").css('color','');
                }
            }
        }
    })
    $('input[data-id^="actual_element"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
        // console.log('$(this).val()');
                if($(this).val()==""){
                    $(this).css("border-color", "red");
                    $(this).closest('td').find('.element_error').text("Enter the Element").css('color','red').css('float','left');
                    valid=false;
                } else {
                    $(this).css("border-color", "");
                    $(this).closest('td').find('.element_error').text("").css('color','');
                }
            }
        }
    })
    $('input[data-id^="actual_od"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
        // console.log('$(this).val()');
                if($(this).val()==""){
                    $(this).css("border-color", "red");
                    $(this).closest('td').find('.od_error').text("Enter the OD").css('color','red').css('float','left');
                    valid=false;
                } else {
                    $(this).css("border-color", "");
                    $(this).closest('td').find('.od_error').text("").css('color','');
                }
            }
        }
    })
    $('input[data-id^="actual_identity"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
                if($(this).closest('td').find('.first_id').hasClass('first_id')!=true){
        // console.log('$(this).val()');
                    if($(this).val()==""){
                        $(this).css("border-color", "red");
                        $(this).closest('td').find('.identity_error').text("Enter the ID").css('color','red').css('float','left');
                        valid=false;
                    } else {
                        $(this).css("border-color", "");
                        $(this).closest('td').find('.identity_error').text("").css('color','');
                    }
                }
            }
        }
    })
    $('input[data-id^="actual_length"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
        // console.log('$(this).val()');
                if($(this).val()==""){
                    $(this).css("border-color", "red");
                    $(this).closest('td').find('.length_error').text("Enter the Length").css('color','red').css('float','left');
                    valid=false;
                } else {
                    $(this).css("border-color", "");
                    $(this).closest('td').find('.length_error').text("").css('color','');
                }
            }
        }
    })
    $('input[data-id^="actual_length_onejoint"]').each(function(){
        if($(this).closest('tr').attr('class')!='new-row'){
            if($(this).closest('tr').attr('id') != 'bhadatarow1'){
        // console.log('$(this).val()');
                if($(this).val()==""){
                    $(this).css("border-color", "red");
                    $(this).closest('td').find('.length_onejoint_error').text("Enter the Cumulative Length").css('color','red').css('float','left');
                    valid=false;
                } else {
                    $(this).css("border-color", "");
                    $(this).closest('td').find('.length_onejoint_error').text("").css('color','');
                }
            }
        }
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('change','#type_name', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.type_name_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.actual_length', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.length_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','.cumulative-length', function(){
    $(this).css("border-color", "");
    $(this).closest('td').find('.length_onejoint_error').text("").css('color','');
    valid=true;
});

$('.actual_drill_submit').click(function(){
    var valid=true;
    $('input[name^="serial_no"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $('.serial_no_error').text("Enter the Serial No").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.serial_no_error').text("").css('color','');
            }
        
    })
    $('select[data-id^="actual_bit_type"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $('.bit_type_error').text("Enter the Bit type").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.bit_type_error').text("").css('color','');
            }
        
    })
    $('select[data-id^="actual_bhaname"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $('.bhaname_error').text("Enter the BHA").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.bhaname_error').text("").css('color','');
            }
        
    })
    $('input[name^="manufacture"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $(this).closest('div').find('.manufacture_error').text("Enter the Manufacturer").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $(this).closest('div').find('.manufacture_error').text("").css('color','');
        }
    })
    $('input[name^="idac_code"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.idac_code_error').text("Enter the number of IDAC code").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.idac_code_error').text("").css('color','');
        }
    })
    $('input[name^="no_of_nozzle"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.no_of_nozzle_error').text("Enter the number of nozzle").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.no_of_nozzle_error').text("").css('color','');
        }
    })
    $('input[data-id^="actual_nozzle_size"]').each(function(){
        if($(this).val()==""){
            $(this).css("border-color", "red");
            $('.nozzle_size_error').text("Enter the nozzle size").css('color','red').css('float','left');
            valid=false;
        } else {
            $(this).css("border-color", "");
            $('.nozzle_size_error').text("").css('color','');
        }
    })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$(document).on('blur','.serial_no', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.serial_no_error').text("").css('color','');
    valid=true;
});
$(document).on('change','#bit_type', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.bit_type_error').text("").css('color','');
    valid=true;
});
$(document).on('change','#bhaname', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.bhaname_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','#idac_code', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.idac_code_error').text("").css('color','');
    valid=true;
});
$(document).on('blur','#no_of_nozzle', function(){
    $(this).css("border-color", "");
    $(this).closest('div').find('.no_of_nozzle_error').text("").css('color','');
    valid=true;
});

$('.muddata_submit').click(function(){
    var valid=true;
    $('input[name^="section"]').each(function(){
        if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.section_error').text("Enter the Section").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.section_error').text("").css('color','');
            }
        }
        
    })
    $('input[name^="from_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.from_depth_error').text("Enter the from depth").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.from_depth_error').text("").css('color','');
            }
        }
    })
    $('input[name^="to_depth"]').each(function(){
        if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.todepth_error').text("Enter the TO depth").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.todepth_error').text("").css('color','');
            }
        }
    })
    $('input[name^="mud_weight"]').each(function(){
        if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.mud_weight_error').text("Enter the mud weight").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.mud_weight_error').text("").css('color','');
            }
        }
        
    })
    $('select[name^="mudtype"]').each(function(){
        if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $(this).closest('td').find('.mudtype_error').text("Enter the mud type").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $(this).closest('td').find('.mudtype_error').text("").css('color','');
            }
        }
    })
    // $('input[name^="plastic_viscosity"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.pv_error').text("Enter the PV").css('color','red').css('float','left');
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.pv_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="yield_point"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.yp_error').text("Enter the YP").css('color','red').css('float','left');
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.yp_error').text("").css('color','');
    //         }
    //     }
    // })
    // $('input[name^="low_shear_rate"]').each(function(){
    //     if($(this).closest('tr').attr('id') != 'muddatatobeadd'){
    //         if($(this).val()==""){
    //             $(this).css("border-color", "red");
    //             $(this).closest('td').find('.lsryp_error').text("Enter the LSRYP").css('color','red').css('float','left');
    //             valid=false;
    //         } else {
    //             $(this).css("border-color", "");
    //             $(this).closest('td').find('.lsryp_error').text("").css('color','');
    //         }
    //     }
    // })
    if(valid==false){
        return false;
    }else{
        return true;
    }
})
$("form[name='recover_password']").validate({
    rules: {
      email: {
        required: true,
        email: true,
      },
    },
    messages: {
      email:{
        required: "Please provide a email ",
        email: "Please provide a valid email",
      },
    }
})
})