import discord
from discord.ext import commands
import Algorithmia
from MTC import Convert
import random
import requests
import json
import markovify
from breeds import getbreed
from bs4 import BeautifulSoup
import dvdscript
import praw
from PyDictionary import PyDictionary
#from PIL import Image
import os

dictionary = PyDictionary()

bot = commands.Bot(command_prefix=':>', description='i dont know what to put here')
reddit = praw.Reddit(client_id='clientid',
                     client_secret='clientsecret',
                     user_agent='bruhbruhbruhbruh',
                     username='username',
                     password='drowssap')


#Functions
def sntm(text):
    """Sentiment Analysis"""
    input = {"document": text}
    client = Algorithmia.client('simPAhEntLcOy0EoBAlGMezWxNP1')
    algo = client.algo('nlp/SentimentAnalysis/1.0.5')
    algo.set_options(timeout=300) # optional
    res = algo.pipe(input).result[0]
    info = {'sentiment':res['sentiment']}
    if res['sentiment'] >= 0.700:
        info.update({'vague':'Very Positive'})
        return info
    elif res['sentiment'] >= -0.200 and res['sentiment'] <= 0.199:
        info.update({'vague':'Neutral'})
        return info
    elif res['sentiment'] >= 0.200 and res['sentiment'] <= 0.699:
        info.update({'vague':'Positive'})
        return info
    elif res['sentiment'] >= -0.699 and res['sentiment'] <= -0.199:
        info.update({'vague':'Negative'})
        return info
    elif res['sentiment'] <= -0.700:
        info.update({'vague':'Very Negative'})
        return info

def get_dog():
    """Returns dictionary info of a random doggo"""
    dog_dict = {}
    dog = requests.get('https://dog.ceo/api/breeds/image/random')
    url = json.loads(dog.content.decode('utf-8'))["message"]
    
        
    name = random.choice(open('/home/dazzix/facebookbot/doggo/names.txt').readlines()).strip()
    
    
    breed_old = url.split('/')[-2].split('-')
    breed_n = []
    if len(breed_old) >= 2:
        breed_n.append(breed_old[1])
        breed_n.append(breed_old[0])
    else:
        breed_n.append(breed_old[0])
    
        	
    
    breed = ' '.join([b.capitalize() for b in breed_n])
    
    #Fix Breed
    if breed == 'Germanshepherd':
        breed = 'German Shepherd'
    elif breed == 'Mexicanhairless':
        breed = 'Mexican Hairless'
    elif breed == 'Stbernard':
        breed = 'St. Bernard'
    elif breed == 'African':
        breed = 'African Hunting Dog'
    elif breed == 'Bullterrier':
        breed = 'Bull Terrier'
    elif breed == 'Puggle':
        breed = 'Beagle'
    elif breed == 'Staffordshire Bullterrier':
        breed = 'Staffordshire Bull Terrier'

    info = getbreed(breed)
    
    
    headers = {'x-api-key':'c346fcf5-8b89-4c2a-a24f-0a3cf4fc662b'}
    params = {"limit":1,"size":"full","mime_types":"jpg,png"}
    
    if info != None:
        temp1 = info['temperament'].split(', ')
        bred_for = info['bred_for']
    else:
        print('No correct info found, randomizing...lol')
        while True:
            try:
                dog2 = requests.get('https://api.thedogapi.com/v1/breeds').content
                full = random.choice(json.loads(dog2.decode('utf-8')))
                #url = full["url"]
                #breed = full["breeds"][0]["name"]
                bred_for = full["bred_for"]
                temp1 = full["temperament"].split(', ')
            except:
                print('Error! Restarting...')
            else:
                break
    
    temp2 = []
    length = random.randint(1, len(temp1))
    for w in range(length):
        sel = random.choice(temp1)
        temp2.append(sel)
        temp1.remove(sel)
    temperament = ', '.join(temp2)
    
    dog_dict.update({'name':name, 'breed':breed, 'temp':temperament, 'url':url})
    return dog_dict


