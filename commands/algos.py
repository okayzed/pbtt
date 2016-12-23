import math
import random
import urllib2
import time

from bs4 import BeautifulSoup

from mannerisms import *

def pick_hackerrank_problem(bot, topics, tries=0):
    import time, json
    now = str(time.time()*1000)
    data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master?&_=" + now)
    read = json.loads(data.read())

    print "PICKING HR PROBLEM"
    cats = []
    if not topics:
        topics = [ "algorithms" ]
    for c in read["model"]["categories"]:
        for t in topics:
            print c["slug"], c["name"]
            if c["slug"].find(t) != -1 or c["name"].lower().find(t) != -1:
                cats.append(c)

    random_cat = random.choice(cats)
    cand = []
    for topic in random_cat["children"]:
        for t in topics:
            if t[0] != "#":
                continue

            if topic["slug"].find(t[1:]) != -1 or topic["name"].lower().find(t[1:]) != -1:
                cand.append(topic)

    if not cand:
        cand = random_cat["children"]

    choice = random.choice(cand)
    print "CHOICE IS", choice
    data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master/categories/%s%%7C%s/challenges?offset=0&limit=100&_=%s" % (random_cat["slug"], choice["slug"], now))

    read = json.loads(data.read())
    problems = read["models"]

    total = read["total"]
    print "TOTAL", total

    rand_pick = random.randint(0, total-1)

    if random.random() < 0.2:
        bot.say("%s i'm gonna pick a problem from %s" % (hold_on().strip(), choice["name"].lower()))
    elif random.random() < 0.2:
        bot.say("let me look a for a good one...")

    time.sleep(random.random() * 10 + 10)

    offset = rand_pick / 50
    idx = rand_pick % 50
    data = urllib2.urlopen("https://www.hackerrank.com/rest/contests/master/categories/%s%%7C%s/challenges?offset=%s&limit=50&_=%s" % (random_cat["slug"], choice["slug"], offset, now))
    read = json.loads(data.read())

    problems = read["models"]

    try:
        model = problems[idx]

        problem_slug = "https://hackerrank.com/challenges/%s" % (model["slug"])
        difficulty = model["difficulty_name"].lower()
        score = model["max_score"]
        if random.random() > 0.5:
            bot.say("how about %s? %s" % (problem_slug, encouragement()))
        else:
            bot.say("how about %s? it's a %s problem worth %s points" % (problem_slug, difficulty, score))
            
    except:
        bot.say("Oops... had a little trouble there, gonna look for a new one")
        if tries < 3:
            pick_hackerrank_problem(bot, topics, tries+1)
        



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
    bot.say("Sorry, not leetcode allowed!")
    pass


ALGO_SITES = {
    "hackerrank": pick_hackerrank_problem,
    "spoj" : pick_spoj_problem,
    "uva" : pick_uva_problem,
    "leetcode": pick_leetcode_problem
}

COMMANDS={}
