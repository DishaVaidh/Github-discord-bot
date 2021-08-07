import discord
from discord.ext import commands, tasks
import datetime
from dateutil.tz import gettz
import pandas as pd
import time
import asyncio
from multiprocessing import Process

from github import git
git()

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all()

bot=commands.Bot(command_prefix='!',intents=intents)

@tasks.loop(hours = 6.0)
async def send_message():
  df = pd.read_csv('update.csv')
  repo_url = list(df['Updated Files'])
  folder_list = bot.get_guild(864499877723504640).categories
  for folder in folder_list:
    if folder.name.startswith('SP'):
      channel_list = folder.channels
      for i in channel_list:
        if i.name == 'general':
          if "['"+folder.name+'/README.md'+"']" in repo_url:
            pass
          else:
            print("\"['"+folder.name+'/README.md'+"']\"")
            roles = bot.get_guild(864499877723504640).roles
            role_ = [role for role in roles if role.name==folder.name]
            await bot.get_channel(i.id).send("<@&"+str(role_[0].id)+'>  We did not recieved your daily report for today on Github. Please upload the report.')

@bot.event
async def on_ready():
  print("I am",bot.user)
  send_message.start()

def discord_bot():
  bot.run('ODY0OTA0MTY4ODYxNzI4ODM5.YO8Oxg.mdC4Mz6WZurnsnP13iKqh0Xkxh4')

discord_bot()