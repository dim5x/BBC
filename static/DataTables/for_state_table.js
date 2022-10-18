$(document).ready(function () {
    $("#state").DataTable({
        "lengthMenu": [[-1, 10, 20, 30], ['All', 10, 20, 30]],
        "order": [[2, "desc"]]
    });
});
