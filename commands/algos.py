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

difficulties = ['easy', 'normal', 'medium', 'hard', 'advanced', 'expert']
def pick_hackerrank_problem(bot, topics, tries=0):
    import time, json
    max_tries = 3
    now = str(time.time()*1000)
    data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master?&_=" + now)
    read = json.loads(data.read())

    print "PICKING HR PROBLEM", topics, tries
    cats = []
    if not topics:
        topics = [ "algorithms" ]

    backup_cats = []
    for c in read["model"]["categories"]:
        for t in topics:
            if regex_contains(c["slug"], t) or regex_contains(c["name"], t):
                cats.append(c)
        if c["slug"] in [ "algorithms" ]:
            backup_cats.append(c)

    if not cats:
        cats = backup_cats

    random_cat = random.choice(cats)
    cand = []
    for topic in random_cat["children"]:
        for t in topics:
            if t[0] != "#":
                continue

            slug = topic["slug"]
            name = topic["name"]
            if regex_contains(slug, t[1:]) or regex_contains(name, t[1:]):
                cand.append(topic)


    available_difficulty = []
    for t in topics:
        if t.lower().strip() in difficulties:
            available_difficulty.append(t.lower().strip())


    if not cand:
        cand = random_cat["children"]

    choice = random.choice(cand)
    print "CHOICE IS", choice
    data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master/categories/%s%%7C%s/challenges?offset=0&limit=100&_=%s" % (random_cat["slug"], choice["slug"], now))

    read = json.loads(data.read())
    problems = read["models"]

    total = read["total"]
    print "TOTAL", total


    # if we can pick from any difficulty
    rand_pick = random.randint(0, total-1)

    if not available_difficulty and random.random() < 0.2:
        bot.say("%s i'm gonna pick a problem from %s" % (hold_on().strip(), choice["name"].lower()))
    elif random.random() < 0.2:
        bot.say("let me look a for a good one...")

    def next_step():
        offset = rand_pick / 50
        idx = rand_pick % 50
        data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master/categories/%s%%7C%s/challenges?offset=%s&limit=50&_=%s" % (random_cat["slug"], choice["slug"], offset, now))
        read = json.loads(data.read())

        problems = read["models"]

        if available_difficulty:
            available_problems = []
            for p in problems:
                if p["difficulty_name"].lower().strip() in available_difficulty:
                    available_problems.append(p)

            if available_problems:
                model = random.choice(available_problems)
            else:
                if tries < max_tries:
                    return pick_hackerrank_problem(bot, topics, tries+1)
                else:
                    bot.say("oops - i couldn't find any problems")
                    return

        else:

            try:
                model = problems[idx]
            except:
                bot.say("Oops... had a little trouble there, gonna look for a new one")
                if tries < max_tries:
                    pick_hackerrank_problem(bot, topics, tries+1)

        problem_slug = "https://hackerrank.com/challenges/%s" % (model["slug"])
        difficulty = model["difficulty_name"].lower()
        score = model["max_score"]
        if random.random() > 0.5:
            bot.say("how about %s? %s" % (problem_slug, encouragement()))
        else:
            bot.say("how about %s? it's a %s problem worth %s points" % (problem_slug, difficulty, score))
    wait_large(next_step)

def pick_euler_problem(bot, topics=[]):
    problem = random.randint(1, 550)
    url = "https://projecteuler.net/problem=%s" % problem
    f = urllib2.urlopen(url)

    soup = BeautifulSoup(f, 'html.parser')
    title = soup.find("div", id="content").find("h2").string
    if title:
        bot.say("How about %s? %s - %s " % (title, url, encouragement()))

def pick_uva_problem(bot, topics=[]):
    problem = random.randint(1, 5000)
    url = "https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=%s" % problem
    f = urllib2.urlopen(url)

    soup = BeautifulSoup(f, 'html.parser')
    title = soup.find("div", id="col3_content").find("h3").string
    if title:
        bot.say("How about %s? %s - %s " % (title, url, encouragement()))

def pick_spoj_problem(bot, topics=[]):
    bot.say("uhhh... maybe later?")
    pass

def pick_leetcode_problem(bot, topics=[]):
    bot.say("Sorry, no leetcode allowed!")
    pass


ALGO_SITES = {
    "hackerrank": pick_hackerrank_problem,
    "spoj" : pick_spoj_problem,
    "uva" : pick_uva_problem,
    "leetcode": pick_leetcode_problem,
    "euler" : pick_euler_problem
}

COMMANDS={}
