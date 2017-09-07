from global_vars import tracked_players

class Player(object):
    def __init__(self, id='', name='', discriminator=''):
        self.id = id
        self.name = name
        self.discriminator = discriminator
        self.score = 0
        self.wins = 0