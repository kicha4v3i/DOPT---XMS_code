$(document).ready(function() {
    var csrf =$('.getcsrf').val();
    var pump_manufacture_id=$('#manumaster').val()
    var pump_name=$('#pump_name').val()

    $( "#manumaster" ).change(function() {
        var pump_manufacture_id=$(this).val()
        $('#stroke_length').val('');
        $("#pump_type").val('');
        $("input[name=linear_size]").val('');
        $("input[name=max_discharge_pressure]").val('');
        getmudpumps(pump_manufacture_id,csrf)


    });


    function getmudpumps(pump_manufacture_id,csrf){
        $.ajax({
            type: "GET",
            url:"/wells/mud/getpumps",
            contentType: 'application/json',  
            data: {'pump_manufacturer_id':pump_manufacture_id},
            dataType: "json",
            beforeSend: function(xhr){
                xhr.setRequestHeader('X-CSRFToken', csrf);
            },
            success: function(data) {
                $('#pump_name_select').empty();
                $('#pump_name_select').append($("<option></option>").attr("value", '').text("Select Pump Name")); 
                $.each(JSON.parse(data), function(key, value) {
                    $('#pump_name_select').append($("<option></option>").attr("value", value.pk).text(value.fields.name)); 
                });
            }
        });
    }
})



