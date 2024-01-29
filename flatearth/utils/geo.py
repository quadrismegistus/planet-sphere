from ..imports import *
from .utils import merge_dicts
from .ip import geo_ip


@cache
def get_geocoder():
    from geopy.geocoders import GoogleV3
    geocoder = GoogleV3(api_key='AIzaSyCgfF7O8nBILgyGcSDlmuhBbHy9vArxTyY')
    return geocoder


def geodecode_offline(lat=None, lon=None, ip=None):
    import reverse_geocode
    if not lat or not lon: lat, lon = geo_ip(ip)
    res = reverse_geocode.get((lat, lon))
    return {
        'point': f'POINT({lon} {lat})',
        'name': res.get('city', ''),
        'country': res.get('country_code', ''),
    }


def geodecode_google_loc(lat=None, lon=None, ip=None):
    if not lat or not lon: lat, lon = geo_ip(ip)
    if not lat or not lon: return
    geocoder = get_geocoder()
    loc = geocoder.reverse((lat, lon))
    return loc


def geodecode_google(lat=None, lon=None, ip=None):
    loc = geodecode_google_loc(lat, lon, ip=ip)
    return geo_parse_loc(loc) if loc else {}


def geodecode(lat=None, lon=None, ip=None):
    return merge_dicts(
        geodecode_offline(lat, lon, ip=ip),
        geodecode_google(lat, lon, ip=ip),
    )


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
    if not loc: return {}
    return merge_dicts(
        geodecode_offline(loc.latitude, loc.longitude),
        geo_parse_loc(loc, with_geodecode=True),
    )


def geo_parse_loc(loc, with_geodecode=False):

    def get_parts(loc):
        return loc.raw.get('address_components', [])

    def get_country(loc):
        for d in get_parts(loc):
            if 'country' in set(d['types']):
                return d['short_name']
        return ''

    def get_name(loc):
        return ', '.join(
            d['long_name'] for d in get_parts(loc)
            if ({'locality', 'administrative_area_level_1', 'country'}
                & set(d['types']) and d['long_name']
                and d['long_name'][0].isalpha()))

    return {
        'point': f'POINT({loc.longitude} {loc.latitude})',
        'name': get_name(loc),
        'country': get_country(loc)
    }
