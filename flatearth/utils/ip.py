from ..imports import *


@cache
def get_ipinfo_handler():
    handler = ipinfo.getHandler(IPINFO_TOKEN)
    return handler


def get_ipinfo(ip=None):
    if ip in {'127.0.0.1'}: ip = None
    try:
        res = get_ipinfo_handler().getDetails(ip)
        return res.details if res else {}
    except Exception:
        return {}


@cache
def geo_ipinfo(ip=None, hostname_required=True):
    data = get_ipinfo(ip)
    if not hostname_required or data.get('hostname'):
        return {
            'name': data.get('city', ''),
            'country': data.get('country', ''),
            'latitude': float(data.get('latitude', 0)),
            'longitude': float(data.get('longitude', 0)),
        }
    return {}


@cache
def geo_ip(ip=None, hostname_required=True):
    data = geo_ipinfo(ip, hostname_required=hostname_required)
    return data.get('latitude', 0), data.get('longitude', 0)
