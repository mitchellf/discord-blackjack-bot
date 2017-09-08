import discord
import asyncio
from discord.ext import commands
import json
import configparser
from player import Player
from global_vars import tracked_players

async def load_records(bot, filename):
    """Loads player records from player_records.json
    into tracked_players.

    keyword arguments:
    bot -- Bot object
    filename -- str, json filename containing player records
    """
    global tracked_players
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for id in data:
                user =  await bot.get_user_info(id)
                tracked_players[id] = Player(
                    id, user.name, str(user.discriminator)
                )
                tracked_players[id].score = data[id]["score"]
                tracked_players[id].wins = data[id]["wins"]
    #Need to make this more detailed/informative
    except:
        print('Error loading player records.')
        exit()

def update_records(filename):
    """Updates player_records.json from tracked_players
    dictionary

    keyword arguments:
    bot -- Bot object
    """
    global tracked_players
    data = {}
    with open(filename,'w') as f:
        for player in tracked_players:
            data[player] = (
                {"score": tracked_players[player].score,
                "wins": tracked_players[player].wins}
            )
        json.dump(data,f)

def load_config(filename):
    """Loads and reads config file.

    keyword arguments:
    filename -- str, config file name
    
    returns a valid ConfigParser() object
    """
    config = configparser.ConfigParser()
    try:
        with open(filename, 'r') as f:
            config.read_file(f)
        if not config.get('bot','token'):
            raise ValueError
    except (OSError, IOError, FileNotFoundError):
        print('Bot config file \'{}\' not found.'.format(filename))
        exit()
    except ValueError:
        print('Bot token not found. Place in config file as\n'
                'token = <bot token>'
        )
        exit()

    return config