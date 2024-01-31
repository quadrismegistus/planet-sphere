from .place import *
from .user import *
from .text import *
from .post import *


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

    for city in tqdm(cities):
        user = User.getc(name=city.split()[0]+'Lover69')
        user.post(f'I love {city}!', placename=city)

    for n in tqdm(list(range(100))):
        lat,lon = random_lat_lon()
        User.random().post(
            random.choice(demoposts), 
            lat=lat, 
            lon=lon
        )

    for n in tqdm(list(range(100))):
        u = User.random()
        p = Post.random()
        u.like(p)
    
    return repost


