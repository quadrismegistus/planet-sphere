from .place import *
from .user import *
from .text import *
from .post import *
from .feed import *


demoposts = [
    "Just tried the new vegan burger at Green Bites Café – absolutely delicious! 🌱🍔 #VeganFood #Foodie",
    "Morning run completed, feeling energized and ready to tackle the day! 🏃‍♂️💪 #MorningRun #FitnessGoals",
    "In awe of the sunset I witnessed today. Nature's beauty is truly unmatched. 🌅 #SunsetLover #NaturePhotography",
    "Can't believe how much I've learned in my coding journey this month. Persistence pays off! #CodeNewbie #100DaysOfCode",
    "Throwback to our amazing beach holiday last summer. Can't wait to travel again! 🏖️✈️ #TravelMemories #Wanderlust",
    "Just finished reading 'The Midnight Library' and wow, what an emotional rollercoaster! 📚 #BookRecommendations #Readers",
    "Exploring the local art scene this weekend was a blast. So much talent out there! 🎨 #ArtLover #SupportLocalArtists",
    "Coffee and jazz music – the perfect combo for a relaxing Sunday morning. ☕🎷 #SundayVibes #Relaxation",
    "DIY home renovation project: complete! Feeling proud and a bit exhausted. 🛠️🏡 #HomeImprovement #DIYProjects",
    "Gearing up for tonight's game. Let's go team! ⚽🏆 #GameDay #SportsFan"
]


def test(clear=True):
    ensure_db_tables(clear=clear)
    marx = User.register(name='marx',password='rocks')
    zuck = User.register(name='zuck',password='sucks')
    elon = User.register(name='elon',password='suxxx')
    
    post = marx.post('Guten morgen', placename='Trier')
    # post.translate_to('fr')

    zuck.post('Good morning', placename='Palo Alto')
    elon.post('I am an idiot')

    elon.follow(marx)
    elon.follow(zuck)
    zuck.follow(marx)

    elon.like(post)
    zuck.like(post)

    repost = elon.repost(post, 'lol')

    zuck.reply(repost, 'what?', placename='Palo Alto')
    zuck.reply(post, 'good morning', placename='Palo Alto')

    cities = ['Rio de Janeiro', 'Bogota', 'Budapest', 'Berlin', 'Hong Kong', 'Tokyo', 'Sydney']

    for city in tqdm(cities):
        user = User.register(name=city.split()[0]+'Lover69', password=city)
        user.post(f'I love {city}!', placename=city)

    for n in tqdm(list(range(50))):
        lat,lon = random_lat_lon()
        post = User.random().post(
            random.choice(demoposts), 
            lat=lat, 
            lon=lon
        )

    for n in tqdm(list(range(100))):
        u = User.random()
        p = Post.random()
        u.reply(p, 'wtf are you talking about', placename=Place.random().name)

    for n in tqdm(list(range(1000))):
        u = User.random()
        p = Post.random()
        u.like(p)
    
    return repost


