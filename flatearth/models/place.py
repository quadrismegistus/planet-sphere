from .base import *

class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name: Mapped[str]
    country: Mapped[Optional[str]] = mapped_column(String(2))

    def to_dict(self):
        return super().to_dict(
            name = self.name,
            country = self.country,
            lat = self.lat,
            lon = self.lon
        )
    
    @classmethod
    def nearby(cls, lat, lon, ip=None, mindist_km=None):
        if not lat or not lon: lat,lon=geo_ip(ip)
        if not lat or not lon: lat,lon = NULL_LAT,NULL_LON
        point = get_point(lat, lon)
        for place in get_db_session().query(cls).order_by(
                func.ST_Distance(
                    cls.point,
                    point,
                )):
            dist = place.dist_from(lat, lon)
            if mindist_km and dist > mindist_km: break
            yield place, dist

    @classmethod
    @cache
    def loc(cls, lat=None, lon=None, ip=None, placename=None, mindist_km=10):
        if placename:
            place = Place.get(name=placename)
            if not place:
                geo_d = geocode(placename)
                place = Place.get(name=geo_d['name'])
                if not place:
                    place = Place.getc(**geo_d)
        else:
            if not lat or not lon: lat,lon = geo_ip(ip)
            if not lat or not lon: return get_null_place()
            places = cls.nearest(lat,lon,mindist_km=mindist_km)
            if places: 
                place = places[0][0]
            else:
                place = Place.getc(**geodecode(lat,lon))
        return place
    

    def dist_from(self, lat, lon, metric='km'):
        try:
            dist = geodesic((lon, lat), (self.lon, self.lat))
            return getattr(dist, metric)
        except ValueError as e:
            print(e)
            return np.nan

    @cached_property
    def latlon(self):
        point = wkb.loads(self.point.data.tobytes())
        return (point.y, point.x)

    @property
    def lat(self):
        return self.latlon[0]

    @property
    def lon(self):
        return self.latlon[1]

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