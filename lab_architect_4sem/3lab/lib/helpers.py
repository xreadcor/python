from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import time

from lib.constants import URL_PATTERN_DAILY, URL_PATTERN_YEAR
from lib.db import DBInstance


def fill_db(year):
    params = {
        'year': year
    }
    responce = requests.get(
        URL_PATTERN_YEAR,
        params=params
    )
    data = []
    ignored_currencies = {'rub', 'hrk'}
    ignored_indexes = set()
    for ind_, head in enumerate(responce.text.split('\n')[0].split('|')[1:]):
        if head[-3:].lower() in ignored_currencies:
            ignored_indexes.add(ind_)
    for line in responce.text.split('\n'):
        if not line or line.startswith('Date'):
            continue
        line = line.split('|')
        date = line[0]
        values = [float(val) for ind, val in enumerate(line[1:]) if ind not in ignored_indexes]
        data.append((date, *values))
    db = DBInstance()
    db.insert_many(data)


def fill_day():
    current_date = datetime.now().date()
    params = {
        'date': current_date
    }
    responce = requests.get(
        URL_PATTERN_DAILY,
        params=params
    )
    data = []
    rateindex = 4
    for line in responce.text.split('\n'):
        if 'Rate' in line:
            headers = line.strip().split('|')
            rateindex = headers.index('Rate')
        elif "|" in line:
            values = line.strip().split('|')
            rate = float(values[rateindex])
            data.append(rate)
    db = DBInstance()
    db.insert_one(current_date, data)


def schedule_task(interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(fill_day, 'interval', days=interval)
    scheduler.start()
    try:
        while True:
            time.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
