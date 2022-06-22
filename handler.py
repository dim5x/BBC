import logging
import os
import subprocess
import sys
import time

import schedule
import yadisk

match sys.platform:
    case 'darwin':
        GET_IPLAYER = r'get_iplayer'
    case 'win32':
        GET_IPLAYER = r'C:\Program Files\get_iplayer\get_iplayer.cmd'

PATH = os.getcwd()
TOKEN = os.environ['TOKEN_BBC']

file_log = logging.FileHandler('bbc.log')
file_log.setLevel(level=logging.INFO)
console_log = logging.StreamHandler()
console_log.setLevel(level=logging.DEBUG)
logging.basicConfig(handlers=(file_log, console_log),
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%d.%m.%Y %I:%M:%S')

logging.info('Start script.')
y = yadisk.YaDisk(token=TOKEN)


def file_exists():
    return 'request.txt' in [i.name for i in y.listdir('/BBC')]


def download():
    logging.info('File exists.')
    y.download('/BBC/request.txt', 'request.txt')
    with open('request.txt', 'r', encoding='utf-8') as f:
        links = [i.strip() for i in f.readlines()]
        logging.info(f'{links}')
    try:
        for link in links:
            logging.info('Start download.')
            res = subprocess.run([GET_IPLAYER, '-o', 'download', link], stdout=subprocess.PIPE)
            logging.debug(f'{res.stdout=}')
            p = str(res.stdout)
            if 'WARNING' in p:
                logging.warning(p)
            if '--pid-recursive' in p:
                res = subprocess.run([GET_IPLAYER, '-o', 'download', '--pid-recursive', link])
                logging.debug(res)
    except Exception as error:
        logging.exception(error)
        pass


def upload():
    y.remove('/BBC/request.txt')
    logging.info('Заявка удалена.')
    for file in os.scandir('download'):
        if file.name.endswith('.m4a'):
            try:
                logging.info(f'Try to upload file {file.name}.')
                y.upload(f'download/{file.name}', f'/BBC/download/{file.name}')
                os.remove(file)
            except ConnectionError as error:
                logging.exception(error)
                pass
            except yadisk.exceptions.PathExistsError as error:
                logging.exception(error)
                pass


def job():
    logging.info('Start job...')
    if file_exists():
        download()
        upload()
    else:
        logging.info('File NOT exists. Stop job.')


schedule.every(1).hours.do(job)
# schedule.every(10).seconds.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
