import discord
from discord.ext import commands
import configparser
import bot_utilities

config = bot_utilities.load_config('bot_cfg_test.ini')
bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

try:
    bot.run(config.get('bot','token'))
except:
    print('Login error or invalid token in bot config file.')
    exit()

with open('bot_cfg_test.ini','w') as cfg_file:
    config.write(cfg_file)