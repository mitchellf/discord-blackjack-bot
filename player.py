from global_vars import tracked_players

class Player(object):
    def __init__(self, id='', name='', discriminator=''):
        self.id = id
        self.name = name
        self.discriminator = discriminator
        self.hand = None
        self.status_text = ''
        self.bet = 0
        self.value = 0
        self.score = 0
        self.wins = 0
        self.no_response = 0