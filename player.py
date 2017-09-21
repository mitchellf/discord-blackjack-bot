import pydealer
from global_vars import tracked_players

class Player(object):
    def __init__(self, id=''):
        self.id = id
        self.hand = None
        self.status_text = ''
        self.bet = 0
        self.value = 0
        self.score = 0
        self.wins = 0
        self.no_response = 0
        self.request_leave = False
        self.playing = False

    def calculate_value(self):
        """Calculates value of player's hand"""
        if not self.hand:
            return 0
        num_aces = 0
        total_value = 0
        for card in self.hand:
            if pydealer.const.DEFAULT_RANKS['values'][card.value] == 13:
                num_aces += 1
                total_value += 11
            elif pydealer.const.DEFAULT_RANKS['values'][card.value] >= 10:
                total_value += 10
            else:
                total_value += int(card.value)

        while num_aces > 0 and total_value > 21:
                total_value -= 10
                num_aces -= 1
        return total_value