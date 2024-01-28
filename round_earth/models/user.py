from .base import *



class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[List['Post']] = relationship(back_populates='user')
    following = relationship(
        'User', 
        secondary=lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers'
    )

    likes: Mapped[List['Post']] = relationship(
        secondary=lambda: post_liking, 
        back_populates="likes"
    )


    @cached_property
    def places(self):
        return {post.place for post in self.posts}

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'
    
    def post(self, txt='', lang='', lat=None, lon=None, ip=None, placename=None, reply_to=None, repost_of=None):
        from .models import Place, Txt, Post
        if not txt and not repost_of: return
        place = Place.loc(lat,lon,ip=ip,placename=placename)
        if place:
            text = Txt.getc(txt=txt, lang=lang)
            post = Post(
                user_id=self.id, 
                place_id=place.id, 
                text_id=text.id,
                timestamp=time.time(),
                replying_to=[reply_to] if reply_to else [],
                reposting=[repost_of] if repost_of else []
            ).save()
            return post
        
    def repost(self, post, txt='', **kwargs):
        post = post.repost_of if post.is_repost and not post.txt else post
        return self.post(repost_of=post, txt=txt, **kwargs)

    def reply(self, post, txt='', **kwargs):
        post = post.repost_of if post.is_repost and not post.txt else post
        return self.post(reply_to=post, txt=txt, **kwargs)


    def follow(self, *users):
        for user in users:
            if not user in set(self.following):
                self.following.append(user)
        self.save()

    def like(self, *posts):
        likes = set(self.likes)
        for post in posts:
            if not post in likes:
                self.likes.append(post)
        self.save()

    @property
    def following_ids(self):
        return {u.id for u in self.following}

    @cached_property
    def feed(self): 
        from .feed import Feed
        return Feed(self)




user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id), primary_key=True)
)
