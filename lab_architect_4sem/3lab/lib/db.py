from sqlalchemy.sql import text

from lib.db_init import init_db


class DBInstance:
    def __init__(self):
        engine = init_db()
        self.conn = engine.connect()

    def get_rates(self, currency, from_date, to_date):
        query = text(f'SELECT {currency}_rate FROM rates '
                     f'WHERE rates.date BETWEEN :from_date AND :to_date')
        result = self.conn.execute(query, {'from_date': from_date, 'to_date': to_date})
        return result.fetchall()

    def get_amount(self, currency):
        query = text(f'SELECT amount FROM amounts '
                     f'WHERE code = \'{currency}\'')
        result = self.conn.execute(query)
        return result.fetchone()

    def insert_many(self, data):
        query_pattern = 'INSERT INTO rates (date, aud_rate, bgn_rate, brl_rate, cad_rate, chf_rate, cny_rate, ' \
                        'dkk_rate, eur_rate, gbp_rate, hkd_rate, huf_rate, idr_rate, ils_rate, inr_rate, ' \
                        'isk_rate, jpy_rate, krw_rate, mxn_rate, myr_rate, nok_rate, nzd_rate, php_rate, pln_rate, ' \
                        'ron_rate, sek_rate, sgd_rate, thb_rate, try_rate, usd_rate, xdr_rate, zar_rate) ' \
                        'VALUES {values}'
        for line in data:
            query = text(query_pattern.format(values=(*line,)))
            try:
                self.conn.execute(query)
            except:
                continue
        self.conn.commit()

    def insert_one(self, date, values):
        query = text(f'INSERT INTO rates (date, aud_rate, brl_rate, bgn_rate, cad_rate, cny_rate, dkk_rate, '
                     f'eur_rate, hkd_rate, huf_rate, isk_rate, xdr_rate, inr_rate, idr_rate, ils_rate, jpy_rate, '
                     f'myr_rate, mxn_rate, nzd_rate, nok_rate, php_rate, pln_rate, ron_rate, sgd_rate, '
                     f'zar_rate, krw_rate, sek_rate, chf_rate, thb_rate, try_rate, gbp_rate, usd_rate) '
                     f'VALUES {date.strftime("%d.%m.%Y"), *values}')
        try:
            self.conn.execute(query)
        except:
            return
        self.conn.commit()

    def fill_amounts(self, data):
        query_pattern = 'INSERT INTO amounts (country, currency, amount, code)' \
                        'VALUES {values}'
        for line in data:
            query = text(query_pattern.format(values=(*line,)))
            try:
                self.conn.execute(query)
            except:
                continue
        self.conn.commit()
