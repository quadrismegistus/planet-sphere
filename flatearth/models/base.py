from ..imports import *

Base = declarative_base()

@classmethod
def iter(self):
    yield from self.find()

@classmethod
def rand(self):
    return random.choice(self.all())

@classmethod
def all(self):
    return list(self.iter())

@classmethod
def _first(self):
    for x in self.iter(): return x

def save(self):
    self.ensure_table()
    db = get_db_session()
    db.add(self)
    db.commit()
    return self


@classmethod
def query_by_attr(cls, **kwargs):
    db = get_db_session()
    query = db.query(cls)
    if not kwargs:
        return query
    else:
        qconds = [(getattr(cls, key) == val) for key, val in kwargs.items()]
        return query.filter(and_(*qconds))


@classmethod
def get(cls, **kwargs):
    return cls.query_by_attr(**kwargs).first()

@classmethod
def get_or_create(cls, **kwargs):
    obj = cls.get(**kwargs)
    if not obj:
        obj = cls(**kwargs).save()
    return obj

@classmethod
def find(cls, **kwargs):
    return cls.query_by_attr(**kwargs).all()


@classmethod
def ensure_table(self):
    engine = get_db_engine()
    with engine.connect() as conn:
        if not engine.dialect.has_table(conn, self.__tablename__):
            self.__table__.create(engine)


@classmethod
def nearby_l(cls,*args,n=25,**kwargs):
    return list(itertools.islice(cls.nearby(*args,**kwargs), n))

@classmethod
def nearest(cls,*args,**kwargs):
    res = first(cls.nearby(*args,**kwargs))
    return res[0] if res else res


@classmethod
def getc(cls, *x,**y):
    return cls.get_or_create(*x,**y)

@property
def jsonx(self):
    return json.dumps(
        self.data,
        indent=2
    )

@property
def data(self): return self.to_dict()

def to_dict(self, **attrs):
    d = {}
    attrs = {'id':self.id, **(self.__dict__ if not attrs else attrs)}
    for k,v in attrs.items():
        if k[0]!='_' and v is not None:
            d[k]=(v.to_dict() if isinstance(v,Base) else v)
    d['_tbl']=self.__tablename__
    return d


Base.save = save
Base.query_by_attr = query_by_attr
Base.get = get
Base.getc = getc
Base.get_or_create = get_or_create
Base.find = find
Base.ensure_table = ensure_table
Base.nearby_l = nearby_l
Base.nearest = nearest
Base.json = jsonx
Base.data = data
Base.to_dict = to_dict
Base.iter = iter
Base.all = all
Base.first = _first
Base.random = rand

# rels
post_liking = Table(
    'post_liking', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True)
)
