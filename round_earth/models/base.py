from ..imports import *

Base = declarative_base()


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
def nearest(cls, lat, lon, n=25, **kwargs):
    return list(itertools.islice(cls.nearby(lat, lon, **kwargs), n))


Base.save = save
Base.query_by_attr = query_by_attr
Base.get = get
Base.get_or_create = get_or_create
Base.find = find
Base.ensure_table = ensure_table
Base.nearest = nearest
