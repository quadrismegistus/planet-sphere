from .place import *
from .user import *
from .text import *
from .post import *


def test():
    ensure_db_tables(clear=True)
    marx = User.getc(name='marx')
    elon = User.getc(name='elon')
    zuck = User.getc(name='zuck')
    
    post = marx.post('Guten morgen', placename='Trier')
    post.translate_to('fr')

    zuck.post('Good morning', placename='Palo Alto')
    elon.post('I am an idiot', placename='San Francisco')

    elon.follow(marx)
    elon.follow(zuck)
    zuck.follow(marx)

    elon.like(post)
    zuck.like(post)

    repost = elon.repost(post, 'lol')

    zuck.reply(repost, 'what?')
    zuck.reply(post, 'good morning')
    
    return repost
