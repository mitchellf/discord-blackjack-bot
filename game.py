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
    def __init__(self,bot=None, server=None):
        self.bot = bot
        self.server = server
        self.queue = []
        self.ingame = []
        self.dealer = Player(self.bot.user.id)
        self.dealer.score = 2000
        self.deck = pydealer.Deck()

    def deal_cards(self):
        """Deal cards to dealer and players.

        Dealer only recieves one card at this stage. This simulates the dealer
        only showing one card.
        """
        self.deck.shuffle(5)
        self.dealer.hand = self.deck.deal(1)
        self.dealer.value = self.dealer.calculate_value()
        for player in self.ingame:
            if player.bet != 0:
                player.hand = self.deck.deal(2)
                player.value = player.calculate_value()

    async def do_dealer_turn(self, ctx):
        """Run through the dealers turn. Delays added for dramatic effect."""
        game_msg = await self.bot.say(self.game_display())
        #Check for all blackjack, all bust, or all no bet
        if (any([player.value < 21 for player in self.ingame])
                and all([player.bet != 0 for player in self.ingame])):
            prompt_msg = await self.bot.say('Dealer turn.')
            self.dealer.hand += self.deck.deal(1)
            self.dealer.value = self.dealer.calculate_value()
            game_msg = await self.bot.edit_message(
                game_msg,
                self.game_display()
            )
            await asyncio.sleep(3.0)
            while(self.dealer.value < 17):
                prompt_msg = await self.bot.edit_message(
                    prompt_msg,
                    'Dealer hits!'
                )
                self.dealer.hand += self.deck.deal(1)
                self.dealer.value = self.dealer.calculate_value()
                game_msg = await self.bot.edit_message(
                    game_msg,
                    self.game_display()
                )
                await asyncio.sleep(4.0)
            prompt_msg = await self.bot.edit_message(
                prompt_msg,
                'Dealer stays.'
            )
            if prompt_msg:
                await self.bot.delete_message(prompt_msg)
        await self.bot.delete_message(game_msg)

    async def do_player_turns(self, ctx):
        """Run through the players turns."""
        for player in self.ingame:
            if player.bet == 0: continue
            game_msg = await self.bot.say(self.game_display())
            prompt_msg = await self.bot.say(
                ('__*{0}*__, hit or stay? Please enter \'h\' for hit '
                'or \'s\' for stay within 10 seconds.'
                ).format(self.server.get_member(player.id).display_name)
            )
            while player.value < 21 and player.hand.size < 6:
                game_msg = await self.bot.edit_message(
                    game_msg,
                    self.game_display()
                )
                response_msg = await self.bot.wait_for_message(
                    timeout = 10,
                    check = (lambda message: message.author.id == player.id)
                )
                if (response_msg):
                    if ((response_msg.content.strip())[0].upper() == 'H'):
                        player.hand += self.deck.deal(1)
                        player.value = player.calculate_value()
                    else: break
                else: break
            await self.bot.delete_message(prompt_msg)
            await self.bot.delete_message(game_msg)

    async def endround(self, ctx):
        """Runs end round calculation and messages."""
        game_msg = await self.bot.say(self.game_display())
        if self.dealer.value == 21:
                self.dealer.status_text = '\'\'\'Got blackjack!\'\'\''
        elif self.dealer.value > 21:
            self.dealer.status_text = '\'\'\'Busted!\'\'\''
        for player in self.ingame:
            #Skip those who didn't play
            if player.bet == 0:
                continue
            #Can probably clean this up
            if player.value == 21 and self.dealer.value != 21:
                player.status_text = '\'\'\'Got blackjack!\'\'\''
                player.score += round(2.5*player.bet)
                player.wins += 1
            elif (player.value < 21 
                    and (self.dealer.value < player.value
                        or self.dealer.value > 21)):
                player.status_text = '\'\'\'Won!\'\'\''
                player.score += 2*player.bet
                player.wins += 1
            elif player.value < 21 and player.value < self.dealer.value:
                player.status_text = '\'\'\'Lost.\'\'\''
                self.dealer.score += player.bet
            elif player.value > 21:
                player.status_text = '\'\'\'Busted\'\'\''
                self.dealer.score += player.bet
            else:
                player.status_text = '\'\'\'Push.\'\'\''
                player.score += player.bet
        game_msg = await self.bot.edit_message(
            game_msg,
            self.game_display()
        )
        #Reset game related
        self.deck += self.dealer.hand.empty(return_cards=True)
        self.dealer.status_text = ''
        self.dealer.value = 0
        for player in self.ingame:
            player.bet = 0
            player.value = 0
            player.status_text = ''
            if player.hand:
                self.deck += player.hand.empty(return_cards=True)
            if (player.score <= 0
                    or player.no_response >= 2
                    or player.request_leave):
                self.ingame.remove(player)
                player.no_response = 0
                player.request_leave = False
                player.playing = False
        for player in self.queue:
            if player.request_leave:
                self.queue.remove(player)
                player.request_leave = False
                player.playing = False
        await asyncio.sleep(5.0)
        await self.bot.delete_message(game_msg)

    def game_display(self):
        """Generates game display text"""
        return_text = ((
            'Use `join` command to join the game. Use `leave` command '
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
                    self.server.get_member(player.id).display_name,
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
            'Use `join` command to join the queue.'
        )
        await asyncio.sleep(15.0)
        await self.bot.delete_message(game_msg)
        while (self.queue or self.ingame) and self.dealer.score>0:
            self.populate_game()
            await self.get_bets(ctx)
            self.deal_cards()
            await self.do_player_turns(ctx)
            await self.do_dealer_turn(ctx)
            await self.endround(ctx)

    async def get_bets(self, ctx):
        """Get bets from players."""
        game_msg = await self.bot.say(self.game_display())
        for player in self.ingame:
            await self.bot.edit_message(game_msg,self.game_display())
            prompt_msg = await self.bot.say(
                ('__*{0}*__ , please enter valid bet '
                'amount within 10 seconds.\n'
                'Bets must be positive integer amounts.'
                ).format(self.server.get_member(player.id).display_name)
            )
            response_msg = await self.bot.wait_for_message(
                timeout = 11,
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
                    else: player.no_response += 1
                except: player.no_response += 1
            else: player.no_response += 1
            await self.bot.delete_message(prompt_msg)
        await self.bot.delete_message(game_msg)

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

    def populate_game(self):
        """Populate ingame from queue"""
        if len(self.ingame) < 5:
            for i in range(0,min(5-len(self.ingame),len(self.queue))):
                self.ingame.append(self.queue.pop(0))
        