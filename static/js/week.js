$(function () {
    $("#weekpicker").on("change", function () {
        var selected = $(this).val();
        console.log(selected)

        $.ajax({
            type: 'post', // метод отправки
            url: '/order', // путь к обработчику
            data: {
                // "param1": "Просто текст",
                "week": selected, // переменная со значением из поля с классом email
            },
            dataType: 'text',
        });
    });
})

