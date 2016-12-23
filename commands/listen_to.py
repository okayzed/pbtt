import math
import random
import urllib2
import time

import auth

from mannerisms import *

# beautiful soup4, (apt install python-bs4)
from bs4 import BeautifulSoup

def add_user(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        print "LISTENING TO OWNER!", data["nick"]
        changed = False
        for tok in args:
            if tok in [ "to", "and", "now" ] or tok in FILLWORDS:
                continue

            if tok[0] == "!":
                print "REMOVE USER", tok
                tok = tok[1:]
                if tok in [ "everyone" ]:
                    auth.remove_user("*", data["nick"])
                else:
                    auth.remove_user(tok, data["nick"])

                changed = True
            else:
                if tok in [ "everyone" ]:
                    auth.add_user("*", data["nick"])
                else:
                    print "ADDING USER", tok
                    auth.add_user(tok, data["nick"])
                changed = True

        if changed:
            bot.say("%s: %s %s" % (data["nick"], affirmative(), affirmative()))

    
COMMANDS = {}
COMMANDS["listen"] = add_user
