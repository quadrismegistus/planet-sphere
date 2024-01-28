from .base import *

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[List['Post']] = relationship(back_populates='user')
    followers: Mapped[List["Following"]] = relationship(back_populates="followed")
    followeds: Mapped[List["Following"]] = relationship(back_populates="follower")


    @cached_property
    def places(self):
        return {post.place for post in self.posts}

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'
    
    def post(self, txt, lang='', lat=None, lon=None, ip=None, placename=None):
        from .models import Place, Txt, Post
        if not txt: return
        place = Place.located_at(lat,lon,ip=ip,placename=placename)
        if place:
            text = Txt.get_or_create(txt=txt, lang=lang)
            post = Post(user_id=self.id, place_id=place.id, text_id=text.id).save()
            return post


class Following(Base):
    __tablename__ = "follows"

    source_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    target_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[float]

    # association between Assocation -> Child
    follower: Mapped["User"] = relationship(back_populates="followeds")

    # association between Assocation -> Parent
    followed: Mapped["User"] = relationship(back_populates="followers")