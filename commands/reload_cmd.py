import math
import random
import urllib2
import time

import algos
import auth

from mannerisms import *
import ircbot
import reloadables

def reload_bot(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        import commands, interactions
        print "RELOADING (BC OF %s) " % data["nick"]

        reload(ircbot)
        reload(reloadables)
        reloadables.load()

    bot.say(affirmative())

# TODO: actually create a new instance of the bot with a different lock
def hand_forward(oldbot):
    newbot = ircbot.IRC_Bot()
    print "HANDING BOT FORWARD", oldbot, newbot
    newbot.server = oldbot.server
    newbot.port = oldbot.port
    newbot.channel = oldbot.channel
    newbot.botnick = oldbot.botnick
    newbot.password = oldbot.password


    if hasattr(oldbot, 'history'):
        newbot.history = oldbot.history

    if hasattr(oldbot, 'members'):
        newbot.members = oldbot.members

    oldbot.expired = True
    if hasattr(oldbot, 'irc'):
        newbot.irc = oldbot.irc

    return newbot

def transfer_bot(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        reload_bot(bot, data, *args)
        newbot = hand_forward(bot.bot)
        newbot.run_forever()

        # we raise this so we can quit when the bot finally does finish
        raise ircbot.BotTransferException()

def resurrect_bot(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        reload_bot(bot, data, *args)
        newbot = hand_forward(bot.bot)

        bot.send("QUIT")
        newbot.connect()
        newbot.run_forever()

        raise ircbot.BotTransferException()


COMMANDS = {}
COMMANDS["reload"] = reload_bot
COMMANDS["upd8"] = reload_bot
COMMANDS["update"] = reload_bot

COMMANDS["reconnect"] = resurrect_bot
COMMANDS["reincarnate"] = transfer_bot
