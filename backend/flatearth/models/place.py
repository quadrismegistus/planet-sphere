from .base import *

class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    name: Mapped[str]
    geopkl: Mapped[bytes]

    def to_dict(self):
        return super().to_dict(
            **self.geo.data
        )
    
    @classmethod
    def from_geo(self, geo):
        return self.locate(geo=geo)

    @classmethod
    def as_row(self, geo):
        return dict(
            point=geo.point_str,
            name=geo.name,
            geopkl=geo.pkl
        )
    
    @classmethod
    def nearby(
            self, 
            lat=None, 
            lon=None, 
            ip=None, 
            placename=None,
            geo=None, 
            maxdist_km=10):
        
        # get location
        if not geo:
            geo = Geocode(
                lat=lat,
                lon=lon,
                ip=ip,
                placename=placename
            )
        # force safe location
        geo = geo.safe

        for place in get_db_session().query(self).order_by(
                func.ST_Distance(
                    self.point,
                    geo.point,
                )):
            dist = place.geo.dist(geo, metric='km')
            if maxdist_km and dist > maxdist_km: break
            yield place, dist

    @classmethod
    @cache
    def locate(
            self, 
            lat=None, 
            lon=None, 
            ip=None, 
            placename=None,
            geo=None, 
            maxdist_km=10):
        
        # get location
        if not geo:
            geo = Geocode(
                lat=lat,
                lon=lon,
                ip=ip,
                placename=placename
            )
        
        # force safe location
        # geo = geo.safe
        
        # find nearby existing locs
        place = self.nearest(geo.lat,geo.lon,maxdist_km=maxdist_km)
        
        # if no place and we have at least a name
        if not place and geo.name:
            # create new place from geo
            place = Place.create(**Place.as_row(geo))
        
        return place
    

    def dist_from(self, lat, lon, metric='km'):
        try:
            dist = geodesic((lat, lon), (self.lat, self.lon))
            return getattr(dist, metric)
        except ValueError as e:
            # print(e)
            return np.nan

    @property
    def lat(self): return self.geo.lat
    @property
    def lon(self): return self.geo.lon

    @cached_property
    def geo(self):
        return Geocode.from_pkl(self.geopkl)

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