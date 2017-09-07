#There's likely a much better way to do this
global tracked_players
global ingame_channels
#Store player records in <player id> : Player() pairs.
tracked_players = {}
#Store games in <channel id> : Game() pairs
ingame_channels = {}