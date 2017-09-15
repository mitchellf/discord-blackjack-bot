# Discord Blackjack Bot

> ### [Invite blackjack_bot!](https://discordapp.com/oauth2/authorize?client_id=355590976686784514&scope=bot&permissions=0)

This is a simple [discord](https://discordapp.com/) blackjack bot made using the [discord.py](https://github.com/Rapptz/discord.py) api wrapper, the [pydealer](https://github.com/Trebek/pydealer) package, and [python](https://www.python.org/).

Up to five users per channel can play in a casino style blackjack game with the bot acting as a dealer. The game features a queue system for larger channels/servers and records user points (i.e. chips or money) in a file for long-term play. Users are also given points periodically. This bot supports play on multiple channels at a time.

This was developed mainly to experiment with python, bots, and remote hosting.

![](/sample_play.png "Example of bot interface.")

## Dependencies

* [python](https://www.python.org/) 3.4.2+
* [discord.py](https://github.com/Rapptz/discord.py)
* [pydealer](https://github.com/Trebek/pydealer)

## Installation

#### Dependencies

Both [discord.py](https://github.com/Rapptz/discord.py) and [pydealer](https://github.com/Trebek/pydealer) are available via `pip`.

```
$ pip install discord.py
```

```
$ pip install pydealer
```

#### Bot

You can create a discord bot for your server [here](https://discordapp.com/developers/applications/me#top). Check out [this](https://discordapp.com/developers/docs/intro) and [this](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) for more information.

[Clone](https://github.com/mitchellf/discord-blackjack-bot.git) this repository or [download](https://github.com/mitchellf/discord-blackjack-bot/archive/master.zip) files.
In the bot directory edit the `bot_cfg.ini` to add/modify:
* ```token = <bot token>``` (required).
* ```description = <your custom description>``` (optional).
This is added to the default help command.

You may also want to edit/customize:
* give point period in the `auto_give_points` function in `bot.py`.
* method and class docstrings of the `Blackjack` class in `blackjack.py`.

## Usage

Once you have the dependencies installed and `bot_cfg.ini` properly configured, run the bot using:
```
$ python bot.py
```
Use `@<bot_username> help` in discord for help with available commands.

## Comments

I am quite new to programming in general and this project likely contains lots of bugs/errors. Feel free to expand on it or create a new bot in its likeness. If you have questions, comments, advice, or other open an [issue](https://github.com/mitchellf/discord-blackjack-bot/issues/new), I'd love to hear it.

Thanks!
