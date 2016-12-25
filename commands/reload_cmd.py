import math
import random
import urllib2
import time

import algos
import auth

from mannerisms import *
import ircbot

def reload_bot(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        import commands, interactions
        print "RELOADING (BC OF %s) " % data["nick"]

        reload(ircbot)
        ircbot.load()

        # TODO: actually create a new instance of the bot with a different lock
        def hand_forward(old_bot):
            newbot = ircbot.IRC_Bot()
            print "HANDING BOT FORWARD", old_bot, newbot
            newbot.server = old_bot.server
            newbot.port = old_bot.port
            newbot.channel = old_bot.channel
            newbot.botnick = old_bot.botnick
            newbot.password = old_bot.password
            newbot.irc = old_bot.irc

            newbot.s_mutex = old_bot.s_mutex
            newbot.run_forever()

            # we raise this so we can quit when the bot finally does finish
            raise ircbot.BotTransferException()

        bot.say(affirmative())

        # TODO: make this safe to hand forward somehow
#        hand_forward(bot.bot)


    
COMMANDS = {}
COMMANDS["reload"] = reload_bot
COMMANDS["upd8"] = reload_bot
COMMANDS["update"] = reload_bot

