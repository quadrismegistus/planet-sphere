from .imports import *


def run():
    cmd = f'( cd "{PATH_REPO}" && uvicorn round_earth:app --reload )'
    os.system(cmd)


def get_spatialite_path():
    for path in PATHS_SPATIALITE:
        if os.path.exists(path):
            return path

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


def get_point(lat, lon):
    pointstr = f'POINT({lon} {lat})'
    point = func.Geometry(func.ST_GeographyFromText(pointstr))
    return point


def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    return result


def geodecode(lat=None, lon=None):
    import reverse_geocode
    if not lat or not lon: lat,lon = geo_ip()
    res = reverse_geocode.get((lat, lon))
    return {
        'point': f'POINT({lon} {lat})',
        'name': res.get('city', ''),
        'country': res.get('country_code', ''),
    }

@cache
def get_geocoder():
    from geopy.geocoders import GoogleV3
    geocoder = GoogleV3(api_key='AIzaSyCgfF7O8nBILgyGcSDlmuhBbHy9vArxTyY')
    return geocoder

@cache
def geo_ipinfo(ip=None):
    import geocoder
    res = geocoder.ip(ip if ip else 'me')
    return res.json

def geo_ip(ip=None, hostname_required=True):
    data = geo_ipinfo(ip)
    if not hostname_required or data.get('hostname'):
        return data.get('lat'),data.get('lng')
    return None,None

def geodecode_google(lat=None, lon=None):
    if not lat or not lon: lat,lon=geo_ip()
    if not lat or not lon: return
    geocoder = get_geocoder()
    res = geocoder.reverse((lat,lon))
    return res.raw
    return {
        'city': res.get('city', ''),
        'country': res.get('country_code', ''),
    }

@cache
def geo_loc(placename):
    geocoder = get_geocoder()
    loc = geocoder.geocode(placename)
    return loc

def geo_name(placename):
    loc = geo_loc(placename)
    return loc.latitude, loc.longitude

def geocode(placename):
    loc = geo_loc(placename)
    if not loc: return

    def get_parts(loc):
        return loc.raw.get('address_components',[])
    def get_country(loc):
        for d in get_parts(loc):
            if 'country' in set(d['types']):
                return d['short_name']
        return ''
    def get_name(loc):
        return ', '.join(d['long_name'] for d in get_parts(loc) if d['long_name'] and d['long_name'][0].isalpha())

    country = get_country(loc)
    name = get_name(loc)
    odx={**geodecode(loc.latitude, loc.longitude)}
    if name: odx['name']=name
    if country: odx['country']=country
    return odx




def ensure_db_tables(clear=DB_CLEAR):
    from .models import DB_TABLES
    if clear: clear_db()
    for table in DB_TABLES:
        table.ensure_table()
