import discord
import asyncio
from discord.ext import commands
import configparser
import bot_utilities
import game

config = bot_utilities.load_config('bot_cfg_test.ini')
bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def auto_update_records(filename):
    """Updates player records json file hourly"""
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(3600)
        game.update_records(bot,filename)

game.load_records(bot, 'player_records_test.json')
bot.loop.create_task(auto_update_records('player_records_test.json'))
try:
    bot.run(config.get('bot','token'))
except:
    print('Login error or invalid token in bot config file.')
    exit()

game.update_records(bot, 'player_records_test.json')
with open('bot_cfg_test.ini','w') as cfg_file:
    config.write(cfg_file)