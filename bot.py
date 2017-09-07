import discord
from discord.ext import commands
import configparser
import bot_utilities
import game

config = bot_utilities.load_config('bot_cfg.ini')
bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

game.load_records(bot)

try:
    bot.run(config.get('bot','token'))
except:
    print('Login error or invalid token in bot config file.')
    exit()

game.update_records(bot)
with open('bot_cfg.ini','w') as cfg_file:
    config.write(cfg_file)