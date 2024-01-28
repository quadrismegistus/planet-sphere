from .place import *
from .user import *
from .text import *
from .post import *

DB_TABLES = [User, Place, Txt, Translation, Post]

def test():
    ensure_db_tables(clear=True)
    user = User.get_or_create(name='Marx')
    post = user.post('Guten morgen!', lat=49.75565, lon=6.63935)
    post.translate_to('fr')
    post.translate_to('en')
    return post
