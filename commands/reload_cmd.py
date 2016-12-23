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

        ircbot.load()
    
COMMANDS = {}
COMMANDS["reload"] = reload_bot
COMMANDS["upd8"] = reload_bot
COMMANDS["update"] = reload_bot

