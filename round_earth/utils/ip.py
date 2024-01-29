from ..imports import *


@cache
def geo_ipinfo(ip=None):
    import geocoder
    if ip in {'127.0.0.1'}: ip = None
    res = geocoder.ip(ip if ip else 'me')
    return res.json


@cache
def geo_ip(ip=None, hostname_required=True):
    data = geo_ipinfo(ip)
    if not hostname_required or data.get('hostname'):
        return data.get('lat'), data.get('lng')
    return None, None
