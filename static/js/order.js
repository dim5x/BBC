// function get_len() {
//             $.ajax({
//                 type: "POST",
//                 url: "/",
//                 data: $('button').serialize(),
//                 success: function(response) {
//                     var json = jQuery.parseJSON(response)
//                     $('#len').html(json.len)
//                     // console.log(response);
//                 },
//                 error: function(error) {
//                     console.log(error);
//                 }
//             });
//         }

// document.addEventListener('DOMContentLoaded', function(){
//   document.getElementById('submit').addEventListener('click', do_request);
// });
//
// function do_request() {
//   axios.post('http://127.0.0.1:5000/getandpost', {
//     test1: document.querySelector('#test1').value,
//     // test2: document.querySelector('#test2').value,
//     // test3: document.querySelector('#test3').value
//   })
//   .catch(err => console.error(err));
// }


// $("#changeform").on("click", function () {
//     $.ajax({
//         url: '/getandpost',
//         method: 'post',
//         dataType: 'json',
//         contentType: 'application/json',
//         data: $("#changeform").serialize(),
//         success: function (data) {
//             $('#message').html(data);
//         }
//     });
// });
// $(document).click('submit', '#todo-form', function (e) {
//     console.log('hello');
//     e.preventDefault();
//     var thisForm = this;
//     console.log(thisForm);
//     $.ajax({
//         type: 'POST',
//         url: '/',
//         // data: {todo: $("#todo").val()},
//         data: {todo: thisForm},
//
//
//     })
//     ;
// });

$(document).on("click", "#send", function () {
    // var param = $(".bbc_link").val();
    var link = $(this).attr('value');
    console.log(link);
    $.ajax({
        type: 'POST', // метод отправки
        url: '/order', // путь к обработчику
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
    this.setAttribute('disabled', true)
    this.textContent='Ok'
    return false;
})