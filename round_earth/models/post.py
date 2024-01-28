from .base import *

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates='posts',
                                        foreign_keys=[user_id])

    place_id: Mapped[int] = mapped_column(ForeignKey("place.id"))
    place: Mapped["Place"] = relationship(foreign_keys=[place_id])

    text_id: Mapped[int] = mapped_column(ForeignKey("text.id"))
    text: Mapped["Txt"] = relationship(foreign_keys=[text_id])

    
    
    


    @classmethod
    def nearby(cls, lat=None, lon=None, ip=None, mindist_km=None):
        from .models import Place
        if not lat or not lon: lat,lon=geo_ip(ip)
        if not lat or not lon: return
        point = get_point(lat, lon)
        for post in get_db_session().query(cls).join(Place).order_by(
                func.ST_Distance(
                    Place.point,
                    point,
                )):
            dist = post.place.dist_from(lat, lon)
            if mindist_km and dist > mindist_km: break
            yield post, dist

    

    def __repr__(self):
        return f'''
Post(
    id={self.id}, 
    text="{self.text.txt}",
    user={self.user}, 
    place={self.place})'
)'''.strip()
    
    def translate_to(self, lang):
        tr = self.text.translate_to(lang)
        tr.post = self
        return tr
    
    @property
    def translations(self):
        l = []
        for tr in self.text.translations:
            tr.post = self
            l.append(tr)
        return l

