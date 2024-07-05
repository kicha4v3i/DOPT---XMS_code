$(document).ready( function () {
    $('#individual-table').DataTable({
        serverSide: true,
        ajax: {
            url: "/getindividuals/",  
            type: 'GET'
        },
        columns: [
            { data: 'first_name' },
            { data: 'last_name' },
            { data: 'email' },
            {
                data: null,
                render: function(data, type, row) {
                    
                    
                    return '<div class="common-txt-center"><a href="/company/views/' + data.id + '/Individual"><i class="fa fa-eye"></i></a></div>';

                }
            }
        ]

    });

    $('#company-table').DataTable({
        serverSide: true,
        ajax: {
            url: "/getcompanies/CompanyPlan",  
            type: 'GET'
        },
        cache:false,
        columns: [
            { data: 'company_name' },
            { data: 'email' },
            { data: 'no_of_users',className:"common-txt-center" },
            { data: 'subscription_type' },
            {
                data: null,
                render: function(data, type, row) {
                    console.log('data',data)
                    return '<a href="/company/views/' + data.id + '/CompanyPlan"><i class="fa fa-eye"></i></a>';

                }
            }


        ]

    });

    $('#enterprise-table').DataTable({
        serverSide: true,
        ajax: {
            url: "/getcompanies/Enterprise",  
            type: 'GET'
        },
        cache:false,
        columns: [
            { data: 'company_name' },
            { data: 'email' },
            { data: 'no_of_users', className:"common-txt-center"},
            { data: 'subscription_type' },
            {
                data: null,
                render: function(data, type, row) {
                    console.log('data',data)
                    return '<a href="/company/views/' + data.id + '/Enterprise"><i class="fa fa-eye"></i></a>';

                }
            }


        ]

    });

});