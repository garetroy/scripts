import discord, asyncio
import requests, json
from discord.ext.commands import Bot

STATE            = False 
BOT_TOKEN        = ""
CHANNEL_ID       = 0 
URL              = "https://api.twitch.tv/kraken/streams" + str(CHANNEL_ID)
TWITCH_CLIENT_ID = ""

bot = Bot(command_prefix=";;")
client = discord.Client()

@bot.event
async def on_read():
    pass

@bot.command()
async def start():
    global STATE
    while(True):
        onlinenow = isonline()
        if(onlinenow != STATE):
            STATE = onlinenow
            if(STATE):
                await bot.say("@everyone Shannon is now Live!")
            else:
                await bot.say("@everyone Shannon just went offline!!")
        await asyncio.sleep(30)

@bot.command()
async def online(*args):
    if isonline():
        return await bot.say("Shannon is online")
    else:
        return await bot.say("Shannon is not online")

def isonline():     
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': TWITCH_CLIENT_ID
          }

    r = requests.get(URL,headers=headers)
    if r.json()['stream']:
        return True
    return False

bot.run(BOT_TOKEN)
