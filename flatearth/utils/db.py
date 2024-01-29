from ..imports import *


def clear_db(db_url=DB_URL):
    if database_exists(db_url):
        cmd = f"{DB_CMD_PREF} -c 'DROP DATABASE {DB_DATABASE};'"
        os.system(cmd)


@cache
def get_db_engine(clear=DB_CLEAR, db_url=DB_URL):
    if clear: clear_db(db_url)
    if not database_exists(db_url):
        cmd1 = f"{DB_CMD_PREF} -c 'CREATE DATABASE {DB_DATABASE};'"
        cmd2 = f"{DB_CMD_PREF} -d {DB_DATABASE} -c 'CREATE EXTENSION postgis;'"
        os.system(f'{cmd1} && {cmd2}')

    return create_engine(db_url, echo=False)


@cache
def get_db_session():
    return Session(get_db_engine())


def ensure_db_tables(clear=DB_CLEAR):
    from ..models import Base, Place
    if clear: clear_db()
    Base.metadata.create_all(bind=get_db_engine())

    # for table in DB_TABLES:
    # table.ensure_table()


def get_point(lat, lon):
    pointstr = f'POINT({lon} {lat})'
    point = func.Geometry(func.ST_GeographyFromText(pointstr))
    return point
