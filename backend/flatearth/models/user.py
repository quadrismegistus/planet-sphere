from .base import *

class UserError(Exception): pass
class UserNotExist(UserError): pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    passhash: Mapped[bytes]
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

    @classmethod
    def register(self, name:str, password:str):
        if not name or len(name)<MIN_USERNAME_LEN:
            raise UserError('no or too short username given')
        
        # no password
        if not password:
            raise UserError('no password given')

        # name exists?
        if self.has(name=name):
            raise UserError('user already exists')

        # create
        return self.create(
            name=name,
            passhash=hash_password(password)
        )
    
    @classmethod
    def login(self, name:str, password:str):
        # valid input?
        if not name or not password:
            raise UserError('name and pw not given')
        
        # name exists?
        user = self.get(name=name)
        if not user:
            logger.error('user not exist')
            raise UserNotExist('user does not exist')
        
        # password ok?
        if not check_password(password, user.passhash):
            logger.error('pw no match')
            raise UserError('password not matching')

        return user

        
        



    @cached_property
    def places(self):
        return {post.place for post in self.posts}

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'
    
    def post(self, txt='', lang='', lat=None, lon=None, ip=None, placename=None, reply_to=None, repost_of=None):
        from .models import Place, Txt, Post
        if not txt and not repost_of: return
        place = Place.locate(lat,lon,ip=ip,placename=placename)
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
    
    def to_dict(self):
        d=super().to_dict()
        del d['passhash']
        return d




user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.id), primary_key=True)
)
