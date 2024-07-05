$(document).ready(function() {
    var subscriber_table = $('.subscriber-table').DataTable({
        searching: false,
        lengthChange: false,
        responsive: true,
        language: {
            emptyTable: "---", 
        },
        drawCallback: function(settings) {
            if (subscriber_table.rows().count() === 0) {
                $('.dataTables_paginate, .dataTables_info').hide();
            } else {
                $('.dataTables_paginate, .dataTables_info').show();
            }
        },

    })
});