def sentence():
    with open("/home/dazzix/facebookbot/showerthoughts/thoughts.txt", encoding="utf-8") as f:
        text = f.read()
    num = random.randint(2,4)
    text_model = markovify.NewlineText(text, state_size=num)
    sen = text_model.make_sentence(tries=1000)
    return sen

def fibonacci_y(length):
    n1 = 0
    n2 = 1
    for count in range(length):
        yield n1
        nth = n1 + n2
        n1 = n2
        n2 = nth

def get_comic():
    r = requests.get('http://explosm.net/rcg')
    soup = BeautifulSoup(r.content, 'html.parser')
    img = soup.find('meta', {'property':'og:image'})['content']
    return img

def get_xkcd():
    r = requests.get('https://c.xkcd.com/random/comic/')
    soup = BeautifulSoup(r.content, 'html.parser')
    img = 'https:' + soup.find('div', {'id':'comic'}).img['src']
    ctitle = soup.find('div', {'id':'ctitle'}).text
    return {'img':img, 'title':ctitle}
    
def get_waifu():
    pic = 0
    page = requests.get('http://safebooru.org/index.php?page=post&s=random')
    raw_html = page.content
    html = BeautifulSoup(raw_html, 'html.parser')
    tags = html.find("img", {"id": "image"})['alt']
    taglist = [tag.strip() for tag in tags.split(' ')] 
    pic = html.find("img", {"id": "image"})['src']
    pic_url = 'http:'+pic
    print("downloaded")
    return {'img_url':pic_url,'tags':', '.join(taglist[:10])+'...','page_url':page.url}

