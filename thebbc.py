from datetime import datetime, timedelta
import hashlib
import os
import sqlite3
import time

from flask import Flask, render_template, request, redirect, flash, session
from flask_cors import CORS

import psycopg2
import yadisk

app = Flask(__name__)
app.template_folder = 'template'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # для работы session
CORS(app, supports_credentials=True)

TOKEN = os.environ['TOKEN_BBC']
PASSWORD_HASH = os.environ['PASSWORD_HASH']

DATABASE_URL = os.environ['DATABASE_URL']

y = yadisk.YaDisk(token=TOKEN)
login: str = ''

GO_TO_LOGIN = """
        <style> * {background: black; text-align:center; color: white;} a {color:blue;}</style>
        <h2>You are not <a href="/">logged in.</a></h2>
        """


# TODO jinja: filesizeformat(value, binary=False):
# Фильтр filesizeformat() форматирует значение как удобочитаемый размер файла (например, 13 KB; 4,1 MB; 102 bytes и т. д.).
#
# По умолчанию используются десятичные префиксы (Mega, Giga и т. д.), Если второй параметр имеет значение True, используются двоичные префиксы (Mebi, Gibi).

def convert_bytes(size: int) -> str:
    ''' Человекочитаемая конвертация байт. '''
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f'{size:.2f} {x}'
        size /= 1024.0


def weeknum_to_dates(WEEK):
    YEAR = 2022
    return [datetime.strptime(f'{YEAR}-{WEEK}-{DAY}', "%Y-%W-%w").strftime(' %d ') for DAY in (1, 2, 3, 4, 5, 6, 0)]


@app.context_processor
def wrapper():
    '''
    Размещение в шаблонизаторе Jinja своей функции в {{ }},
    которая переводит секунды в человекочитаемый формат.
    '''

    def convert(seconds=0):
        _, _, _, h, m, *_ = list(time.gmtime(seconds))
        h = f'{h} hours' if h else ''
        m = f'{m} minutes' if m else ''
        return f'{h} {m}'

    return dict(convert=convert)


@app.route('/', methods=['GET', 'POST'])
def login():
    # session.clear()
    global login
    session.permanent = True
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


@app.route('/bbc', methods=['GET', 'POST'])
def bbc():
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
                     'date': i['created'].strftime('%d.%m.%y - %H:%M:%S'),
                     'timestamp': datetime.timestamp(i['created'])}
                data.append(d)
        except Exception as error:
            print(error)
            flash(str(error))
            pass

        return render_template('bbc.html', data=data)

    return GO_TO_LOGIN


@app.route('/order_choice', methods=['GET', 'POST'])
def order_choice():
    global login
    if login in session:
        current_week = int(datetime.today().strftime("%U"))

        # SQLITE3
        # sqlite_connection = sqlite3.connect('Gbase.sqlite')
        # cursor = sqlite_connection.cursor()

        # Local Postgres
        # postgres_connection = psycopg2.connect(dbname='postgres', user='postgres',
        #                                        password='Poiq701384', host='localhost')
        # cursor = postgres_connection.cursor()

        # HEROKU
        heroku_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = heroku_connection.cursor()

        sql = "SELECT DISTINCT week_number FROM article"
        cursor.execute(sql)

        l = cursor.fetchall()
        # print(l)

        week_list = sorted([i[0] for i in l])
        # print(week_list)

        days = {i: ' '.join(weeknum_to_dates(i)) for i in week_list}

        return render_template('order_choice.html', week_list=week_list, current_week=current_week, days=days)
    return GO_TO_LOGIN


@app.route('/week/<int:week_id>', methods=['GET', 'POST'])
def order(week_id):
    global login
    rows = []
    if login in session:

        # SQLITE3
        # sqlite_connection = sqlite3.connect('Gbase.sqlite')
        # cursor = sqlite_connection.cursor()
        # sqlite_select_query = "SELECT * FROM article WHERE week_number=? ORDER BY title, subtitle"
        # cursor.execute(sqlite_select_query, (week_id,))

        # LocalPostgres
        # postgres_connection = psycopg2.connect(dbname='postgres',
        #                                        user='postgres',
        #                                        password='Poiq701384',
        #                                        host='localhost')
        # cursor = postgres_connection.cursor()

        # Heroku
        heroku_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = heroku_connection.cursor()

        sqlite_select_query = "SELECT * FROM article WHERE week_number=%s ORDER BY title, subtitle"
        cursor.execute(sqlite_select_query, (week_id,))
        for row in cursor.fetchall():
            d = {'title': row[0],
                 'subtitle': row[1],
                 'medium_synopsis': row[2],
                 'long_synopsis': row[3],
                 'series': row[4],
                 'episode_position': row[5],
                 'episode_count': row[6],
                 'duration': row[7],
                 'genre': row[8].split('\n'),
                 'genre_id1': row[9],
                 'genre_id2': row[10],
                 'genre_id3': row[11],
                 'genre_id4': row[12],
                 'genre_id5': row[13],
                 'img_id': row[14],
                 'image': row[15],
                 'url_id': row[16],
                 'week_number': row[17],
                 'downloaded': row[18],
                 }
            rows.append(d)
            # print(rows[0]['genre'])
        if request.method == 'POST':

            print('form', request.form)
            link = request.form.get('link')
            print('link=', link)

            sqlite_update_query = """UPDATE article SET downloaded = %s where url_id = %s"""
            value = (1, link)
            cursor.execute(sqlite_update_query, value)
            # sqlite_connection.commit()
            # sqlite_connection.close()
            # postgres_connection.commit()
            heroku_connection.commit()
            # postgres_connection.close()

            # filename = f"{time.strftime('%H%M%S')}.txt"
            filename = link + '.txt'
            with open(filename, 'w') as f:
                f.write(link)
            try:
                y.upload(filename, f'/BBC/{filename}')
                print(f'try {filename}')
            except yadisk.exceptions.PathExistsError as error:
                print(error)

        return render_template('order.html', rows=rows)

    # return render_template('order.html')
    return GO_TO_LOGIN


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
