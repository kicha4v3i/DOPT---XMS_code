
$(document).ready( function () {
   
    $('.enquiry-table').DataTable({
        serverSide: true,
        ajax: {
            url: "/getenquiries",                    
            type: 'GET',
        },

        columns: [
            { data: 'title' },
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            { data: 'message' , className:"enq-msg"},
            {
                data: null,
                render: function (data, type, row) {
                    console.log("data"+data)
                    if(data.form_type=='enterprise'){
                        return '<div class="eye-icon-enq"><a href="/company_signup"><i class="fa-regular fa-eye"></i></a></div>';
                    }else{
                        return '<div class="eye-icon-enq"><a href="/view_enquiries/'+data.id+'"><i class="fa-regular fa-eye"></i></a></div>';
                    }
                }
            }
        ]
    });
 
});