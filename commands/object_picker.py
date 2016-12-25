import math
import random
import urllib2
import time

import algos

from mannerisms import *

# beautiful soup4, (apt install python-bs4)
from bs4 import BeautifulSoup

ALLOW_HR_CATEGORIES = [
    "algorithms",
]

OBJECTS = {
    "algorithm" : algos.ALGO_SITES
}


# OBJECT PICKER SYNTAX IS:
# [pick|find|suggest] a <object>
# ABOUT topic words
# FROM site

# examples:
# pick a problem about easy #dynamic algorithms from hackerrank
# pick a problem from hackerrank about algorithms #dynamic (easy or medium, please)
# can you suggest a problem about math and #combinatorics (easy only) from hackerrank?

def pick_random_object(bot, cmd, *args):
    print "PICKING RANDOM ALGO"

    pick_from = []
    not_from = []

    nono = False
    obj = None
    for arg in args:
        if arg == "not" or arg == "but":
            continue

        if not obj:
            for o in OBJECTS:
                if o.find(arg.lower()):
                    obj = o
                    break

            if obj:
                continue


    if not obj in OBJECTS:
        self.say("What?")
        return


    sites = OBJECTS[obj]
    topics = []
    from_ = True
    topic = False
    import string
    for arg in args:
        arg = arg.lower()
        arg = arg.translate(None, string.punctuation.replace("#", ""))
        if arg == "not" or arg == "but":
            nono = True
            continue

        if arg == "about" or arg == "that" or arg == "thats" or arg == "make":
            topic = True
            from_ = False
            continue

        if arg == "from":
            from_ = True
            topic = False
            continue



        if len(arg) < 3:
            continue

        if topic or arg[0] == "#":
            topics.append(arg)
        elif from_:
            for k in sites:
                if k.find(arg) != -1:
                    if nono:
                        not_from.append(k)
                    else:
                        pick_from.append(k)

    if len(pick_from) == 0:
        pick_from = set(sites.keys()) - set('leetcode')

    print "AVAILABLE SITES", pick_from

    pick_from = list(set(pick_from) - set(not_from))

    site = random.choice(pick_from)

    print "PICKING PROBLEM FROM...", site
    def next_step():

        if len(pick_from) == 1:
            bot.say("%s" % (hold_on().strip()))
        else:
            bot.say("%s" % (hold_on().strip()))


        def pick_obj():
            try:
                sites[site](bot, topics)
            except Exception, e:
                print "EXC:", e
                bot.say("%s: %s" % (cmd["nick"], huh()))

        wait_large(pick_obj)

    wait_small(next_step)

COMMANDS = {}
COMMANDS["pick"] = pick_random_object
COMMANDS["give"] = pick_random_object
COMMANDS["find"] = pick_random_object
COMMANDS["suggest"] = pick_random_object
