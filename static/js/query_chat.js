$(document).ready(function() {
    var selectedFiles = [];

    $('#ticket_input').summernote({
        toolbar:false
    })


    document.querySelector("#ticketsend-btn").onclick = function (e) {
        console.log(csrf_token)
        var attachments=$('#attachments_hidden').val()
        console.log(attachments)
        console.log(selectedFiles)
        var ticket_input = document.querySelector(
          "#ticket_input"
        ).value;
        var uid=uuidv4()
        var ticket_data= {
            'message': ticket_input,
            'sender':sender,
            'message_id':roomName,
            'recipient':assigne,
            'uid':uid,
            'attachments':attachments
        }

        $.ajax({
            url: '/ticket/sendmessage', 
            type: 'POST',
            headers: { "X-CSRFToken": csrf_token },
            data:  {
                csrfmiddlewaretoken: csrf_token, 
                ticket_data: JSON.stringify(ticket_data)
            },
            dataType: 'json',

            success: function (response) {
                console.log(response)
                messages=response
                var chat_div = document.createElement("div");
                chat_div.className =  messages.sender==sender ? "right_message" : "left_message";
                var html=''
                html +='<p>'+messages.message+'</p>'
                html +='<p>'+moment(new Date()).format("DD-MM-YYYY hh:mm A")+'</p>'
                if(messages.attachments){
                    var attachment=JSON.parse(messages.attachments)
                    $.each(attachment, function(index, element) {
                        var url=download_url.replace('0',element.id)
                        html +='<a href='+url+'>'+element.name+'</a>'
                    });
                }
                $('#ticket_input').summernote('code', '');
                chat_div.innerHTML=html
                $('#query_attachments').val('');
                $('#attachments_hidden').val('')
                document.querySelector("#chat-messages").appendChild(chat_div);
                $('#file_attachments').html('')
                selectedFiles = [];

            },
            error: function (xhr, status, error) {
              
            }
        });
    };

    $('#query_attachments').on('change', function(e) {
        e.stopImmediatePropagation();
        console.log("gfd")
        var file_attachment_html=''
        const files = $(this)[0].files;
        var formData = new FormData();
        var existlength=selectedFiles.length
        console.log("existlength"+existlength)
        for (let i = 0; i < files.length; i++) {
            file_attachment_html +='<div>'
            file_attachment_html +='<p>'+files[i].name+'</p>'
            file_attachment_html +='<button data_index='+existlength+' class="remove_attachments"><i class="fa fa-close close-ichat "></i></button>'
            file_attachment_html +='</div>'
            formData.append('query_attachment_file', files[i]);
            existlength = existlength+1


        }
        $('#file_attachments').append(file_attachment_html)
        $.ajax({
            url: '/ticket/file_upload', 
            type: 'POST',
            headers: { "X-CSRFToken": csrf_token },
            data: formData,
            processData: false, 
            contentType: false, 
            success: function (response) {
                console.log(response.data)
                $('#attachments_hidden').val(JSON.stringify(response.data))
                $.each(response.data, function(index, value) {
                    console.log(value);
                    selectedFiles.push({'id':value.id,'name':value.name})

                });
                console.log(selectedFiles)


            },
            error: function (xhr, status, error) {
              
            }
        });
    });

    $(document).on('click', '.remove_attachments', function(e) {
        e.stopImmediatePropagation();
        var index=$(this).attr('data_index')
        $(this).closest('div').remove();
        var removedElement=selectedFiles.splice(index, 1);
        $('#attachments_hidden').val(JSON.stringify(selectedFiles))

    });
    

});
function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}
function sendmessage(){

}
