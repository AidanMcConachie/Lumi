import discord
import time
import os
import random
import datetime 
from replit import db

intents = discord.Intents.default()
intents.members = True

from discord.ext import commands

client = commands.Bot(command_prefix='!', intents=intents)

client.remove_command('help')

token=os.environ.get("DISCORD_BOT_SECRET")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.send('You have been banned from the server: ' + str(reason))
    await member.ban(reason=reason)
    await ctx.send('Banned ' + str(member))


@client.command()
@commands.has_permissions(ban_members=True)
async def fban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send('Banned ' + str(member))


@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nick=None):
    await member.edit(nick=nick)
    await ctx.send(str(member) + ' nickname is now ' + str(nick))


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.send('You have been kicked from the server: ' + str(reason))
    await member.kick(reason=reason)
    await ctx.send('Kicked ' + str(member))


@client.command()
@commands.has_permissions(kick_members=True)
async def fkick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send('Kicked ' + str(member))


@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    await member.send('You have been warned: ' + str(reason))
    await ctx.send('Warned ' + str(member))


@client.command()
async def ping(ctx):
    ping = client.latency * 1000
    final = '%0.2f' %ping
    await ctx.send('Pong! `' + str(final) + ' ms`')


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(remove, *, amount=0):
    await remove.channel.purge(limit=amount + 1)


@client.command()
async def type(ctx, *, words):
    await ctx.channel.purge(limit=1)
    await ctx.send('`' + str(words) + '`')





@client.command()
async def suggest(ctx, *, suggestion=None):
  if suggestion==None:
    await ctx.send('Maybe suggest something...')
  elif suggestion!=None:
    suggestchannel = client.get_channel(786466339472277515)
    await ctx.channel.purge(limit=1)
    await ctx.author.send('Your suggestion (' + str(suggestion) + ') has been submitted to the server!')
    embed = discord.Embed(
        title='New Suggestion!',
        description=str(suggestion),
        colour=discord.Colour.teal())
    embed.set_footer(text='Sumbitted by ' + str(ctx.author.name))
    await suggestchannel.send(embed=embed)


@client.command()
async def embed(ctx, title, *, description):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(
        title=title, description=description, colour=discord.Colour.blue())
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def cf(ctx, side, amount):
  flip = ["Heads", "Tails"]
  final = str(random.choice(flip))
  id = ctx.author.id
  if db[id]>=int(amount):
    if final=='Heads' and side=='h' or final=='Tails' and side=='t':
      await ctx.send(ctx.author.mention + ' flipped a coin! It landed on `' + final + '`! You won ' + str(amount) + ' cookies!')
      db[id]=db[id]+int(amount)
    elif final=='Heads' and side=='t' or final=='Tails' and side=='h':
      await ctx.send(ctx.author.mention + ' flipped a coin! It landed on `' + final + '`! You lost ' + str(amount) + ' cookies...')
      db[id]=db[id]-int(amount)
  else:
    await ctx.send('You do not have enough cookies!')



