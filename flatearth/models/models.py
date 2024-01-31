from .place import *
from .user import *
from .text import *
from .post import *


def test(clear=True):
    ensure_db_tables(clear=clear)
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


    cities = ['Rio de Janeiro', 'Bogota', 'Budapest', 'Berlin', 'Hong Kong', 'Tokyo', 'Sidney']
    for city in cities:
        user = User.getc(name=city.split()[0]+'Lover69')
        user.post(f'I love {city}!', placename=city)

    for n in range(50):
        lat,lon = random_lat_lon()
        user.post(
            f'Just posting again the {n}th time', 
            lat=lat, 
            lon=lon
        )
    
    return repost


