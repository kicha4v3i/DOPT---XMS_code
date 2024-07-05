$(document).ready( function () {
    var notification_table=$('#notify-table').DataTable({
        serverSide: true,
        searching: false,
        ajax: {
            url: '/projects/notifications_datatable',                    
            type: 'GET'
        },
        columns: [
            { data: 'data1' },
            { data: 'data2' },
        ],
    });
    $('#notify-table tbody').on('click', 'tr', function () {
        var rowData = notification_table.row(this).data();
        if (rowData && rowData.url) {
            window.location.href = rowData.url + '?msgid=' + rowData.id; 
        }
    });
});