import discord
import asyncio
from discord.ext import commands
import configparser
import bot_utilities
from blackjack import Blackjack

config_file = 'bot_cfg.ini'
record_file = 'player_records.json'

config = bot_utilities.load_config(config_file)
bot = commands.Bot(
    command_prefix=commands.when_mentioned,
    description=config.get('bot','description')
)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#Just using sleep for these does NOT seem right.
#Should probably be using a cronjob
async def auto_update_records(filename):
    """Updates player records json file every 3 hours"""
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(10800.0)
        bot_utilities.update_records(filename)

async def auto_give_points():
    """Gives points every 24 hours."""
    await bot.wait_until_ready()
    while not bot.is_closed:
        #Adjust point giving period as needed
        await asyncio.sleep(86400.0)
        bot_utilities.give_points()

#name these for the dc command. Probably a nicer way to do this than naming.
update_task = bot.loop.create_task(auto_update_records(record_file))
give_task = bot.loop.create_task(auto_give_points())

@bot.command(hidden=True, pass_context=True)
async def dc(ctx):
    """Updates records before disconnecting bot"""
    #May want to add in a way to shut down any games
    #in progress
    if ctx.message.author.id == config.get('bot','admin'):
        bot_utilities.update_records(record_file)
        update_task.cancel()
        give_task.cancel()
        await bot.logout()
        print('Disconnecting bot...')

bot_utilities.load_records(bot, record_file)
bot.add_cog(Blackjack(bot))

try:
    bot.run(config.get('bot','token'))
except:
    print('Login error or invalid token in bot config file.')
    exit()
bot_utilities.update_records(record_file)
