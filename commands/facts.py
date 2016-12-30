import math
import random
import urllib2
import time
import re

import algos
import auth

from mannerisms import *
import ircbot
import shlex
import helpers
import parser


STEMMER=lambda w: w

try:
    from stemming import porter2
    STEMMER=porter2.stem
except:
    pass

try:
    import porter2stemmer
    STEMMER=porter2stemmer.Porter2Stemmer().stem
except:
    pass


class Fact(object):
    def __init__(self, *args, **kwargs):
        self.answer = " ".join(args)

class Topic(object):
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.topic = set(map(STEMMER, args[0].lower().split(" ")))
        self.answers = []
        if len(args) > 1:
            self.answers = args[1:]
        print 'LEARNING NEW FACT', self.name, self.topic, self.answers

FACTS=None
def load_data():
    global FACTS
    loaded_data = helpers.load_data_for_module("facts", "db", [])
    FACTS=loaded_data
    return loaded_data

def save_data():
    helpers.save_data_for_module("facts", "db", FACTS)

def find_exact_topic(topic):
    for q in FACTS:
        if q.name == topic:
            return q

# find a list of facts and topics they fall under
def find_all_topics(tokens, sort=True):
    add = []
    tokens = [ t.translate(None, string.punctuation) for t in tokens ]

    topics = set(map(STEMMER, tokens))
    # remove fill words from the tokens, probably

    possibles = []
    load_data()
    for q in FACTS:
        overlap = topics.difference(FILLWORDS).intersection(q.topic)
        if overlap:
            possibles.append((q, overlap))

    if sort:
        possibles.sort(key=lambda w: len(w[1]), reverse=True)

    return [p[0] for p in possibles]

def find_topic(tokens):
    return find_all_topics(tokens)[0]

def learn_fact(bot, data, *args):
    load_data()
    if data["nick"] in auth.ALLOWED:
        import commands, interactions
        full_args = " ".join(args)

        if full_args.find('"') != -1:
            tokens = shlex.split(full_args)
            # we are trying to improve how we remember
            if tokens[0] in ["that"]:
                tokens.pop(0)

            topic = tokens[0]
            fact = tokens[1:]


        else:
            tokens = list(args)
            if tokens[0] in ["that"]:
                tokens.pop(0)
            topic = " ".join(tokens)
            fact = ""

        cand = find_exact_topic(topic)
        if not cand:
            cand = Topic(topic)
            FACTS.append(cand)


        print "LEARNING", cand.topic, tokens[1:]

        cand.answers.append(fact)
        bot.say(data["nick"] + ":", affirmative())
        save_data()


def forget_fact(bot, data, *args):
    load_data()
    full_args = " ".join(args)
    match = re.search("\[(\d+)\]", full_args)

    full_args = re.sub("\[(\d+)\]", "", full_args)
    tokens = shlex.split(full_args)
    cand = find_exact_topic(" ".join(tokens))
    print "TOPIC SEARCH", full_args


    index = 0
    if match:
        index = int(match.group(1))

        if index < 0:
            index += len(cand.answers)

        if index > len(cand.answers):
            return

    if cand:
        if cand.answers:
            bot.say("forgetting", cand.name, "[%s/%s]:" % (index, len(cand.answers)), " ".join(cand.answers[index-1]))
        else:
            bot.say("forgetting", cand.name)

        if cand.answers:
            cand.answers.pop(index-1)

        if not cand.answers:
            FACTS.remove(cand)

        save_data()

import string
def recall_fact(bot, data, *args):
    wait_small()
    full_args = " ".join(args).lower()
    match = re.search("\[(\d+)\]", full_args)
    full_args = re.sub("\[(\d+)\]", "", full_args).translate(None, string.punctuation)

    if full_args.find("latest") != -1 or full_args.find("news") != -1:
        recall_latest_fact(bot, data, *args)
        return

    tokens = shlex.split(full_args)
    cands = find_all_topics(tokens)

    if not cands:
        bot.say("%s: %s" % (data["nick"], deny_knowledge()))
        return

    index = 1
    if match:
        index = int(match.group(1))

        if index <= 0:
            index = 1

    cur_index = 0
    fact_info = None
    fact_topic = None

    for cand in cands:
        if cur_index <= index:
            this_index = 0
            for ans in cand.answers:
                cur_index += 1
                this_index += 1

                if cur_index == index:
                    fact_topic = cand
                    fact_info = ans
                    fact_offset = this_index
        else:
            cur_index += len(cand.answers)

    if cur_index < index:
        fact_topic = cand
        fact_info = ""
        if fact_topic.answers:
            fact_info = fact_topic.answers[-1]
        fact_offset = 0

    all_topics = [c.name for c in cands]
    # if there was more than one topic, we print: "search term", "topic term", search idx, topic idx
    answer = ""
    if data["explain"]:
        if fact_offset == 0:
            fact_offset = len(fact_topic.answers)

        if len(all_topics) > 10:
            sentence_one = "Found %s tidbits in %s topics" % (cur_index, len(all_topics))
        else:
            topic_sentence = ", ".join([ "'%s'" % w for w in all_topics ])

            sentence_one = "Found %s tidbits in %s topics, %s" % (cur_index, len(all_topics), topic_sentence)

        sentence_two = "Using '%s' [%s/%s]" % (fact_topic.name, fact_offset, len(fact_topic.answers))

        bot.say("%s. %s" % (sentence_one, sentence_two))
        search_term = full_args
        if fact_topic.answers:
            answer = fact_topic.answers[fact_offset-1]
    else:
        search_term = all_topics[0]
        if fact_topic.answers:
            answer = fact_topic.answers[fact_offset-1]
        bot.say(data["nick"] + ":", fact_topic.name, " ".join(answer))




    return

