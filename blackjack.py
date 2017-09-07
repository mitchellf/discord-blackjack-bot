import discord
import asyncio
from discord.ext import commands
import pydealer
from player import Player
from global_vars import tracked_players, ingame_channels
from game import Game

class Blackjack(object):
    def __init__(self,bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=10)
    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Join a blackjack game queue.

        Attempts to add user to queue blackjack of a blackjack game in
        progress. Command has a 10 second cooldown.
        """
        #Nested ifs since it's a long messy condition
        #Check if game in progress in user channel, then
        #check if user is already in that game queue or ingame
        if ctx.message.channel.id in ingame_channels:
            user_id = ctx.message.author.id
            channel_id = ctx.message.channel.id
            if (not (user_id in ingame_channels[channel_id].queue
                    and user_id in ingame_channels[channel_id].ingame)):
                ingame_channels[channel_id].queue.append(user_id)

    @commands.cooldown(rate=1, per=15)
    @commands.command(pass_context=True)
    async def start(self, ctx):
        """Start a blackjack game.

        Starts a new game of blackjack if there is not already a game in
        progress in the user's current channel. Automatically adds  user to
        game queue. Command has a 15 second cooldown.
        """

        global tracked_players
        global ingame_channels
        #Check for game in channel
        if ctx.message.channel.id in ingame_channels:
            return
        ingame_channels[ctx.message.channel.id]  = (
            Game(self.bot, ctx.message.channel.id)
        )
        ingame_channels[ctx.message.channel.id].queue = (
            [ctx.message.author.id]
        )
        await ingame_channels[ctx.message.channel.id].game_loop(ctx)
        await self.add_to_tracked(ctx.message.author.id)
        await self.bot.say('Thanks for playing!')

    async def add_to_tracked(self, id):
        """Adds player to tracked_players if not already present

        keyword arguments:
        id -- str, id of user to add to tracked_players
        """
        global tracked_players
        if not tracked_players.get(id):
            user =  await self.bot.get_user_info(id)
            tracked_players[id] = Player(
                id, user.name, str(user.discriminator)
            )
            tracked_players[id].score = 200
            tracked_players[id].wins = 0