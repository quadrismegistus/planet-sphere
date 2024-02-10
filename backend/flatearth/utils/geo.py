from ..imports import *
from .utils import merge_dicts
from .ip import geo_ip

def geodist(latlon1,latlon2,metric='km'):
    if latlon1==latlon2: return 0
    dist = geodesic(latlon1,latlon2)
    return getattr(dist,metric) if dist else np.nan


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

def random_lat_lon(epsilon=1e-10):
    return (
        random.uniform(-90 + epsilon, 90 - epsilon),
        random.uniform(-180 + epsilon, 180 - epsilon)
    )



@cache
def get_nominatim():
    from geopy.geocoders import Nominatim
    return Nominatim(user_agent='flatearth')



class Geocode:

    @classmethod
    @cache_obj.memoize()
    def decode(self, lat:float, lon:float, lang=DEFAULT_LANG, **kwargs):
        res = self.coder.reverse(
            query=(lat,lon),
            exactly_one=True,
            timeout=30,
            language=lang,
            addressdetails=True,
            namedetails=True,
            **kwargs
        )
        if not res:
            logger.debug('using reverse_geocode')
            resd = reverse_geocode.get((lat,lon))
            city,country = resd.get('city'),resd.get('country')
            if city and country:
                name=f'{city}, {country}'
                res = self.encode(name)
        return res

    
    @classmethod
    @cache_obj.memoize()
    def encode(self, placename:str, lang=DEFAULT_LANG, **kwargs):
        return self.coder.geocode(
            placename,
            exactly_one=True,
            timeout=30,
            language=lang,
            extratags=True,
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
    

    @property
    def loc(self):
        if not self._loc:
            if self._lat!=None and self._lon!=None:
                self._loc = self.decode(
                    self._lat, 
                    self._lon, 
                    lang=self.lang
                )
            elif self._placename:
                self._loc = self.encode(
                    self._placename, 
                    lang=self.lang
                )
            elif self._ip:
                lat,lon = geo_ip(self._ip)
                self._loc = self.decode(lat,lon,lang=self.lang)
            else:
                self._loc = self.decode(0,0,lang=self.lang)
        return self._loc
        
    @property
    def lat(self): 
        return self.loc.latitude if self.loc else self._lat
    @property
    def lon(self):
        return self.loc.longitude if self.loc else self._lon
    @property
    def latlon(self):
        return (self.lat,self.lon)
    
    @property
    def address(self):
        return self.loc.raw.get('address',{}) if self.loc else {}
    @property
    def extratags(self):
        return self.loc.raw.get('extratags',{}) if self.loc else {}
    @property
    def wikidata(self):
        return self.extratags.get('wikidata','') if self.extratags else ''
    @property
    def population(self):
        return int(self.extratags.get('population',0)) if self.extratags else ''
    @property
    def default_lang(self):
        return self.extratags.get('default_language','') if self.extratags else ''
    @property
    def local_name(self):
        return self.name_details.get(
            f'name:{self.default_lang}',
            ''
        ) if self.name_details else ''

    @property
    def city(self):
        return self.address.get('city','') if self.address else ''
    
    @property
    def country(self):
        return self.address.get('country','') if self.address else ''
    
    @property
    def country_code(self):
        return self.address.get('country_code','').upper() if self.address else ''
    
    @property
    def address_type(self):
        return self.loc.raw.get('addresstype','') if self.loc else ''
    
    @property
    def osm_type(self):
        return self.loc.raw.get('osm_type','') if self.loc else ''
    @property
    def osm_id(self):
        return self.loc.raw.get('osm_id','') if self.loc else ''
    @property
    def uri(self):
        if self.osm_type and self.osm_id:
            return f'https://openstreetmap.org/{self.osm_type}/{self.osm_id}'
        return ''

    @property
    def display_name(self):
        return self.loc.raw.get('display_name','') if self.loc else ''
    @property
    def name_details(self):
        return self.loc.raw.get('namedetails',{}) if self.loc else {}
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
            'country',
            'country_code'
        ]
        d = {
            x:self.address.get(x,'')
            for x in keys
        }
        d['country_code'] = d.get('country_code','').upper()
        return d

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
    
    @property
    def safe(self):
        if self._safe: return self
        if not self.name: return self
        geo = Geocode(
            placename=self.name,
            lang=self.lang,
            safe=True
        )
        return geo if geo.loc else self
    
    @property
    def can_be_safe(self, min_dist_km=1):
        if self._safe: return True
        if {self._lat,self._lon} == {None}: return True
        return self.safe_dist_km >= min_dist_km
    
    @property
    def is_safe(self, min_dist_km=1):
        if self._safe: return True
        if {self._lat,self._lon} == {None}: return True
        return self.dist_km >= min_dist_km
    
    @property
    def dist_km(self):
        if None in {self._lat, self._lat}:
            return np.nan
        else:
            dist = self.dist_from(self._lat, self._lon)
            return dist.km
    
    @property
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

    def dist(self, geo, metric='km'):
        return geodist(self.latlon,geo.latlon,metric=metric)

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
            uri=self.uri,
            name=self.name,
            name_local=self.local_name,
            lat=self.lat,
            lon=self.lon,
            **self.name_d,
            wikidata=self.wikidata,
            population=self.population,
            lang_default=self.default_lang,
        )
    
    @property
    def pkl(self):
        # make sure location and safe loc found
        self.loc,self.safe.loc
        return b64encode(pickle.dumps(self))
    @property
    def pkl_s(self):
        return self.pkl.decode('utf-8')
    
    @classmethod
    def from_pkl(self, pkl):
        if type(pkl)==str: pkl=pkl.encode('utf-8')
        return pickle.loads(b64decode(pkl))
    
    @property
    def point_str(self):
        return f'POINT({self.lon} {self.lat})'
    @property
    def point(self):
        from .db import get_point
        return get_point(self.lat, self.lon)
    
    @property
    def country_colors(self):
        return get_country_colors().get(self.country_code,[])
    @property
    def country_color(self,default='#000000'):
        colors = self.country_colors
        return default if not colors else random.choice(colors)


    

@cache
def get_country_colors():
    with open(os.path.join(PATH_REPO_DATA,'national-colors-hex.json')) as f:
        return json.load(f)



glat,glon = 31.5017, 34.4668