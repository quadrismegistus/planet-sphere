from .base import *

class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name: Mapped[str]
    uri: Mapped[Optional[str]]
    # country: Mapped[Optional[str]] = mapped_column(String(2))
    data_json: Mapped[Optional[str]]

    def to_dict(self):
        return super().to_dict(
            **self.data_json_d
        )
    
    @classmethod
    def nearby(cls, lat, lon, ip=None, maxdist_km=None):
        if not lat or not lon: lat,lon=geo_ip(ip)
        if not lat or not lon: lat,lon = NULL_LAT,NULL_LON
        point = get_point(lat, lon)
        for place in get_db_session().query(cls).order_by(
                func.ST_Distance(
                    cls.point,
                    point,
                )):
            dist = place.dist_from(lat, lon)
            if maxdist_km and dist > maxdist_km: break
            yield place, dist

    @classmethod
    @cache
    def locate(self, lat=None, lon=None, ip=None, placename=None, maxdist_km=10):
        geo = Geocode(
            lat=lat,
            lon=lon,
            ip=ip,
            placename=placename
        )
        place = self.nearest(lat,lon,maxdist_km=maxdist_km)
        if not place:
            if not geo.name:
                return
            place = Place.getc(**geo.data_db)
        place._geo = geo
        return place
    

    def dist_from(self, lat, lon, metric='km'):
        try:
            dist = geodesic((lat, lon), (self.lat, self.lon))
            return getattr(dist, metric)
        except ValueError as e:
            # print(e)
            return np.nan

    @cached_property
    def data_json_d(self):
        return json.loads(self.data_json)

    @property
    def lat(self): return self.data_json_d.get('lat')
    @property
    def lon(self): return self.data_json_d.get('lon')
    @property
    def city(self): return self.data_json_d.get('city','')
    @property
    def country(self): return self.data_json_d.get('country','')

    @property
    def geo(self):
        if not hasattr(self,'_geo') or not self._geo:
            self._geo = Geocode(placename=self.name)
        return self._geo

    @cached_property
    def point_str(self):
        return f'POINT({self.lon} {self.lat})'

    def __repr__(self):
        return f'Place(id={self.id}, name="{self.name}")'


@cache
def get_null_place():
    place = Place.get(id=0)
    if not place:
        place = Place(
            id=0,
            point='POINT(0 0)',
            name='Null Island',
            country='XX'
        ).save()
    return place