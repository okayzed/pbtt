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

COMMANDS = {}
COMMANDS["join"] = join_channel
COMMANDS["leave"] = leave_channel
