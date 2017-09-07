import discord
import asyncio
from discord.ext import commands
import pydealer

class Game(object):
    def __init__(self,bot=None, channel=''):
        self.bot = bot
        self.channel = ''
        self.queue = []
        self.ingame = []

    async def game_loop(self, ctx):
        pass
