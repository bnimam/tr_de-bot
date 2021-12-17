import configparser
import io

import aiosqlite
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import pandas as pd

import yfinance as yf
import wallstreet as ws

creds = configparser.ConfigParser()
creds.read('.config')

TOKEN = creds['credentials']['token']

colors = {'red': '#ff207c', 'grey': '#42535b', 'blue': '#207cff', 'orange': '#ffa320', 'green': '#00ec8b'}
config_ticks = {'size': 14, 'color': colors['grey'], 'labelcolor': colors['grey']}
config_title = {'size': 18, 'color': colors['grey'], 'ha': 'left', 'va': 'baseline'}

client = commands.Bot(command_prefix='-')


async def defaults(func):
    async def wrap(ctx):
        if ctx.author.id == client.user.id:
            return
        elif ctx.message.guild is None:
            await ctx.channel.send("This is not the proper way to ask me")
            return
        else:
            await func(ctx)
    return wrap


async def get_std_chart(dataframe: pd.DataFrame,
                        tkr:       str) -> io.BytesIO:
    plt.rc('figure', figsize=(15, 10))
    fig, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.tight_layout(pad=3)

    date = dataframe['Date']
    close = dataframe['Close']
    vol = dataframe['Volume']

    plot_price = axes[0]
    plot_price.plot(date, close, color=colors['blue'], 
    linewidth=2, label='Price')

    plot_vol = axes[1]
    plot_vol.bar(date, vol, width=15, color='darkgrey')

    plot_price.yaxis.tick_right()
    plot_price.tick_params(axis='both', **config_ticks)
    plot_price.set_ylabel('Price (in USD)', fontsize=14)
    plot_price.yaxis.set_label_position("right")
    plot_price.yaxis.label.set_color(colors['grey'])
    plot_price.grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.5)
    plot_price.set_axisbelow(True)

    plot_price.spines['top'].set_visible(False)
    plot_price.spines['left'].set_visible(False)
    plot_price.spines['left'].set_color(colors['grey'])
    plot_price.spines['bottom'].set_color(colors['grey'])

    plot_vol.spines['top'].set_visible(False)
    plot_vol.spines['left'].set_visible(False)
    plot_vol.spines['left'].set_color(colors['grey'])
    plot_vol.spines['bottom'].set_color(colors['grey'])

    fig.suptitle(f'{tkr} Price and Volume', size=36, color=colors['grey'], x=0.24, y=1.10)

    b = io.BytesIO()

    plt.savefig(b, format='png')
    plt.close()

    return b


async def check_user_exists(user: str) -> bool:
    async with aiosqlite.connect("d_tabase.db") as db:
        cursor = await db.execute(f'select * from users where username=:user', {'user': user})
        res = await cursor.fetchall()
        rows = [r for r in res]
        if len(rows) < 1:
            return False
        if len(rows) > 1:
            raise Exception(f'Duplicate user with username: {user}')
        else:
            return True
            

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
    msg_tkns = ctx.message.content.split(' ')
    tkr = msg_tkns[0]

    try:
        daysback = msg_tkns[1]
    except ValueError:
        daysback = 30

    try:
        frequency = msg_tkns[2]
    except ValueError:
        frequency = 'd'

    msg = await ctx.channel.send(f"Getting history for {tkr}")
    hist = ws.Stock(tkr).historical(days_back=daysback,
                                    frequency=frequency)

    plot = await get_std_chart(dataframe=hist, tkr=tkr)
    discord.File(plot, filename='plot.png')
    embed = discord.Embed()
    embed.set_image(url="attachment://plot.png")

    await msg.delete()
    await ctx.send(embed=embed, file=plot)


@client.command()
@defaults
async def buy_stock(ctx):
    user = ctx.author.id
    return


@client.command()
@defaults
async def sell_stock(ctx):
    user = ctx.author.id
    return


@client.command()
@defaults
async def balance(ctx):
    user = ctx.author.id
    return


@client.command()
@defaults
async def leaderboard(ctx):
    user = ctx.author.id
    return


client.run(TOKEN)