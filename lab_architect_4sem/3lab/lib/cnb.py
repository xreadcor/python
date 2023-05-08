from datetime import datetime
import requests

from lib.constants import URL_PATTERN_DAILY
from lib.db import DBInstance


def serialize_rate(rate):
    return float(rate[0])


def serialize_amount(amount):
    return int(amount[0])


class API:
    def __init__(self):
        self.db_instance = DBInstance()

    def fill_amounts(self):
        current_date = datetime.now().date()
        params = {
            'date': current_date
        }
        responce = requests.get(
            URL_PATTERN_DAILY,
            params=params
        )
        data = []
        for line in responce.text.split('\n'):
            if 'Country' in line:
                pass
            elif '|' in line:
                values = line.strip().split('|')[:4]
                amount_list = [values[0], values[1], int(values[2]), values[3].lower()]
                data.append(amount_list)
        self.db_instance.fill_amounts(data)

    def get_currency_info(self, currency, from_date, to_date):
        if from_date > to_date:
            return {
                'error': 'Incorrect time interval'
            }
        rate_list_raw = self.db_instance.get_rates(
            currency,
            from_date.strftime('%d-%m-%Y'),
            to_date.strftime('%d-%m-%Y')
        )
        amount_raw = self.db_instance.get_amount(currency)
        amount = serialize_amount(amount_raw)
        rate_list = [serialize_rate(rate) for rate in rate_list_raw]
        if len(rate_list) == 0:
            return {
                'error': 'No data were found for the specified time interval'
            }
        return {
            'min_rate': min(rate_list) / amount,
            'max_rate': max(rate_list) / amount,
            'avg_rate': round(sum(rate_list) / len(rate_list) / amount, 3)
        }
