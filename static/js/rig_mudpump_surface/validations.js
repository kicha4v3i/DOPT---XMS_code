$(document).ready(function() {
    $('.mudpump_submit').click(function(){
        var valid=true;
        var pump_manufacture=$('#manumaster').val()
       
        if(pump_manufacture==""){
            $(this).css("border-color", "red");
            $('.pump_manufacturer_error').text("Enter the Pump Manufacturer").css('color','red').css('float','left');
            valid=false; 
        }else{
            $(this).css("border-color", "");
            $('.pump_manufacturer_error').text("").css('color','');
        }

        $('input[name^="pump_name_select"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $('.pump_name_error').text("Enter the Pump name").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.pump_name_error').text("").css('color','');
            }
        })
        $('input[name^="pump_type"]').each(function(){
            if($(this).val()==""){
                $(this).css("border-color", "red");
                $('.pump_type_error').text("Enter the Pump type").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.pump_type_error').text("").css('color','');
            }
        })
        $('input[name^="stroke_length"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $('.stoke_length_error').text("Enter the stoke length").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.stoke_length_error').text("").css('color','');
            }
        });
        $('input[name^="number_of_pumps"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $('.no_of_pump_error').text("Enter the number of pump").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.no_of_pump_error').text("").css('color','');
            }
        });
        $('input[name^="linear_size"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $(this).closest('td').find('.linersize_error').text("Enter the linersize").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.linersize_error').text("").css('color','');
            }
        });
        $('input[name^="max_discharge_pressure"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $(this).closest('td').find('.max_discharge_error').text("Enter the max discharge").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.max_discharge_error').text("").css('color','');
            }
        });
        $('input[name^="pump_speed"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $(this).closest('tr').find('.pump_speed_error').text("Enter the pump speed").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.pump_speed_error').text("").css('color','');
            }
        });
        $('input[name^="flowrate"]').each(function(){
            if ($(this).val() == "") {
                $(this).css("border-color", "red");
                $('.flowrate_error').text("Enter the flowrate").css('color','red').css('float','left');
                valid=false;
            } else {
                $(this).css("border-color", "");
                $('.flowrate_error').text("").css('color','');
            }
        });
        if(valid==false){
            return false;
        }else{
            return true;
        }
    })
})