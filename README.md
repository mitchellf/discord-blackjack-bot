# Discord Blackjack Bot

This is a simple [discord](https://discordapp.com/) blackjack bot made using the [discord.py](https://github.com/Rapptz/discord.py) api wrapper, the [pydealer](https://github.com/Trebek/pydealer) package, and [python](https://www.python.org/).

Up to five users can play in a casino style blackjack game with the bot acting as a dealer. The game features a queue system for larger servers and records user points (i.e. chips or money) in a file for long-term play. Users are also given points periodically. This bot supports play on multiple channels at a time.

This was developed mainly to expirement with python, bots, and remote hosting.

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

As a note this was developed using the current `async` branch of `discord.py`.

#### Bot

You can create a discord bot for your server [here](https://discordapp.com/developers/applications/me#top). Check out [this](https://discordapp.com/developers/docs/intro) and [this](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) for more information.

Clone this repository or or download [here]().
In the bot directory edit the `bot_cfg.ini` to add/modify:
* ```token = <bot token>``` (required).
* ```description = <your custom description>``` (optional).
This is added to the default help command.

## Usage

Once you have the dependencies installed and `bot_cfg.ini` properly configured, run the bot using:
```
$ python bot.py
```
Use `@<bot_name> help` in discord for help with available commands.

## Comments

I am quite new to programming in general and this project likely contains lots of bugs/errors. Feel free to expand on it or create a new bot in its likeness. If you have questions, comments, advice, or other open an [issue](https://github.com/mitchellf/discord-blackjack-bot/issues/new), I'd love to hear it.

Thanks!