
import math
import random
import urllib2
import time

from bs4 import BeautifulSoup

from mannerisms import *
import re
import string
import auth
import pickle
import helpers

def regex_contains(parent, regex):
    parent = parent.lower()
    m = re.match(regex, str(parent).translate(None, " "))
    return m != None


DEFAULT_SOLVERS = {
    "dbqpdb" : "oky"
}

SOLVERS = {}

def add_user(username, handle):
    print "ADDING USER", username, handle
    if not username in SOLVERS:
        SOLVERS[username] = handle

    save_users()

def remove_user(username, by):
    if username in SOLVERS:
        del SOLVERS[username]

    save_users()

def _reload():
    solvers = helpers.load_data_for_module(__name__, "solvers", SOLVERS)
    SOLVERS.clear()
    for a in solvers:
        SOLVERS[a] = solvers[a]

    if not SOLVERS:
        SOLVERS.update(DEFAULT_SOLVERS)

    print "LOADED HR SOLVERS:", SOLVERS

def save_users():
    helpers.save_data_for_module(__name__, "solvers", SOLVERS)

def has_solved_problem(bot, cmd_data, *args):
    bot.say("Sorry, HR banned me for a bit :-(");
    return

    import time, json
    now = str(time.time()*1000)

    offset = 0

    args = [ arg.replace("-", " ").translate(None, string.punctuation).strip() for arg in args ]

    slug = "-".join(args)

    url = "https://www.hackerrank.com/rest/contests/master/challenges/%s" % (slug)
    print "URL IS", url

    try:
        members = dict( (x, x) for x in bot.bot.members[cmd_data["channel"]])
    except:
        members = {}

    for k in SOLVERS:
        members[k] = SOLVERS[k]

    print "PROBLEM IS", url
    data = urllib2.urlopen("%s/leaderboard?offset=%s&limit=100&include_practice=true&_=%s" % (url, offset, now))
    read = json.loads(data.read())
   
    found_solver = False
    found_solvers = []

    total = read["total"]
    print "TOTAL", total
    if total > 20000:
        bot.say("too many people solved this problem, i'm not digging through that");
        return

    while not found_solver and offset < total:
        print "CHECKING %s..." % (offset)
        solvers = read["models"]

        
        for solver in solvers:
            name = solver["hacker"].lower()
            if name in members:
                solver["hacker"] = members[name]
                found_solvers.append(solver)

        offset += 100

        if offset > total:
            break

        try:
            data = urllib2.urlopen("%s/leaderboard?offset=%s&limit=100&include_practice=true&_=%s" % (url, offset, now))
            read = json.loads(data.read())
        except Exception, e:
            print e
            break



    if found_solvers:
        solve_str = ", ".join([ "%s (%s)" % (str(s["hacker"]).lower(), int(s["score"])) for s in found_solvers ])
        bot.say("%s: %s was solved by %s" % (cmd_data["nick"], slug.replace("-", " "), solve_str))
    else:
        bot.say("No one has solved this problem so far")
    print "FOUND SOLVERS", found_solvers



    

def add_solver(bot, data, *args):
    if data["nick"] in auth.OWNERS:
        print "LISTENING TO OWNER!", data["nick"]
        changed = False
        for tok in args:
            if tok.find(":") == -1:
                continue

            if tok in [ "to", "and", "now" ] or tok in FILLWORDS:
                continue

            if tok[0] == "!":
                print "REMOVE USER", tok
                tok = tok[1:]
                if tok in [ "everyone" ]:
                    remove_user("*", data["nick"])
                else:
                    remove_user(tok, data["nick"])

                changed = True
            else:
                if tok in [ "everyone" ]:
                    add_user("*", data["nick"])
                else:
                    print "ADDING USER", tok
                    tok = tok.split(":")

                    username = tok[0]
                    ircnick = tok[1]
                    add_user(username, ircnick)
                changed = True

        if changed:
            bot.say("%s: %s %s" % (data["nick"], affirmative(), affirmative()))


_reload()

COMMANDS = {}
COMMANDS={
    "solved": has_solved_problem
}
COMMANDS["!addsolver"] = add_solver
