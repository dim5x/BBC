//Ajax запрос при нажатии кнопки Заказать
$(document).on("click", "#send", function () {
    // var param = $(".bbc_link").val();
    let link = $(this).attr('value');
    console.log(link);
    $.ajax({
        type: 'POST', // метод отправки
        // по умолчанию считает что обработчик на той же странице
        // удобно, если ссылка на страницу динамически меняется.
        // url: '/order', // путь к обработчику
        data: {
            // "param1": "Просто текст",
            "link": link, // переменная со значением из поля с классом email
        },
        dataType: 'text',
        // success: function (data) {
        //     $(".answer").html(data); // при успешном получении ответа от сервера, заносим полученные данные в элемент с классом answer
        // },
        // error: function (data) {
        //     console.log(data); // выводим ошибку в консоль
        // }
    });
    this.setAttribute('disabled', true);
    // this.textContent='✓';
    this.textContent = 'v';
    this.style.color = 'green';
    this.style.borderColor = 'black';
    return false;
})

//Поиск в таблице по нажатию на тэг.
$(document).on("click", ".tag", function () {
    let genre = $(this).attr('value');
    let table = $('#state').DataTable();
    table.search(genre).draw();
});