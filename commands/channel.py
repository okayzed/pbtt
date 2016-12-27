import math
import random
import urllib2
import time

import algos
import auth

from mannerisms import *
import ircbot

def leave_channel(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        for arg in args:
            if arg[0] == "#":
                arg = arg.replace("?", "").replace("!", "")
                # try to join this channel
                print "LEAVING CHANNEL %s (BC OF %s) " % (arg, data["nick"])
                rsp.bot.send("PART", arg)
        rsp.say("%s: %s" % (data["nick"], affirmative()))

def join_channel(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        for arg in args:
            if arg[0] == "#":
                arg = arg.replace("?", "").replace("!", "")
                # try to join this channel
                print "JOINING CHANNEL %s (BC OF %s) " % (arg, data["nick"])
                rsp.bot.send("JOIN", arg)
        rsp.say("%s: %s" % (data["nick"], affirmative()))

def changename(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        nick = args[0]
        print "CHANGING NICK TO", nick

        rsp.bot.botnick = nick
        rsp.bot.send("NICK", nick)

COMMANDS = {}
COMMANDS["join"] = join_channel
COMMANDS["leave"] = leave_channel
COMMANDS["changename"] = changename
