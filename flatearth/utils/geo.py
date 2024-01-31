from ..imports import *
from .utils import merge_dicts
from .ip import geo_ip


@cache
def get_geocoder():
    from geopy.geocoders import GoogleV3
    geocoder = GoogleV3(api_key='AIzaSyCgfF7O8nBILgyGcSDlmuhBbHy9vArxTyY')
    return geocoder


def geodecode_offline(lat=None, lon=None, ip=None):
    if not lat or not lon: lat, lon = geo_ip(ip)
    res = reverse_geocode.get((lat, lon))
    return {
        # 'point': f'POINT({lon} {lat})',
        'name': res.get('city', ''),
        'country': res.get('country_code', ''),
        'lat': lat,
        'lon': lon
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


# def geodecode(lat=None, lon=None, ip=None):
#     return merge_dicts(
#         geodecode_offline(lat, lon, ip=ip),
#         geodecode_google(lat, lon, ip=ip),
#     )

def geodecode(lat=None,lon=None,ip=None):
    data = geodecode_offline(lat,lon,ip=ip)
    name = ', '.join(x for x in [data['name'], data['country']] if x)
    loc = geo_loc(name)
    return merge_dicts(data, geo_parse_loc(loc), {'lat_orig':lat, 'lon_orig':lon})
    


@cache
def geo_loc(placename):
    geocoder = get_geocoder()
    loc = geocoder.geocode(placename)
    return loc


def geo_name(placename):
    loc = geo_loc(placename)
    return loc.latitude, loc.longitude


def geocode(placename, with_geodecode=True):
    loc = geo_loc(placename)
    if not loc: return {}
    return merge_dicts(
        geodecode_offline(loc.latitude, loc.longitude) if with_geodecode else {},
        geo_parse_loc(loc),
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
        ok_types={
            'locality', 
            'administrative_area_level_1', 
            'country'
        }
        ok_parts = [d for d in get_parts(loc) if set(d['types']) & ok_types]
        def get_name_d(d):
            if {'locality','country'} & set(d['types']):
                return d['long_name']
            else:
                return d['short_name']
        names = map(get_name_d,ok_parts)
        return ', '.join(n for n in names if n)

    return {
        # 'point': f'POINT({loc.longitude} {loc.latitude})',
        'name': get_name(loc),
        'country': get_country(loc),
        'lat': loc.latitude,
        'lon': loc.longitude
    }

def random_lat_lon():
    return (
        random.uniform(-90, 90),
        random.uniform(-180, 180)
    )



@cache
def get_nominatim():
    from geopy.geocoders import Nominatim
    return Nominatim(user_agent='flatearth')



class Geocode:

    @classmethod
    @cache_obj.memoize()
    def decode(self, lat:float, lon:float, lang=DEFAULT_LANG, **kwargs):
        return self.coder.reverse(
            query=(lat,lon),
            exactly_one=True,
            timeout=30,
            language=lang,
            addressdetails=True,
            namedetails=True,
            **kwargs
        )
    
    @classmethod
    @cache_obj.memoize()
    def encode(self, placename:str, lang=DEFAULT_LANG, **kwargs):
        return self.coder.geocode(
            placename,
            exactly_one=True,
            timeout=30,
            language=lang,
            extratags=False,
            addressdetails=True,
            namedetails=True,
            **kwargs
        )
    
    @classmethod
    @property
    def coder(self): return get_nominatim()
        



    def __init__(self, lat=None, lon=None, ip=None, placename=None,lang=DEFAULT_LANG,safe=False):
        self._lat=lat
        self._lon=lon
        self._placename=placename
        self._ip=ip
        self._loc = None
        self.lang = lang
        self._safe=safe
    

    @cached_property
    def loc(self):
        if not self._loc:
            if self._lat!=None and self._lon!=None:
                self._loc = self.decode(self._lat, self._lon, lang=self.lang)
            elif self._placename:
                self._loc = self.encode(self._placename, lang=self.lang)
            elif self._ip:
                lat,lon = geo_ip(self._ip)
                self._loc = self.decode(lat,lon,lang=self.lang)
            else:
                self._loc = self.decode(0,0,lang=self.lang)
        return self._loc
        
    @property
    def latlon(self):
        return self.loc.latitude, self.loc.longitude
    @property
    def lat(self): return self.latlon[0]
    @property
    def lon(self): return self.latlon[1]

    
    @cached_property
    def address(self):
        return self.loc.raw.get('address',{})
    
    @property
    def city(self):
        return self.address.get('city','')
    
    @property
    def country(self):
        return self.address.get('country','')
    
    @property
    def country_code(self):
        return self.address.get('country_code','')
    
    @property
    def address_type(self):
        return self.loc.raw.get('addresstype','')
    
    @property
    def osm_type(self):
        return self.loc.raw.get('osm_type','')
    @property
    def osm_id(self):
        return self.loc.raw.get('osm_id','')
    @property
    def osm_uri(self):
        if self.osm_type and self.osm_id:
            return f'https://openstreetmap.org/{self.osm_type}/{self.osm_id}'

    @property
    def display_name(self):
        return self.loc.raw.get('display_name','')
    @cached_property
    def name_details(self):
        return self.loc.raw.get('namedetails',{})
    @property
    def name_d(self):
        keys = [
            'neighbourhood',
            'suburb',
            'city',
            'state_district',
            'county',
            'state',
            'region',
            'country'
        ]
        return {
            x:self.address.get(x,'')
            for x in keys
        }

    @property
    def name(self):
        keys = {
            'city',
            'state_district',
            'state',
            'region',
            'country'
        }
        names = [v for k,v in self.name_d.items() if v and k in keys]
        if names: 
            return ', '.join(names)
        if 'int_name' in self.name_details:
            return self.name_details['int_name']
        return self.display_name
    
    @cached_property
    def safe(self):
        if self._safe: return self
        return Geocode(
            placename=self.name,
            lang=self.lang,
            safe=True
        )
    
    @cached_property
    def can_be_safe(self, min_dist_km=1):
        if self._safe: return True
        if {self._lat,self._lon} == {None}: return True
        return self.safe_dist_km >= min_dist_km
    
    @cached_property
    def is_safe(self, min_dist_km=1):
        if self._safe: return True
        if {self._lat,self._lon} == {None}: return True
        return self.dist_km >= min_dist_km
    
    @cached_property
    def dist_km(self):
        if None in {self._lat, self._lat}:
            return np.nan
        else:
            dist = self.dist_from(self._lat, self._lon)
            return dist.km
    
    @cached_property
    def safe_dist_km(self):
        if None in {self._lat, self._lat}:
            return np.nan
        else:
            dist = self.dist_from(
                self._lat, 
                self._lon,
                self.safe.lat,
                self.safe.lon
            )
            return dist.km


    def dist_from(self, lat, lon, lat2=None, lon2=None):
        dist = geodesic(
            (lat, lon), 
            (
                self.lat if lat2 is None else lat2,
                self.lon if lon2 is None else lon2
            )
        )
        return dist

    @property
    def data(self):
        return dict(
            uri=self.osm_uri,
            name=self.name,
            lat=self.lat,
            lon=self.lon,
            **self.name_d
        )
    





glat,glon = 31.5017, 34.4668