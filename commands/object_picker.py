import math
import random
import urllib2
import time

import algos
import parser

from mannerisms import *

# beautiful soup4, (apt install python-bs4)
from bs4 import BeautifulSoup

ALLOW_HR_CATEGORIES = [
    "algorithms",
]

OBJECTS = {
    "problem" : algos.ALGO_SITES
}


# OBJECT PICKER SYNTAX IS:
# [pick|find|suggest] a <object>
# ABOUT topic words
# FROM site

# examples:
# pick a problem about easy #dynamic algorithms from hackerrank
# pick a problem from hackerrank about algorithms #dynamic (easy or medium, please)
# can you suggest a problem about math and #combinatorics (easy only) from hackerrank?
# pick an easy problem from hackerrank
# pick a hard problem from hackerrank

def pick_random_object(bot, cmd, *args):
    pick_from = []
    not_from = []

    nono = False
    obj = None
    prev_token = None
    for arg in args:
        if arg == "not" or arg == "but":
            continue

        for o in OBJECTS:
            if arg.lower().find(o.lower()) != -1:
                obj = o
                break

        if obj:
            break
        prev_token = arg

    if not obj in OBJECTS:
        bot.say("What?")
        return


    sites = parser.Section(
        tokens=["from"], 
        default="hackerrank",
        defaults=OBJECTS[obj],
        prefix="^")
    topics = parser.Section(
        tokens=["about", "thats", "that"], 
        prefix="$")
    subcat = parser.Section(
        prefix="#")

    # i need to change "easy OBJECT" to "OBJECT thats easy"
    # so that i can say: "give me an easy problem"
    # TODO: do this by adding prev_token to topics if it is a topic for obj
    # right now, we do it always

    if prev_token:
        topics.topics.append(prev_token)

    parser.keyword_seperate(args, keywords=[sites, topics, subcat])
    pick_from = list(set(sites.topics) - set(sites.ignore))
    site = random.choice(pick_from)

    for cat in subcat.topics:
        topics.topics.append("#" + cat)

    print "PICKING FROM", site
    def next_step():

        if len(pick_from) == 1:
            bot.say("%s" % (hold_on().strip()))
        else:
            bot.say("%s" % (hold_on().strip()))


        def pick_obj():
            try:
                OBJECTS[obj][site](bot, topics.topics)
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
