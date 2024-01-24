import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os

bot = commands.Bot(command_prefix = 'v!')
bot.remove_command('help')


#Alerts you when the bot is ready to take in commands
@bot.event
async def on_ready():
    print('Tracking Valorant Accounts!')
    await bot.change_presence(activity=discord.Game(name='Valorant'))
#Checks the ping of the bot
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! My ping is {round(bot.latency*1000)}ms')

#Find a players stats
@bot.command(aliases=['stat', 'track'])
async def stats(ctx, id, *, mode="competitive"):
    name = id.split('#')[0]
    tag = id.split('#')[1]
    URL = f'https://tracker.gg/valorant/profile/riot/{name.replace("-","%20")}%23{tag}/overview?playlist={mode.replace(" ","")}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    app = soup.find(id='app')

    hv = app.find_all('span', class_="valorant-highlighted-stat__value")
    if len(hv) == 2:
        embed = discord.Embed(title=f"Stats for {name}#{tag} in {mode}",description=f"Rank: {hv[0].text}",color=discord.Color.red())
        img = app.find('img', class_="valorant-rank-icon").get('src')
        embed.set_author(name=f'{name}#{tag}', icon_url=img)

    else:
        embed = discord.Embed(title=f"Stats for {name}#{tag}",description=" ",color=discord.Color.red())

    values = app.find_all('span', class_="value")
    embed.add_field(name="Damage Per Round: ",value=f"{values[3].text}",inline=True)
    embed.add_field(name="K/D Ratio: ",value=f"{values[4].text}",inline=True)
    embed.add_field(name="Headshot Percentage: ",value=f"{values[5].text}%",inline=True)
    embed.add_field(name="Win Rate: ",value=f"{values[6].text}",inline=True)
    embed.add_field(name="Total Wins: ",value=f"{values[7].text}",inline=True)
    embed.add_field(name="Total Kills: ",value=f"{values[8].text}",inline=True)
    embed.add_field(name="Kills Per Round: ",value=f"{values[13].text}",inline=True)
    embed.add_field(name="Clutches: ",value=f"{values[14].text}",inline=True)
    embed.add_field(name="Highest Kill Match: ",value=f"{values[16].text}",inline=True)

    agents = app.find_all('span', class_="agent__name")
    names = app.find_all('span', class_="name")
    embed.add_field(name="Top Agents Played:",value="---------------",inline=False)
    embed.add_field(name=f"{agents[0].text}: ",value=f"Matches Played: {names[25].text}\nWin Rate: {names[26].text}\nAgent K/D: {names[27].text}",inline=True)
    embed.add_field(name=f"{agents[1].text}: ",value=f"Matches Played: {names[30].text}\nWin Rate: {names[31].text}\nAgent K/D: {names[32].text}",inline=True)
    embed.add_field(name=f"{agents[2].text}: ",value=f"Matches Played: {names[35].text}\nWin Rate: {names[36].text}\nAgent K/D: {names[37].text}",inline=True)


    await ctx.send(embed=embed)

#Find a players weapon stats
@bot.command(aliases=['guns', 'weapon', 'gun'])
async def weapons(ctx, id, *, mode="competitive"):
    name = id.split('#')[0]
    tag = id.split('#')[1]
    URL = f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/weapons?playlist={mode}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    app = soup.find(id='app')
    weapons = app.find_all('span', class_="segment-used__tp-name")
    embed = discord.Embed(title=f"Weapons Statistics for {name}#{tag}:",description=" ",color=discord.Color.red())

    embed.add_field(name="Top Weapons:",value="---------------",inline=False)
    embed.add_field(name=f"{weapons[0].text}:",value=f"Total Kills: {weapons[1].text}\nHeadshot Percentage: {weapons[4].text}%\nLongest Kill Distance: {weapons[7].text}m",inline=True)
    embed.add_field(name=f"{weapons[8].text}:",value=f"Total Kills: {weapons[9].text}\nHeadshot Percentage: {weapons[12].text}%\nLongest Kill Distance: {weapons[15].text}m",inline=True)
    embed.add_field(name=f"{weapons[16].text}:",value=f"Total Kills: {weapons[17].text}\nHeadshot Percentage: {weapons[20].text}%\nLongest Kill Distance: {weapons[23].text}m",inline=True)

    await ctx.send(embed=embed)

#Find a players total playtime
@bot.command(aliases=['hours', 'time'])
async def playtime(ctx, id):
    name = id.split('#')[0]
    tag = id.split('#')[1]
    days = 0
    hours = 0
    min = 0
    modes = ['Competitive', 'Deathmatch', 'Escalation', 'Spike Rush', 'Unrated']

    embed = discord.Embed(title=f"Playtime for {name}#{tag}:",description=" ",color=discord.Color.red())
    for mode in modes:
        d = 0
        h = 0
        m = 0
        URL = f'https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview?playlist={mode.lower().replace(" ","")}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        app = soup.find(id='app')
        time = app.find('span', class_="playtime").text.replace("Play Time","")
        time = time.split(" ")
        del time[0:10]
        del time[3:12]
        for item in time:
            if "D" in item:
                d = int(item.replace("D",""))
                days = days + d
            if "H" in item:
                h = int(item.replace("H",""))
                hours = hours + h
            if "M" in item:
                m = int(item.replace("M",""))
                min = min + m
        embed.add_field(name=f"Time played on {mode}: ",value=f"{d} Days, {h} Hours, {m} Minutes",inline=False)

    days = days + ((hours - (hours % 24))/24)
    hours = (hours % 24) + ((min - (min % 60))/60)
    min = (min % 60)

    embed.add_field(name=f"Total time played: ",value=f"{days} Days, {hours} Hours, {min} Minutes",inline=False)
    await ctx.send(embed=embed)

#Find a players stats
@bot.command(aliases=['help'])
async def commands(ctx):
    embed = discord.Embed(title="Commands:",description="The bot is still in development, more commands may come soon",color=discord.Color.red())
    embed.add_field(name="Commands (commands) ",value=f"Displays all the commands the robot can do.",inline=False)
    embed.add_field(name="Player Statistics (stats) ",value="Find the statistics of a player.\nParameters:\nid - name#number of the Valorant account.\nmode - The gamemode you want to check the stats on.",inline=False)
    embed.add_field(name="Player Weapons (weapons) ",value="Find the weapon statistics of a player.\nParameters:\nid - name#number of the Valorant account.\nmode - The gamemode you want to check the stats on.",inline=False)
    embed.add_field(name="Player Playtime (playtime) ",value="Find the amount of time a player has on Valorant.\nParameters:\nid - name#number of the Valorant account. Replace spaces with a dash (-).",inline=False)
    embed.add_field(name="Ping",value="Checks the bot's ping.",inline=False)

    await ctx.send(embed=embed)

bot.run("token")
