import discord
import asyncio
from discord.ext import commands
import configparser
import bot_utilities
from blackjack import Blackjack

config = bot_utilities.load_config('bot_cfg.ini')
bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot_utilities.load_records(bot, 'player_records.json')

#Just using sleep for these does NOT seem right.
#Should probably be using a cronjob
async def auto_update_records(filename):
    """Updates player records json file every 3 hours"""
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(10800.0)
        bot_utilities.update_records(filename)

async def auto_give_points():
    """Gives points every 12 hours."""
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(43200.0)
        bot_utilities.give_points()

bot.loop.create_task(auto_update_records('player_records.json'))
bot.loop.create_task(auto_give_points())
bot.add_cog(Blackjack(bot))
try:
    bot.run(config.get('bot','token'))
except:
    print('Login error or invalid token in bot config file.')
    exit()
bot_utilities.update_records('player_records.json')
with open('bot_cfg.ini','w') as cfg_file:
    config.write(cfg_file)