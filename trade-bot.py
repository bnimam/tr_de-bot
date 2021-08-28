import configparser

from discord.ext import commands
from discord import Embed

import yfinance as yf
import wallstreet as ws

creds = configparser.ConfigParser()
creds.read('.config')

TOKEN = creds['credentials']['token']

client = commands.Bot(command_prefix='-')


async def defaults(func):
    async def wrap(ctx):
        if ctx.author == client.user:
            return
        elif ctx.message.guild is None:
            await ctx.channel.send("This is not the proper way to ask me")
            return
        else:
            await func(ctx)
    return wrap

@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print(f'ID: {client.user.id}')
    print('------')


@client.command()
@defaults
async def init(ctx):
    return


@client.command()
@defaults
async def q(ctx):
    msg_tkns = ctx.message.content.split(' ')
    tkr = msg_tkns[0]

    msg = await ctx.channel.send(f"{ctx.message.author.mention} fetching results for {tkr}")
    price = await ws.Stock(tkr).price
    await msg.edit(content=f"{tkr}: {price}")


@client.command()
@defaults
async def history(ctx):
    return


@client.command()
@defaults
async def buy(ctx):
    return


@client.command()
@defaults
async def sell(ctx):
    return


@client.command()
@defaults
async def balance(ctx):
    return


@client.command()
@defaults
async def leaderboard(ctx):
    return


client.run(TOKEN)