def recall_latest_fact(bot, data, *args):
    wait_small()
    full_args = " ".join(args).lower()

    tokens = shlex.split(full_args)
    tokens = filter(lambda w: w not in ["about", "on", "with", "of", "the"], tokens)

    print "TOKENS", tokens
    cands = find_all_topics(tokens, sort=False)

    if not cands:
        bot.say("%s: %s" % (data["nick"], deny_knowledge()))
        return

    fact_topic = cands[-1]
    answer = ""
    if fact_topic.answers:
        answer = fact_topic.answers[-1]

    bot.say(data["nick"] + ":", fact_topic.name, " ".join(answer))

def merge_fact(bot, data, *args):
    full_args = " ".join(args)
    tokens = shlex.split(full_args)

    for x in [ "to", "into" ]:
        if x in tokens:
            tokens.remove(x)

    load_data()

    print "FULL ARGS", full_args

    if len(tokens) > 2:
        bot.say("Huh?")
    else:
        print "TOKENS", tokens
        src = find_exact_topic(tokens[0])
        dst = find_exact_topic(tokens[1])

        if not dst:
            dst = Topic(tokens[1])
            FACTS.append(dst)

        bot.say(data["nick"]+":", "Merging '%s' into '%s'" % (src.name, dst.name))
        print "MERGING", src, "INTO", dst
        for ans in src.answers:
            dst.answers.append(ans)

        print "REMOVING FACT", src.name
        FACTS.remove(src)

        save_data()

def tag_fact(bot, data, *args):
    wait_small()
    full_args = " ".join(args).lower()
    print "TAGGING FACT"

    untags = parser.Section(
        prefix="-",
        tokens=["without"])

    tags = parser.Section(
        prefix="+",
        tokens=["with"])

    query = parser.Section()

    parser.keyword_seperate(full_args, keywords=[tags, untags], unparsed=query)

    topics = find_all_topics(query.topics)
    if not topics:
        return

    if tags.topics:
        print "ADDING TAGS", tags.topics

    if untags.topics:
        print "REMOVING TAGS", untags.topics

    for topic in topics:
        print "ADJUSTING TAGS ON TOPIC", topic.name
        for t in tags.topics:
            t = STEMMER(t)
            topic.topic.add(t)

        for u in untags.topics:
            u = STEMMER(u)
            topic.topic.remove(u)

    save_data()


# remember is a double command.
# if it is: "what do you remember?"
# then we have to use recall_fact
# if it is: "i want you to remember"
# then we have to use learn_fact
# to achieve this, we should check if stop

# words contain 'what' and then turn into
# query vs command mode

def remember_fact(rsp, data, *args):
    stopwords = data['stopwords']

    last_letter = None
    if len(args) > 0:
        last_token = args[-1]
        last_letter = last_token[-1]
        print "LAST TOKEN", last_token[-1]

    if 'what' in stopwords or last_letter == "?":
        recall_fact(rsp, data, *args)
    else:
        learn_fact(rsp, data, *args)

COMMANDS = {}
COMMANDS["know"] = recall_fact
COMMANDS["tell"] = recall_fact
COMMANDS["recall"] = recall_fact
COMMANDS["recommend"] = recall_fact

COMMANDS["news"] = recall_latest_fact
COMMANDS["latest"] = recall_latest_fact

COMMANDS["learn"] = learn_fact

COMMANDS["remember"] = remember_fact

COMMANDS["tag"] = tag_fact

COMMANDS["forget"] = forget_fact
COMMANDS["merge"] = merge_fact

