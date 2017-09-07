import json
import player

#Store player records in <player id> : Player() pairs.
tracked_players = {}

def load_records(bot):
    global tracked_players
    try:
        with open('player_records.json', 'r') as f:
            data = json.load(f)
            for id in data:
                tracked_players[id] = player.Player()
                tracked_players[id].user = bot.get_user_info(id)
                tracked_players[id].score = data[id]["score"]
                tracked_players[id].wins = data[id]["wins"]
    except:
        print('Error loading player records.')
        exit()

class Game(object):
    pass