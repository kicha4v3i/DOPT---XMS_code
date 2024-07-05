$(document).ready(function() {
    $('#ticket_message').summernote({
        toolbar:false
    })
    $(document).on("click", ".add-btn" , function() {   
       var newrow=$("#append-table tr:first");
       $('#attacment-table').append(newrow.clone())
    });
    $(document).on("click", ".remove-btn" , function() {   
        $(this).closest("tr").remove()
    });

});