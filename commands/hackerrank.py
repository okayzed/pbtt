
import math
import random
import urllib2
import time

from bs4 import BeautifulSoup

from mannerisms import *
import re
import string

def regex_contains(parent, regex):
    parent = parent.lower()
    m = re.match(regex, str(parent).translate(None, " "))
    return m != None


SOLVERS = {
    "cherim" : "cherim",
    "dbqpdb" : "oky",
    "kadoban" : "kadoban"
}

def has_solved_problem(bot, cmd_data, *args):

    import time, json
    now = str(time.time()*1000)

    offset = 0

    args = [ arg.replace("-", " ").translate(None, string.punctuation).strip() for arg in args ]

    slug = "-".join(args)

    url = "https://www.hackerrank.com/rest/contests/master/challenges/%s" % (slug)
    print "CHECKING SOLVED PROBLEM", SOLVERS
    print "PROBLEM IS", url
    data = urllib2.urlopen("%s/leaderboard?offset=%s&limit=100&include_practice=true&_=%s" % (url, offset, now))
    read = json.loads(data.read())
   
    found_solver = False
    found_solvers = []

    total = read["total"]
    print "TOTAL", total
    while not found_solver and offset < total:
        print "CHECKING %s..." % (offset)
        solvers = read["models"]

        
        for solver in solvers:
            name = solver["hacker"].lower()
            if name in SOLVERS:
                solver["hacker"] = SOLVERS[name]
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



    

COMMANDS={
    "solved": has_solved_problem
}
