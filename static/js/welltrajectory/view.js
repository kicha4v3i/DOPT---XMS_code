

$(document).ready( function () {
   
    $('.trajectory_table').DataTable({
        serverSide: true,
        ajax: {
            url: "/wells/welltrajectory/gettrajectory",                    
            type: 'GET',
            data:{
                well_id : well_id
            },
        },

        columns: [
            { data: 'md',className:"common-txt-center"},
            { data: 'lnclination',className:"common-txt-center" },
            { data: 'azimuth',className:"common-txt-center" },
            { data: 'tvd',className:"common-txt-center" },
            { data: 'dls' ,className:"common-txt-center"},
            { data: 'vertical_section',className:"common-txt-center"},
        ]

    });
});