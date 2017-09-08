import discord
import asyncio
from discord.ext import commands
import pydealer
from player import Player

suit_map = {'Diamonds': '\u2662',
            'Clubs': '\u2667',
            'Hearts': '\u2661',
            'Spades': '\u2664' }

class Game(object):
    def __init__(self,bot=None, channel=''):
        self.bot = bot
        self.channel = ''
        self.queue = []
        self.ingame = []
        self.dealer = Player(self.bot.user.id,self.bot.user.name)
        self.dealer.score = 2000
        self.deck = pydealer.Deck()

    def game_display(self):
        """Generates game display text"""
        return_text = ((
            'Use \'join\' command to join the game. Use \'leave\' command'
            'to leave the game at the end of the round.\n'
            'In queue: {0}. In game: {1}.\n'
            'After two rounds of invalid/no reponse you are removed from '
            ' the game.\n'
            'The minimum bet is 5 points, the max bet is 500 points.\n'
            '============================\n```py\n'
            ).format(str(len(self.queue)),str(len(self.ingame)))
        )
        for player in ([self.dealer] + self.ingame):
            return_text += ((
                '\n{0:20.20} value: {1:' '>2}, '
                'bet: {2:' '>3}, score: {3:' '>11}\n'
                '{4}\n{5}\n'
                ).format(
                    player.name,
                    str(player.value),
                    str(player.bet),
                    str(player.score),
                    self.hand_display(player.hand),
                    player.status_text
                )
            )
        return return_text + '\n```'

    async def game_loop(self, ctx):
        """Handles main blackjack round loop"""
        global ingame_channels
        game_msg = await self.bot.say('Starting blackjack in 15 seconds.\n'
            'Use \'join\' command to join the queue.'
        )
        await asyncio.sleep(1.0)
        await self.bot.delete_message(game_msg)
        while (self.queue or self.ingame) and self.dealer.score>0:
            #Populate ingame from queue
            if len(self.ingame) < 5:
                for i in range(0,min(5-len(self.ingame),len(self.queue))):
                    self.ingame.append(self.queue.pop(0))
            game_msg = await self.bot.say(self.game_display())
            #Get bets from players
            for player in self.ingame:
                prompt_msg = await self.bot.say(
                    ('__*{0}*__ , please enter valid bet '
                    'amount within 10 seconds.\n'
                    'Bets must be positive integer amounts.'
                    ).format(player.name)
                )
                response_msg = await self.bot.wait_for_message(
                    timeout = 10,
                    #lambda to check for author since I want to avoid using
                    #bot.get_user_info() calls
                    check = (lambda message: message.author.id == player.id)
                )
                #Might be able to fit this into the lambda. Could also
                #clean this up
                if response_msg:
                    try:
                        int(response_msg.content)
                        if (5 <= int(response_msg.content)
                                <= min(player.score,500)):
                            player.no_response = 0
                            player.bet = int(response_msg.content)
                            player.score -= player.bet
                        else:
                            player.no_response += 1
                    except:
                        player.no_response += 1
                else:
                    player.no_response += 1
                await self.bot.delete_message(prompt_msg)
            break
        
    def hand_display(self, hand):
        """Returns text card display for hand

        keyword arguments:
        hand -- pydealer stack, players' hand
        """
        if not hand:
            return ''
        return_text = ''
        rank = ''
        suit = ''
        for card in hand:
            suit = suit_map[card.suit]
            if pydealer.const.DEFAULT_RANKS['values'][card.value] >= 10:
                rank = card.value[0]
            else:
                rank = card.value
            return_text += '| {0:2.2} {1} | '.format(rank,suit)

        return return_text