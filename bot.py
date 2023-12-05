"""
Previously, only God and I understood how wu bot works, but now only God understands how it works
- Vlad
"""

import random

import discord
from discord.ext import commands, tasks
import fandom
from fandom.error import PageError
from google_images_search import GoogleImagesSearch

TOKEN = "TOKEN"

guilds = [738131752710832238, 975501594227535942] # testing guilds that is not counted
intents = discord.Intents.default()
bot = commands.AutoShardedBot(intents=intents)

@tasks.loop(minutes=5)
async def presence_update():
    members_counter = 0
    server_counter = 0
    for guild in bot.guilds:
        if guild.id not in guilds:
            members_counter += guild.member_count
            server_counter += 1
    game = discord.Game(
        f"/help | {members_counter} members on {server_counter} servers | Learn more: support@vladhog.ru")
    await bot.change_presence(activity=game)

@bot.event
async def on_ready():
    print("Ready")
    members_counter = 0
    server_counter = 0
    for guild in bot.guilds:
        if guild.id not in guilds:
            members_counter += guild.member_count
            server_counter += 1
    game = discord.Game(
        f"/help | {members_counter} members on {server_counter} servers | Learn more: support@vladhog.ru")
    await bot.change_presence(activity=game)
    try:
        presence_update.start()
    except RuntimeError:
        pass

@bot.slash_command(name="waiting", description="Waiting for something lmao")
async def _waiting(ctx):
    await ctx.respond("*waiting...*")


@bot.slash_command(name="search", description="Searching information on wiki")
async def search(ctx, word):
    await ctx.defer()
    fandom.set_wiki("Ninjago")
    page_status = 1
    try:
        url = fandom.page(word).url
        a = fandom.summary(word) + f"\n\nFor more info: {url}"
    except PageError:
        page_status = 0
    if page_status == 0:
        a = "**We didn't find what you wanted, but maybe some of this will help you: **\n\n"
        data = fandom.search(word, wiki="Ninjago", language="en", results=5)
        for i in data:
            page = fandom.page(i[0])
            url = page.url
            a += f"**{page.title}** - {url}\n"

    # print(a)
    embed = discord.Embed(title="Ninjago Wiki", description=a, color=discord.Colour.random())
    await ctx.respond(embed=embed)


@bot.slash_command(name="random", description="Random ninjago wiki page")
async def randmon_page(ctx):
    await ctx.defer()
    fandom.set_wiki("Ninjago")
    a = fandom.random()
    url = fandom.page(a[0]).url
    b = fandom.summary(a[0]) + f"\n\nFor more info: {url}"
    embed = discord.Embed(title="Ninjago Wiki", description=b, color=discord.Colour.random())
    await ctx.respond(embed=embed)


@bot.slash_command(name="search_image", description="Searching images in google for you")
async def search_image(ctx, word: str, spread: int = 10):
    await ctx.defer()
    search_params = {
        'q': f'"{word}" ninjago',
        'num': int(spread),
        'safe': 'active',  ##
    }
    try:
        res = {}
        gis = GoogleImagesSearch('some tokens here')
        gis.search(search_params=search_params)
        for image in gis.results():
            # print(image.url)
            # print(image.referrer_url)
            res[image.url] = image.referrer_url

        res_l = len(list(res))
        a = random.randint(0, res_l - 1)
        b = list(res)[a]
        c = res[b]
        embed = discord.Embed(title="Ninjago Image Search", description=f"Source: {c}", colour=discord.Colour.random())
        embed.set_image(url=b)
        await ctx.respond(embed=embed)
    except Exception:
        embed = discord.Embed(title="Ninjago Image Search",
                              description=f"An error occurred during the search.\nOur smart hamsters are already solving this problem\n\n~~Vladhog Development",
                              colour=discord.Colour.random())
        await ctx.respond(embed=embed)


@bot.slash_command(name="help", description="Just a help command")
async def help(ctx):
    embed = discord.Embed(title="Wu bot", description="By Vladhog Development", colour=discord.Colour.random())
    embed.add_field(name="A tematic bot created at the request of the Ninjacord server",
                    value="https://discord.gg/Y43RTSvJYD", inline=True)
    embed.add_field(name="""```/search```""",
                    value="**Looking for your search query on the official ninjago wikipedia!**", inline=True)
    embed.add_field(name="```/waiting```", value="***waiting...***", inline=True)
    embed.add_field(name="```/random```", value="**Looking for a random page on the ninjago wiki**", inline=True)
    embed.add_field(name="```/search_image```",
                    value="**Searches for a random picture according to your request. Attention: Google is the provider of search services and we cannot guarantee the quality of search results**",
                    inline=True)
    await ctx.respond(embed=embed, ephemeral=True)

bot.run(TOKEN)
