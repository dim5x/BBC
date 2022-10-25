$(document).ready(function () {
    $("#state").DataTable({
        "lengthMenu": [[10, 20, 30, -1], [10, 20, 30, 'All']],
        // "order": [[3, "asc"]],
        // columns: [
        //         {title: "Картинка"},
        //         {title: "Название"},
        //         {title: "Описание"},
        //         {title: "Duration", type: 'num'},// магия здесь!
        //         {title: "Жанр"},
        //         {title: ""},
        //     ],
    });

});
