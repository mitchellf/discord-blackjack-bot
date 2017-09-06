import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read('bot_cfg.ini')
if not config.get('bot','token'):
    raise ValueError('Missing bot token.')
bot = commands.Bot(command_prefix=commands.when_mentioned())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(config.get('bot','admins'))

with open('bot_cfg.ini','w') as cfg_file:
    config.write(cfg_file)