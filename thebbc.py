import hashlib
import os
# import pickle
import time
from flask import Flask, render_template, request, redirect, flash, session
from flask_cors import CORS
import sqlite3
import yadisk

app = Flask(__name__)
app.template_folder = 'template'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # для работы session
CORS(app, supports_credentials=True)

TOKEN = os.environ['TOKEN_BBC']
PASSWORD_HASH = os.environ['PASSWORD_HASH']

y = yadisk.YaDisk(token=TOKEN)
login: str = ''


# with open('desc.pickle', 'rb') as f:
#     d = pickle.load(f)


def convert_bytes(size: int) -> str:
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f'{size:.2f} {x}'
        size /= 1024.0


@app.route('/', methods=['GET', 'POST'])
def login():
    # session.clear()
    global login
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        password_hash = hashlib.sha3_384(bytes(password, encoding='UTF-8')).hexdigest()
        if password_hash == PASSWORD_HASH and login == 'Daisy':
            session[login] = login
            return redirect('/bbc')
        else:
            return redirect('/')
    return render_template('login.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    # rows = []
    global login
    if login in session:
        sqlite_connection = sqlite3.connect('Gbbc.sqlite')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM article WHERE week_number=?"
        cursor.execute(sqlite_select_query, (39,))

        rows = cursor.fetchall()
        # print(rows[11])
        print(rows[0][11])
        print(type(rows[0][11]))
        # print(rows)
        if request.method == 'POST':
            # match request.form.get('button'):
            #     case 'Заказать':
            # print('Заказать')
            # links = request.form['button']
            # print(links)

            print('form', request.form)
            link = request.form.get('link')
            print('link=', link)

            filename = f"{time.strftime('%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(link)
            try:
                y.upload(filename, f'/BBC/{filename}')
                print(f'try {filename}')
            except yadisk.exceptions.PathExistsError as error:
                print(error)
        # print('button=', request.form.get('week'))
        # week = request.form.get('week').split('-')[1]
        # print(f'{week=}')
        # sqlite_connection = sqlite3.connect('Gbbc.sqlite')
        # cursor = sqlite_connection.cursor()
        #
        # sqlite_select_query = "SELECT * FROM article WHERE week_number=?"
        # cursor.execute(sqlite_select_query, (39,))

        # rows = cursor.fetchall()
        # print(rows)
        # print('todo=', request.form.get('todo-form'))
        # print('value=', request.form.get('value'))

        # match request.form.get('todo'):
        #     case 'Заказать':
        #         print(request.data)
        #         todo = request.form.get("button")
        #         print(todo)
        #         print(request.form['button'])
        #         # with open('request.txt', 'w') as f:
        #         #     f.write(links)
        #         filename = f"{time.strftime('%H%M%S')}.txt"
        #         with open(filename, 'w') as f:
        #             f.write(links)
        #         try:
        #             # y.upload(filename, f'/BBC/{filename}')
        #             print(f'try{filename}')
        #         except yadisk.exceptions.PathExistsError as error:
        #             print(error)
        # return redirect(f'/{week}')
        # return render_template('order.html', rows=rows)

        return render_template('order.html', rows=rows)

    return render_template('order.html')


# @app.route("/getandpost", methods=["GET", "POST"])
# # @login_required
# def getandpost():
#     print(request.method)  # получаем ессно, POST
#     if request.method == "POST":
#         print(request.is_json)  # Пишет True - типа полученный ответ и есть Джейсон???
#         print(request.mimetype)  # application/json -
#         print(request.data)  # вот они бинарные данные, например


@app.route('/bbc', methods=['GET', 'POST'])
def hello():
    global login
    if login in session:
        # if True:
        print('Login success.')
        flag = True
        data = []
        if request.method == 'POST':
            match request.form.get('button'):
                case 'Отправить':
                    print('Отправить')
                    links = request.form['text']
                    # with open('request.txt', 'w') as f:
                    #     f.write(links)
                    filename = f"{time.strftime('%H%M%S')}.txt"
                    with open(filename, 'w') as f:
                        f.write(links)
                    try:
                        y.upload(filename, f'/BBC/{filename}')
                    except yadisk.exceptions.PathExistsError as error:
                        print(error)
                        flash('Ресурс "/BBC/request.txt" уже существует. Обратитесь-ка к Дмитричу.')
                        flag = False
                        pass
                    if flag:
                        flash('Заявка отправлена.')
                    return redirect('/bbc')

                case 'Удалить всё':
                    print('Удалить всё.')
                    try:
                        for filename in y.listdir('/BBC/download'):
                            y.remove(f'/BBC/download/{filename.name}')
                            print(f'Файл {filename.name} удалён')
                    except Exception as error:
                        print(error)
                        pass
                    flash(f'Все файлы удалены.')
                    redirect('/bbc')

                case _:
                    print('Удалить.')
                    print(request.form['button'])
                    filename = request.form['button']
                    try:
                        y.remove(f'/BBC/download/{filename}')
                    except Exception as error:
                        print(error)
                        pass
                    flash(f'Файл {filename} удалён.')
                    redirect('/bbc')

        try:
            print('Запрос списка файлов в Яндексе.')
            for i in y.listdir("/BBC/download"):
                d = {'link': fr"{i['file']}",
                     'size': convert_bytes(int(i['size'])),
                     'name': i['name'],
                     'date': i['created'].strftime('%d.%m.%y - %H:%M:%S')}
                data.append(d)
        except Exception as error:
            print(error)
            flash(str(error))
            pass

        return render_template('bbc.html', data=data)

    return """
        <style> * {background: black; text-align:center; color: white;} a {color:blue;}</style>
        <h2>You are not <a href="/">logged in.</a></h2>
        """


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
