import shlex
import random

import facts
import auth
import ircbot
import helpers
import parser

from mannerisms import *

def answer_fact_from(bot, data, *args):
    person = parser.Section(prefix="@", tokens=["to", "with"])

    parser.keyword_seperate(args, keywords=[person])

    reversed_history = reversed(bot.bot.history[data["channel"]])
    args = [a for a in args]

    for person in person.topics:
        print "RESPONDING TO", person
        for hist in reversed_history:
            sendername = hist[0]
            line = hist[1]

            nick = helpers.nick_for(sendername)


            if line.find("respond") != -1 or line.find("answer") != -1 and nick == data["nick"]:
                print "SKIPPING LINE ASKING FOR RESPONSE?"
                continue

            if nick == person:
                # now we handle and dispatch, then return
                new_data = dict([(k,data[k]) for k in data ])
                print "USING LINE:",line
                new_data["nick"] = nick

                facts.recall_fact(bot, new_data, *line.split(" "))

                break

def interact_with(rsp, data, *args):
    person = parser.Section(prefix="@", tokens=["to", "with"])
    parser.keyword_seperate(args, keywords=[person])

    reversed_history = reversed(rsp.bot.history[data["channel"]])
    args = [a for a in args]

    for person in person.topics:
        print "INTERACTING WITH", person
        for hist in reversed_history:
            sendername = hist[0]
            line = hist[1]

            nick = helpers.nick_for(sendername)
            skip = False
            for word in ["respond", "answer", "interact"]:
                if line.find(word) != -1 and nick == data["nick"]:
                    print "SKIPPING LINE ASKING FOR RESPONSE?"
                    skip = True
                    break

            if skip:
                continue

            if nick == person:
                # now we handle and dispatch, then return
                new_data = dict([(k,data[k]) for k in data ])
                print "USING LINE:",line
                new_data["nick"] = nick
                new_data["tokens"] = line.split(" ")

                rsp.bot.do_interact(new_data)

                break



# respond should do what? look up facts or try to interact?
# we can randomly decide for now
def respond_to(rsp, data, *args):
    if random.random > 0.5:
        answer_fact_from(rsp, data, *args)
    else:
        interact_with(rsp, data, *args)


COMMANDS={}
COMMANDS["respond"] = respond_to
COMMANDS["answer"] = answer_fact_from
COMMANDS["interact"] = interact_with
