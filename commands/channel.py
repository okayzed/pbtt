import math
import random
import urllib2
import time

import algos
import auth

from mannerisms import *
import ircbot

import parser

def leave_channel(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        for arg in args:
            if arg[0] == "#":
                arg = arg.replace("?", "").replace("!", "")
                # try to join this channel
                print "LEAVING CHANNEL %s (BC OF %s) " % (arg, data["nick"])
                rsp.bot.leave_channel(arg)
        rsp.say("%s: %s" % (data["nick"], affirmative()))

def join_channel(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        for arg in args:
            if arg[0] == "#":
                arg = arg.replace("?", "").replace("!", "")
                # try to join this channel
                print "JOINING CHANNEL %s (BC OF %s) " % (arg, data["nick"])
                rsp.bot.join_channel(arg)
        rsp.say("%s: %s" % (data["nick"], affirmative()))

def who_channel(rsp, data, *args):
    if data["nick"] in auth.OWNERS:
        rsp.bot.send("WHO", data["channel"])


def stalk_user(rsp, data, *args):
    wait_small()
    if data["nick"] in auth.ALLOWED:
        from geoip import geolite2
        nick = args[0].lower()
        print "STALKING", nick
        for channel in rsp.bot.members:
            members = rsp.bot.members[channel]
            if nick in members:
                sendername = members[nick]
                print "FOUND", sendername
                name, hostname = sendername.split("!")[:2]
                ip = None
                try:
                    _, ip = hostname.split("@")
                except: 
                    ip = hostname

                match = None

                try:
                    match = geolite2.lookup(ip or hostname)
                except ValueError, e:
                    pass

                if not match:
                    import socket
                    try:
                        ip = socket.gethostbyname(ip)
                    except Exception, e:
                        print e
                        rsp.say("%s: %s is too hidden for that" % (data["nick"], nick))

                        return

                    match = geolite2.lookup(ip)

                print "MATCH IS", match

                if match:
                    rsp.say("%s: %s is somewhere in %s" % (data["nick"], nick, match.country))
                    break


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
COMMANDS["!who"] = who_channel

COMMANDS["geolocate"] = stalk_user
COMMANDS["geofind"] = stalk_user
COMMANDS["geostalk"] = stalk_user