def getsub(name, sort, time=None):
    try:
        info = None
        subreddit = reddit.subreddit(name)
        if sort == 'controversial':
            if time == 'hour':
                for submission in subreddit.controversial('hour', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
            
            elif time == 'day':
                for submission in subreddit.controversial('day', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'week':
                for submission in subreddit.controversial('week', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'month':
                for submission in subreddit.controversial('month', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'year':
                for submission in subreddit.controversial('year', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'all':
                for submission in subreddit.controversial('all', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
        elif sort == 'top':
            if time == 'hour':
                for submission in subreddit.top('hour', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
            
            elif time == 'day':
                for submission in subreddit.top('day', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'week':
                for submission in subreddit.top('week', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'month':
                for submission in subreddit.top('month', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'year':
                for submission in subreddit.top('year', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
            elif time == 'all':
                for submission in subreddit.top('all', limit=1):
                    info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
        elif sort == 'hot':
            for submission in subreddit.hot(limit=1):
                info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
        elif sort == 'new':
            for submission in subreddit.new(limit=1):
                info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
        elif sort == 'rising':
            for submission in subreddit.rising(limit=1):
                info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
        elif sort == 'random':
            submission = subreddit.random()
            info = {'title':submission.title,'text':submission.selftext,'url':submission.url,'upvotes':submission.score,'author':submission.author.name,'error':None}
    
    except:
        return {'error':'``Not a valid subreddit``'}
    else:
        return info
            

@bot.listen()
async def on_ready():
    print('---BOT ebib ONLINE---')
    game = discord.Game('with ebib 😳 || :>help')
    await bot.change_presence(status=discord.Status.online, activity=game)
    
@bot.listen()
async def on_message(message):
    if 'ebib' in message.content:
        await message.add_reaction('😳')
        await message.channel.send('😳')

"""
@bot.listen()
async def on_guild_join(guild):
    if not os.path.isfile(f'server/{str(guild.id)}.png'):
        canvas = Image.new('RGB', (500,500), (255,255,255))
        canvas.save(f'server/{str(guild.id)}.png')
"""

@bot.command()
async def sentiment(ctx, *, text):
    """Analyzes a message and gives its sentiment"""
    await ctx.trigger_typing()
    snt = sntm(text)
    await ctx.send('``Sentiment: {} ({})``'.format(snt['sentiment'], snt['vague']))

@bot.command()
async def doggo(ctx):
    """A random cute doggo UwU"""
    await ctx.trigger_typing()
    dog = get_dog()
    embed = discord.Embed()
    embed.set_image(url=dog['url'])
    #img_b = requests.get(dog['url'])
    #img_io = BytesIO(img_b.content)
    await ctx.send(content='Name: ``{}``\nBreed: ``{}``\nTemperament: ``{}``'.format(dog['name'], dog['breed'], dog['temp']), embed=embed)
    
@bot.command()
async def shower(ctx, min_chars=None):
    """force the bot to take a shower and think of a thought"""
    await ctx.trigger_typing()
    await ctx.send(sentence())


@bot.command()
async def actualshower(ctx):
    """an actual submission from the r/Showerthoughts subreddit"""
    await ctx.trigger_typing()
    lines = open('/home/dazzix/facebookbot/showerthoughts/thoughts.txt', encoding='utf-8').read().splitlines()
    actual = random.choice(lines)
    await ctx.send(actual)


@bot.command()
async def cursed(ctx):
    """a random cursed image (beware of using this)"""
    await ctx.trigger_typing()
    with open('/home/dazzix/facebookbot/cursedbot/submissions.txt', encoding='utf-8') as f:
        s_lines = f.read().splitlines()
    with open('/home/dazzix/facebookbot/cursedbot/titles.txt', encoding='utf-8') as fp:
        t_lines = fp.read().splitlines()
    rnd_n = random.randint(0, len(s_lines))
    
    embed = discord.Embed()
    embed.set_image(url=s_lines[rnd_n])
    
    await ctx.send(content=t_lines[rnd_n], embed=embed)

@bot.command()
async def cyanide(ctx):
    """A randomly generated Cyanide & Happiness comic"""
    await ctx.trigger_typing()
    embed = discord.Embed()
    embed.set_image(url=get_comic())
    await ctx.send(embed=embed)

@bot.command()
async def fibonacci(ctx, length):
    """Fibonacci sequence up to specified length"""
    await ctx.trigger_typing()
    try:
        if int(length) <= 1:
            await ctx.send('```0```')
        elif int(length) == 2:
            await ctx.send('```0, 1```')
        elif int(length) > 128:
            await ctx.send('bro character limit...')
        else:
            try:
                await ctx.send('```{}```'.format(', '.join([str(num) for num in fibonacci_y(int(length))])))
            except:
                await ctx.send('bro thats too much...')
    except:
        await ctx.send('bro do you not know what a number is')

@bot.command()
async def weeb(ctx):
    """A random image from Safeboruu"""
    await ctx.trigger_typing()
    waifu = get_waifu()
    embed = discord.Embed(title='Go to source page', url=waifu['page_url'])
    embed.add_field(name='Tags', value=waifu['tags'], inline=False)
    embed.set_image(url=waifu['img_url'])
    await ctx.send(embed=embed)

@bot.command()
async def dvd(ctx):
    """Generates an animated gif of a DVD screensaver"""
    await ctx.trigger_typing()
    gif = dvdscript.make_gif()
    await ctx.send(file=discord.File(gif, 'screensaver.gif'))

"""
@bot.command()
async def canvas(ctx, canvas, command):
    
    Draw whatever u want in the server's or bot's 500x500 canvas
    canvas - b (for the bot), g (for the guild)
    Commands:
    add <x(0-499)> <y(0-499)> <R value(0-255)> <B value(0-255)> <G value(0-255)>
    
    
    if canvas == 'g' or canvas == 'guild' or canvas == 's' or canvas == 'server':
"""     

@bot.command()
async def xkcd(ctx):
    """A random xkcd comic"""
    await ctx.trigger_typing()
    c = get_xkcd()
    embed = discord.Embed(title=c['title'])
    embed.set_image(url=c['img'])
    await ctx.send(embed=embed)

@bot.command()
async def define(ctx, *, text):
    """Define a word"""
    await ctx.trigger_typing()
    word_dict = dictionary.meaning(text)
    if word_dict != None:
        embed = discord.Embed(title=text)
        for key,val in word_dict.items():
            embed.add_field(name=key, value='\n'.join(['- '+a for a in val]))
        await ctx.send(embed=embed)
    else:
        await ctx.send('``Cannot find definition of specified word...``')


@bot.command()
async def subreddit(ctx, name, sort, time_filter='day'):
    """(THIS COMMAND IS BROKEN)Get the top sorted post of a subreddit"""
    await ctx.trigger_typing()
    try:
        sorting = ['controversial', 'hot', 'new', 'rising', 'top', 'random']
        filters = ['hour', 'day', 'week', 'month', 'year', 'all']
        imgmats = ['png', 'jpeg', 'jpg', 'gif']
        #try:
        if sort not in sorting:
            await ctx.send('```ERROR: Invalid sorting\nMust only be {}```'.format(', '.join(sorting)))
        elif sort == 'hot' or sort == 'new' or sort == 'rising' or sort == 'random':
            subm = getsub(name, sort)
            if subm['error'] == None:
                embed = discord.Embed(title='r/'+name, description='u/'+subm['author'], color=0xff8400)
                if subm['text'] == "":
                    embed.add_field(name=subm['title'], value='--------------------', inline=False)
                else:
                    embed.add_field(name=subm['title'], value=''.join([l for i,l in enumerate(subm['text']) if i <= 102]), inline=False)
                if subm['url'].split('.')[-1] in imgmats:
                    embed.set_image(url=subm['url'])
                embed.set_footer(text=str(subm['upvotes'])+" ⬆️\n"+subm['url'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(subm['error'])
            
        else:
            if time_filter not in filters:
                await ctx.send('```ERROR: Invalid time filter\nMust only be {}```'.format(', '.join(filters)))
            else:
                subm = getsub(name, sort, time_filter)
                if subm['error'] == None:
                    embed = discord.Embed(title='r/'+name, description='u/'+subm['author'], color=0xff8400)
                    if subm['text'] == "":
                        embed.add_field(name=subm['title'], value='--------------------', inline=False)
                    else:
                        embed.add_field(name=subm['title'], value=''.join([l for i,l in enumerate(subm['text']) if i <= 102]), inline=False)
                    if subm['url'].split('.')[-1] in imgmats:
                        embed.set_image(url=subm['url'])
                    embed.set_footer(text=str(subm['upvotes'])+" ⬆️\n"+subm['url'])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(subm['error'])
    except:
        await ctx.send('``oh god oh fucj a fatal error``')
    
            

@bot.command()
async def conversions(ctx):
    """List of all text conversion commands"""
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert.conversions))

@bot.command()
async def mock(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).mock()))
    
@bot.command()
async def b(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).b()))

@bot.command()
async def crab(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).crab()))

@bot.command()
async def owo(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).owo()))

@bot.command()
async def sbeve(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).sbeve()))

@bot.command()
async def emoji(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).emoji()))

@bot.command()
async def regional(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send(Convert(text).regional())

@bot.command()
async def binary(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).binary()))

@bot.command()
async def shuffle1(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).shuffle1()))

@bot.command()
async def shuffle2(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).shuffle2()))

@bot.command()
async def shuffle3(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).shuffle3()))

@bot.command()
async def fllf(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).fllf()))

@bot.command()
async def piip(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).piip()))

@bot.command()
async def lipsum(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).lipsum()))

@bot.command()
async def igbo(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).igbo()))

@bot.command()
async def from_igbo(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).from_igbo()))

@bot.command()
async def from_som(ctx, *, text):
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).from_som()))
    
@bot.command()
async def rnd(ctx, *, text):
    """Random text conversion"""
    await ctx.trigger_typing()
    await ctx.send('```{}```'.format(Convert(text).random()))


bot.run('bot-token')