@client.command()
async def magic8ball(ctx):
  ran=["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
  ball = str(random.choice(ran))
  await ctx.send(ctx.author.mention + ' :8ball: ' + ball)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def rps(ctx, defend):
  id=ctx.author.id
  choices = ["s", "r", "p"]
  attack = str(random.choice(choices))
  if defend =="s" and attack=="s":
    await ctx.send("You picked `scissors`, I picked `scissors`. Draw! You earned 5 cookies!")
    db[id]=db[id]+int(5)
  elif defend =="s" and attack=="r":
    await ctx.send("You picked `scissors`, I picked `rock`. You lost!")
  elif defend =="s" and attack=="p":
    await ctx.send("You picked `scissors`, I picked `paper`. You won! You earned 10 cookies!")
    db[id]=db[id]+int(10)
  elif defend =="p" and attack=="p":
    await ctx.send(("You picked `paper`, I picked `paper`. Draw! You earned 5 cookies!"))
    db[id]=db[id]+int(5)
  elif defend =="p" and attack=="s":
    await ctx.send("You picked `paper`, I picked `scissors`. You lost!")
  elif defend =="p" and attack=="r":
    await ctx.send("You picked `paper`, I picked `rock`. You won! You earned 10 cookies!")
    db[id]=db[id]+int(10)
  elif defend =="r" and attack=="r":
    await ctx.send("You picked `rock`, I picked `rock`. Draw! You earned 5 cookies!")
    db[id]=db[id]+int(5)
  elif defend =="r" and attack=="p":
    await ctx.send("You picked `rock`, I picked `paper`. You lost!")
  elif defend =="r" and attack=="s":
    await ctx.send("You picked `rock`, I picked `scissors`. You won! You earned 10 cookies!")
    db[id]=db[id]+int(10)
    


@client.command()
async def join(ctx):
  id = ctx.author.id
  db[id]=int()
  await ctx.send('You can now earn cookies! :cookie:')


# -----------------------------------------------------


@client.event
async def on_member_join(member):
  user = str(member.created_at)
  current = str(datetime.datetime.now())
  now = current.replace(" ", "").replace("-", "").replace(":", "").replace(".", "")
  person = user.replace(" ", "").replace("-", "").replace(":", "").replace(".", "")
  x = int(now)-int(person)
  print(now)
  print(person)
  print(x)
  if x<=1000000000000:
    coolchannel = client.get_channel(786465156149542942)
    embed=discord.Embed(title="Potential Raider", description=str(member) + " has been automatically kicked, flagged for `new account`", colour=discord.Colour.red())
    await coolchannel.send(embed=embed)
    embed.set_footer(text="User ID: " + str(member.id))
    await member.send("You have been kicked from the server due to your account being less than 24 hours old")
    await member.kick(reason="Potential Raid/New account")
  else:
    coolchannel = client.get_channel(786465156149542942)
    await coolchannel.send('Welcome to the server ' + str(member.mention) + '!')
  


# -----------------------------------------------------
 

@client.command()
async def change(ctx, id, amount):
  if ctx.author.id==462265714032640000:
    db[id]=int(amount)
    await ctx.send('Success!')
  else:
    await ctx.send('...')


@client.command()
async def shop(ctx):
  embed=discord.Embed(title='Cookie Shop :cookie:', description='Here are some roles you can buy with your cookies!', colour=discord.Colour.from_rgb(250,228,146))
  embed.add_field(name='Cookie Noob - 500 :cookie:', value='`!buy noob`', inline=True)
  embed.add_field(name='Cookie Legend - 5000 :cookie:', value='`!buy legend`', inline=True)
  embed.add_field(name='Cookie Master - 10000 :cookie:', value='`!buy master`', inline=True)
  await ctx.send(embed=embed)

@client.command()
async def buy(ctx, *, item):
  id=ctx.author.id
  if item=='noob':
    if db[id]>=500:
      user = ctx.author
      role=discord.utils.get(ctx.guild.roles, name='Cookie Noob')
      await ctx.send('Are you sure you want to buy the role `Cookie Noob` for 500 :cookie: ? (y/n)')
      def check(m):
            return m.content == 'y'
      await client.wait_for('message', check=check)
      await user.add_roles(role)
      db[id]=db[id]-int(500)
      await ctx.send('You bought the role `Cookie Noob`! I have added the role to your account')
    else:
      await ctx.send('You do not have enough cookies!')
  elif item=='legend':
    if db[id]>=5000:
      user = ctx.author
      role=discord.utils.get(ctx.guild.roles, name='Cookie Legend')
      await ctx.send('Are you sure you want to buy the role `Cookie Legend` for 5000 :cookie: ? (y/n)')
      def check(m):
            return m.content == 'y'
      await client.wait_for('message', check=check)
      await user.add_roles(role)
      db[id]=db[id]-int(5000)
      await ctx.send('You bought the role `Cookie legend`! I have added the role to your account')
    else:
      await ctx.send('You do not have enough cookies!')
  elif item=='master':
    if db[id]>=10000:
      user = ctx.author
      role=discord.utils.get(ctx.guild.roles, name='Cookie Master')
      await ctx.send('Are you sure you want to buy the role `Cookie Master` for 10000 :cookie: ? (y/n)')
      def check(m):
            return m.content == 'y'
      await client.wait_for('message', check=check)
      await user.add_roles(role)
      db[id]=db[id]-int(10000)
      await ctx.send('You bought the role `Cookie Master`! I have added the role to your account')
    else:
      await ctx.send('You do not have enough cookies!')


@client.event
async def on_member_leave(member):
    coolchannel = client.get_channel(786465156149542942)
    await coolchannel.send(str(member) + ' has left the server...')


@client.command()
async def rules(ctx, tn):
  if ctx.author.id==462265714032640000:
    embed=discord.Embed(title='Rules', description='These are the offical rules of the server, and are subject to change at any time', colour=discord.Colour.blue(), url='https://discord.com/terms')
    embed.add_field(name='1. No Toxicity:', value="Don’t be too toxic around members. Try and keep drama out of this server. Directed swears should be kept at a minimum level.", inline=True)
    embed.add_field(name='2. No racial slurs:', value="The use of racial slurs in chat will be a kick or a ban based on the usage.", inline=True)
    embed.add_field(name='3. No NSFW/NSFL:', value='Light NSFW talk is fine as long as nothing bad is said. NSFW memes are fine as long as nothing bad is shown. anything else should go in #・nsfw', inline=True)
    embed.add_field(name='4. No spam:', value='Spam should be kept in #・spam. Spamming anywhere else will result in a mute.', inline=True)
    embed.add_field(name='5. Follow Discord TOS:', value='Click the title to be redirected to it', inline=True)
    embed.set_footer(text='Written by Willing, Embedded by Luminous')
    embed.set_thumbnail(url=tn)
    await ctx.send(embed=embed)
  else:
    await ctx.send('Sorry, only Luminous can run this command!')


@client.command()
async def cookies(ctx, id=None):
  selfid=ctx.author.id
  if id==None:
    await ctx.send('You currently have __' + str(db[selfid]) + '__ cookies!')
  else:
    await ctx.send(str('That user currently has __' + str(db[id]) + '__ cookies!'))


@client.command(name="claim")
@commands.cooldown(1, 300, commands.BucketType.user)
async def claim(ctx):
  id = ctx.author.id
  db[id]=db[id]+int(50)
  await ctx.send('You claimed 50 cookies!')

@claim.error
async def claim_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send( 'You have claimed recently, try again later')
    else:
        raise error





@client.command(name='rob')
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
  id = member.id
  robberid = ctx.author.id
  rob=[1,2,3]
  rolecheck = [role.name for role in ctx.author.roles]
  rolecheck2 = [role.name for role in member.roles]
  robbable = str(random.choice(rob))
  if 'Locked' in rolecheck or 'Locked' in rolecheck2:
    await ctx.send('Either you or the other user is locked! :lock:')
  else:
    if db[robberid]>=100:
      if robbable=='1' or robbable=='2':
        if db[robberid]<=200:
          await ctx.send('You got caught! You now have zero cookies')
          db[robberid]=int(0)
        else:
          await ctx.send('You got caught! You paid a fine of 200 cookies')
        db[robberid]=db[robberid]-int(200)
      elif robbable=='3':
        await ctx.send('You robbed ' + member.name + '! You took ' + str(round(db[id])*0.4)+' cookies!')
        db[robberid]=db[robberid]+round(db[id]*0.4)
        db[id]=round(db[id]*0.6)
    else:
      await ctx.send('You must have at least 100 cookies to rob someone!')
    

@rob.error
async def rob_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        final = '%0.1f' %error.retry_after
        await ctx.send( 'You are on Cooldown, please wait ' + str(final) + ' seconds')
    else:
        raise error 


@client.command(name='work')
@commands.cooldown(1, 60, commands.BucketType.user)
async def work(ctx):
  id = ctx.author.id
  money = [5,10,15,20,25,30,35,40,45,50]
  cookies = str(random.choice(money))
  job=['Lawyer', 'Teacher', 'Mayor', 'Cop', 'Pizza Baker', 'Twitch Streamer', 'Youtuber', 'Developer', 'Director', 'Producer', 'Actor', 'Author', 'Cashier', 'Nurse', 'Doctor', 'Firefighter', 'Engineer']
  choose = str(random.choice(job))
  await ctx.send('You worked as `' + str(choose) + '` for ' + str(cookies) + ' cookies!')
  db[id]=db[id]+int(cookies)



@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after
        final = '%0.1f' %cooldown
        await ctx.send( 'You are on Cooldown, please wait ' + str(final) + ' seconds')
    else:
        raise error



@client.command()
async def version(ctx):
  await ctx.send('Lumi Bot is on Version 0.1.8')

@client.command()
async def pingme(ctx):
  rolecheck = [role.name for role in ctx.author.roles]
  user = ctx.author
  role=discord.utils.get(ctx.guild.roles, name='PingMe')
  if 'PingMe' in rolecheck:
    await user.remove_roles(role)
    await ctx.send('I have removed the role `PingMe`')
  else:
    await user.add_roles(role)
    await ctx.send('You have recived the role `PingMe`')

@client.command()
async def fixvalue(ctx):
  id = ctx.author.id
  db[id]=round(db[id])
  await ctx.send('Fixed Value')


@client.command()
async def lock(ctx):
  user = ctx.author
  role=discord.utils.get(ctx.guild.roles, name='Locked')
  await user.add_roles(role)
  await ctx.send('You locked your account! :lock:')

@client.command()
async def unlock(ctx):
  user = ctx.author
  role=discord.utils.get(ctx.guild.roles, name='Locked')
  await user.remove_roles(role)
  await ctx.send('You unlocked your account! :unlock:')


@client.command()
async def help(ctx):
  user = ctx.author
  embed=discord.Embed(title="Commands", description='To earn cookies, type `!join` once', colour=discord.Colour.teal())
  embed.add_field(name='Moderation', value='`ban, kick, nick, warn, purge`', inline=True)
  embed.add_field(name='Fun', value='`join, cf, magic8ball, rps, shop, buy, cookies, claim, rob, work, lock, unlock`', inline=True)
  embed.add_field(name='Miscellaneous', value='`type, suggest, embed, version, pingme, help, ping`', inline=True)
  embed.set_footer(text="Need help? Ping/DM @Luminous#4617")
  await ctx.send("I've sent info to your DMs")
  await user.send(embed=embed)
@client.event
async def on_connect():
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game(name='!help'))


@client.event
async def on_ready():
    print('Online!')


# ______________________________________________________________________________________________________________________

client.run(token)
