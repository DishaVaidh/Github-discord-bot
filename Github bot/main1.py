import discord
from discord.ext import commands, tasks
import datetime
from dateutil.tz import gettz
import pandas as pd
import time
import asyncio
from multiprocessing import Process

from github import git
import nest_asyncio
nest_asyncio.apply()

#git()

intents = discord.Intents.all()

bot=commands.Bot(command_prefix='!',intents=intents)

@tasks.loop(hours = 1.0)
async def send_message():
  df = pd.read_csv('update.csv')
  repo_url = list(df['updated'])
  channel_list = bot.guilds[0].text_channels
  for i in channel_list:
    if i.name not in ['general','welcome-and-rules','notes-resources','homework-help','session-planning','off-topic']:
      if "['"+i.name+'/a.txt'+"']" in repo_url:
        pass
      else:
        print("\"['"+i.name+'/a.txt'+"']\"")
        await bot.get_channel(i.id).send("Please upload your daily report!")

@bot.event
async def on_ready():
  print("I am",bot.user)
  send_message.start()
  '''p3 = Process(target=cur_time)
  p3.start()'''

'''@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content.startswith("$check"):
    await cur_time()'''

def discord_bot():
  bot.run('ODY0OTA0MTY4ODYxNzI4ODM5.YO8Oxg.mdC4Mz6WZurnsnP13iKqh0Xkxh4')

'''async def cur_time():
  ct = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
  if ct.hour <= 12:
    df = pd.read_csv('update.csv')
    repo_url = list(df['updated'])
    channel_list = bot.guilds[0].text_channels
    for i in channel_list:
      if i.name not in ['general','welcome-and-rules','notes-resources','homework-help','session-planning','off-topic']:
        if "['"+i.name+'/a.txt'+"']" in repo_url:
          pass
        else:
          print("\"['"+i.name+'/a.txt'+"']\"")
          await bot.get_channel(i.id).send("Please upload your daily report!")'''

def main():
  p1 = Process(target=git)
  p2 = Process(target=discord_bot)
  p1.start()
  p2.start()
  
main()