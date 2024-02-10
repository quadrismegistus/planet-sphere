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

    timestamp: Mapped[float]

    likes: Mapped[List['User']] = relationship(
        secondary=lambda: post_liking, 
        back_populates="likes"
    )

    # reply_to_id: Mapped[int] = mapped_column(ForeignKey("post.id"),nullable=True)
    # reply_to: Mapped["Post"] = relationship(foreign_keys=[reply_to_id])

    # repost_of_id: Mapped[int] = mapped_column(ForeignKey("post.id"),nullable=True)
    # repost_of: Mapped["Post"] = relationship(foreign_keys=[repost_of_id])

    replying_to = relationship(
        'Post', 
        secondary=lambda: post_replying,
        primaryjoin=lambda: Post.id == post_replying.c.post_id,
        secondaryjoin=lambda: Post.id == post_replying.c.reply_id,
        backref='replies'
    )

    reposting = relationship(
        'Post', 
        secondary=lambda: post_reposting,
        primaryjoin=lambda: Post.id == post_reposting.c.post_id,
        secondaryjoin=lambda: Post.id == post_reposting.c.repost_id,
        backref='reposts'
    )

    @property
    def reply_to(self):
        return first(self.replying_to)
    
    @property
    def repost_of(self):
        return first(self.reposting)
    
    @property
    def is_repost(self):
        return bool(self.repost_of)
    @property
    def is_reply(self):
        return bool(self.reply_to)
    
    @property
    def forward_related_posts(self):
        relposts=set()
        if self.reply_to: 
            relposts|={self.reply_to}|self.reply_to.related_posts
        if self.repost_of:
            relposts|={self.repost_of}|self.repost_of.related_posts
        return relposts
    
    @property
    def backward_related_posts(self):
        relposts=set()
        for reply in self.replies:
            relposts|={reply}|reply.related_posts
        for repost in self.reposts:
            relposts|={repost}|repost.related_posts
        return relposts
    
    @property
    def related_posts(self):
        return self.forward_related_posts

    @property
    def txt(self):
        return self.text.txt

    @property
    def html_tooltip1(post):
        return (
            f'<b>{wrap_html(trunc(post.txt,WRAP_WIDTH))}</b><br>'
            f'&nbsp;<i>—{post.user.name}</i><br><br>'
            f'{wrap_html(post.place.name)}<br>'
            f'{post.ago} '
            f'[id={post.id}]'
        )
    
    @property
    def html_tooltip2(post):
        return (
            f'{post.user.name}<br>'
            f'{wrap_html(post.place.name)}<br>'
            f'{post.ago} '
            f'[id={post.id}]'
        )
    
    @property
    def html_tooltip(post):
        return (
            # f'{post.ago} in '
            f'{post.place.name} '
            f'[id={post.id}]',
        )
    
    @property
    def html(self):
        return f'<h3>{self.user.name} !!</h3><o>{self.txt}</p>'

    def to_dict(self):
        return super().to_dict(
            timestamp=self.timestamp,
            user=self.user,
            text=self.text,
            place=self.place,
            repost_of=self.repost_of,
            reply_to=self.reply_to,
            likes=[u.to_dict() for u in self.likes],
        )
    
    @classmethod
    def iter_latest(cls, limit=10, replies=False, reposts=False, seen:set=None):
        i=0
        for post in get_db_session().query(cls).order_by(-cls.timestamp):
            if (replies or not post.is_reply) and (reposts or not post.is_repost) and (not seen or post.id not in seen):
                yield post
                if seen: seen.add(post.id)
                i+=1
                if i>=limit: break

    
    @classmethod
    def latest(cls, **kwargs):
        return list(cls.iter_latest(**kwargs))
    


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
    id = {self.id}, 
    text = "{self.text.txt}",
    user = {self.user}, 
    place = {self.place})',
    time = {self.datetime}
)'''.strip()
    
    @cached_property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)
    @cached_property
    def ago(self):
        delta=time.time() - self.timestamp
        delta = delta//60*60 if delta>60 else int(delta)
        return f'{format_timespan(delta, max_units=1)} ago'


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


post_reposting = Table(
    'post_reposting', Base.metadata,
    Column('post_id', Integer, ForeignKey(Post.id), primary_key=True),
    Column('repost_id', Integer, ForeignKey(Post.id), primary_key=True)
)


post_replying = Table(
    'post_replying', Base.metadata,
    Column('post_id', Integer, ForeignKey(Post.id), primary_key=True),
    Column('reply_id', Integer, ForeignKey(Post.id), primary_key=True)
)
