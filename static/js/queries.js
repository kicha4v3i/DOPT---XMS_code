$(document).ready(function() {
    $('.clickable-row').on('click', function() {
        var url = $(this).data('url');
        if (url) {
            window.location.href = url;
        }
    });

    $('#query_list').DataTable({
        
        serverSide: true,
        ajax: {
            url: "/ticket/getalltickets",                    
            type: 'GET',
        },
        language: {
            emptyTable: "---"
        },

        columns: [
            { data: 'sno',className:"common-txt-center" },
            { data: 'title' },
            { data: 'message' ,className:"query-msg-txt"},
            { data: 'status'},
            {
                data: null,
                render: function (data, type, row) {
                    return '<div class="eye-icon-enq"><a href="/ticket/startticket/'+data.id+'"><i class="fa-regular fa-eye"></i></a></div>';
                    
                }
            }
        ]

    });

    $('#poaquery_list').DataTable({
        serverSide: true,
        ajax: {
            url: "/ticket/getallpoatickets",                    
            type: 'GET',
        },
        language: {
            emptyTable: "---"
        },

        columns: [
            { data: 'sno',className: "common-txt-center" },
            { data: 'name' },
            { data: 'designation' },
            { data: 'title' },
            { data: 'message' },
            { data: 'status'},
            {
                data: null,
                render: function (data, type, row) {
                    var actions=''
                    actions +='<div class="icon-container">'
                    actions +='<div class="eye-icon-enq"><a href="/ticket/viewticket/'+data.id+'"><i class="fa-regular fa-eye"></i></a></div>'
                    if(data.is_assigne){
                        actions +='<div class="eye-icon-enq"><a href="/ticket/startticket/'+data.id+'"><i class="fa-regular fa fa-comment"></i></a></div>'
                    }
                    actions +='</div>'
                    return actions
                    
                }
            }
        ]

    });
    $(document).on("click",".assign_users",function(){
        $('#assignuser-modal').modal('show');
    });
  

});