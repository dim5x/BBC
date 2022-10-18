$(document).ready(function () {
    $("#log").DataTable({
        // ajax: '/test',
        // columns:[
        //     {data: 'receivedat'},
        //     {data: 'priority'},
        //     {data: 'from_host'},
        //     {data: 'process'},
        //     {data: 'syslog_tag'},
        //     {data: 'mac_type'},
        //     {data: 'message'},
        //     {data: 'mac'},
        // ],
        "lengthMenu": [[10, 20, 30, -1], [10, 20, 30, "All"]],
        "order": [[ 2, "desc" ]]
    });
});
