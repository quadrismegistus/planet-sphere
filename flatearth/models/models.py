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


    cities = ['Rio de Janeiro', 'Bogota', 'Budapest', 'Berlin', 'Hong Kong', 'Tokyo', 'Sydney']

    for city in cities:
        user = User.getc(name=city.split()[0]+'Lover69')
        user.post(f'I love {city}!', placename=city)

    for n in tqdm(list(range(1000))):
        lat,lon = random_lat_lon()
        random.choice(User.all()).post(
            f'''Just posting again the {n}th time. Just enjoyed a peaceful afternoon at the park, watching the sunset and listening to my favorite playlist. 🌅🎶 It's moments like these that remind me to appreciate the simple things in life. #NatureLover #SunsetVibes. 🍃 Later, tried out a new recipe for homemade pizza - turned out pretty amazing! Who knew cooking could be this fun? 🍕😊 #HomeChef #CookingAdventures. Finally, wrapped up the day with a good book and some quiet time. #EveningReads #RelaxationMode. 📚✨ What’s your go-to activity for a chill day?''', 
            lat=lat, 
            lon=lon
        )

    for n in tqdm(list(range(1000))):
        u = User.random()
        p = Post.random()
        u.like(p)
    
    return repost


