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
def find_all_topics(tokens):
    topics = set(map(STEMMER, tokens))
    # remove fill words from the tokens, probably

    possibles = []
    load_data()
    for q in FACTS:
        overlap = topics.difference(FILLWORDS).intersection(q.topic)
        if overlap:
            possibles.append((q, overlap))

    possibles.sort(key=lambda w: len(w[1]), reverse=True)

    return [p[0] for p in possibles]

def find_topic(tokens):
    return find_all_topics(tokens)[0]

def learn_fact(bot, data, *args):
    load_data()
    if data["nick"] in auth.ALLOWED:
        import commands, interactions
        tokens = shlex.split(" ".join(args))

        topic = tokens[0]
        fact = tokens[1:]
        cand = find_exact_topic(topic)
        if not cand:
            cand = Topic(topic)
            FACTS.append(cand)


        print "LEARNING", cand.topic, tokens[1:]
        cand.answers.append(fact)
        bot.say(data["nick"] + ":", affirmative())
        save_data()

def forget_fact(bot, data, *args):
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
        bot.say("FORGETTING", cand.name, "[%s/%s]:" % (index, len(cand.answers)), " ".join(cand.answers[index-1]))

        if cand.answers:
            cand.answers.pop(index-1)

        if not cand.answers:
            FACTS.remove(cand)

        save_data()

import string
def recall_fact(bot, data, *args):
    full_args = " ".join(args).lower()
    EXPLAIN = False
    if full_args.find("~explain") >= 0:
        EXPLAIN = True
        full_args = full_args.replace("~explain", "").strip()

    match = re.search("\[(\d+)\]", full_args)
    full_args = re.sub("\[(\d+)\]", "", full_args).translate(None, string.punctuation)

    tokens = shlex.split(full_args)
    cands = find_all_topics(tokens)

    if not cands:
        bot.say("%s: I don't know anything about that" % (data["nick"]))
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
        fact_info = fact_topic.answers[-1]
        fact_offset = 0

    all_topics = [c.name for c in cands]
    # if there was more than one topic, we print: "search term", "topic term", search idx, topic idx
    if EXPLAIN:
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
        answer = fact_topic.answers[fact_offset-1]
        bot.say(data["nick"] + ":", "'%s' [%s/%s]: %s" % (search_term, index, cur_index, " ".join(answer)))
    else:
        search_term = all_topics[0]
        answer = fact_topic.answers[fact_offset-1]
        bot.say(data["nick"] + ":", fact_topic.name, " ".join(answer))




    return


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


    

COMMANDS = {}
COMMANDS["learn"] = learn_fact
COMMANDS["know"] = recall_fact
COMMANDS["recall"] = recall_fact
COMMANDS["recommend"] = recall_fact
COMMANDS["forget"] = forget_fact
COMMANDS["merge"] = merge_fact

