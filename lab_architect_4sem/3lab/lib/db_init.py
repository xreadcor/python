from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, Date, Numeric, String
from sqlalchemy_utils import database_exists, create_database

from lib.constants import PG_USER, PG_PASSWD, DB_NAME

metadata = MetaData()


rates = Table('rates', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', Date, unique=True),
    Column('aud_rate', Numeric(8, 3)),
    Column('brl_rate', Numeric(8, 3)),
    Column('bgn_rate', Numeric(8, 3)),
    Column('cad_rate', Numeric(8, 3)),
    Column('cny_rate', Numeric(8, 3)),
    Column('dkk_rate', Numeric(8, 3)),
    Column('eur_rate', Numeric(8, 3)),
    Column('hkd_rate', Numeric(8, 3)),
    Column('huf_rate', Numeric(8, 3)),
    Column('isk_rate', Numeric(8, 3)),
    Column('xdr_rate', Numeric(8, 3)),
    Column('inr_rate', Numeric(8, 3)),
    Column('idr_rate', Numeric(8, 3)),
    Column('ils_rate', Numeric(8, 3)),
    Column('jpy_rate', Numeric(8, 3)),
    Column('myr_rate', Numeric(8, 3)),
    Column('mxn_rate', Numeric(8, 3)),
    Column('nzd_rate', Numeric(8, 3)),
    Column('nok_rate', Numeric(8, 3)),
    Column('php_rate', Numeric(8, 3)),
    Column('pln_rate', Numeric(8, 3)),
    Column('ron_rate', Numeric(8, 3)),
    Column('sgd_rate', Numeric(8, 3)),
    Column('zar_rate', Numeric(8, 3)),
    Column('krw_rate', Numeric(8, 3)),
    Column('sek_rate', Numeric(8, 3)),
    Column('chf_rate', Numeric(8, 3)),
    Column('thb_rate', Numeric(8, 3)),
    Column('try_rate', Numeric(8, 3)),
    Column('gbp_rate', Numeric(8, 3)),
    Column('usd_rate', Numeric(8, 3))
)


amounts = Table('amounts', metadata,
    Column('id', Integer, primary_key=True),
    Column('country', String(20)),
    Column('currency', String(10)),
    Column('amount', Integer),
    Column('code', String(3))
)


def init_db():
    engine = create_engine(f'postgresql+psycopg2://{PG_USER}:{PG_PASSWD}@localhost/{DB_NAME}')
    if not database_exists(engine.url):
        create_database(engine.url)
    metadata.create_all(engine)
    return engine
