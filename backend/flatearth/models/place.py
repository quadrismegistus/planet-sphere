from .base import *

class Place(Base):
    __tablename__ = 'place'
    id: Mapped[int] = mapped_column(primary_key=True)
    point = Column(Geometry(geometry_type='POINT', srid=4326))
    lat: Mapped[float]
    lon: Mapped[float]
    name: Mapped[str]
    long_name: Mapped[Optional[str]]
    geonames_id: Mapped[int]
    geonames_json: Mapped[str]

    contained_by = relationship(
        'Place', 
        secondary=lambda: place_contained_by,
        primaryjoin=lambda: Place.id == place_contained_by.c.place_id,
        secondaryjoin=lambda: Place.id == place_contained_by.c.contained_by_id,
        backref='contains'
    )

    @cached_property
    def geonames_data(self):
        return json.loads(self.geonames_json)

    def to_dict(self,is_root=True):
        odx_mine=dict(
            id=self.id,
            lat=self.lat,
            lon=self.lon,
            name=self.name,
            long_name=self.long_name,
            geonames_id = self.geonames_id,
            contained_by=[] if not is_root else [
                place.to_dict(is_root=False)
                for place in self.contained_by
            ] 
        )
        odx = {
            **odx_mine,
            **{k:v for k,v in self.geonames_data.items() if k not in {'geonameId','lng','toponymName'}},
            **odx_mine
        }
        return odx
    
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
            maxdist_km=10):
        
        # get location
        if lat is None or lon is None:
            geo = Geocode(
                lat=lat,
                lon=lon,
                ip=ip,
                placename=placename
            )
            lat,lon = geo.lat,geo.lon

        point = get_point(self.lat, self.lon)

        for place in get_db_session().query(self).order_by(
                func.ST_Distance(
                    self.point,
                    point,
                )):
            dist = geodist(self.latlon, place.latlon, metric='km')
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
            geonames_id=None,
            maxdist_km=10):
        
        if geonames_id: return self.from_geonames(geonames_id)

        # find nearby existing locs
        place = self.nearest(lat=lat, lon=lon, ip=ip, placename=placename, maxdist_km=maxdist_km)
        
        # # if no place and we have at least a name
        # if not place and geo.name:
        #     # create new place from geo
        #     place = Place.create(**Place.as_row(geo))
        
        return place
    
    @classmethod
    def from_geonames(self, id):
        if Place.has(geonames_id=id): return Place.get(geonames_id=id)

        geoname = Geoname(id)
        geonames = [geoname] + [Geoname(loc.geonames_id,loc=loc,tree=geoname.tree[i:]) for i,loc in enumerate(geoname.tree[1:])]
        places = [Place.get(geonames_id=geo.id) if Place.has(geonames_id=geo.id) else Place.create(**geo.to_db()) for geo in geonames]
        for i,place in enumerate(places):
            place.contained_by = places[i+1:]
            place.save()
        return places[0] if places else None

    def dist_from(self, lat, lon, metric='km'):
        try:
            dist = geodesic((lat, lon), (self.lat, self.lon))
            return getattr(dist, metric)
        except ValueError as e:
            return np.nan


    @property
    def latlon(self): return (self.lat,self.lon)

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




place_contained_by = Table(
    'place_contained_by', Base.metadata,
    Column('place_id', Integer, ForeignKey(Place.id), primary_key=True),
    Column('contained_by_id', Integer, ForeignKey(Place.id), primary_key=True)
)