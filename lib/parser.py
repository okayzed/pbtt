# this file will contain some hacky parsing stuff, for now

# i want to build a sentence that looks like:
# <STOPWORDS> <PRE><COMMAND> <ARGS>

# An example for args will be something like:
# FROM hackerrank THATS easy ABOUT algorithms
# INPUT: { from: "FROM", topic: ["THATS", "ABOUT"] }
# OUTPUT: from: hackerrank, topic: ['easy algorithms']

# can also support NOT before a keyword
# but only if the full list of categories
# are provided for the keyword

# some sample sentences i want to be parsing:
#   "pick an easy problem from hackerrank"
#   "remember that ..."
#   "can you tell me about"
#   "what can you recall about"
#   "revive yourself"

# to do this, we have to have a few functions
# stopword removal
# pre-command extract
# args seperate

import mannerisms
import string

class Section():
    def __init__(self, *args, **kwargs):
        self.topics = []
        self.ignore = []

        self.tokens = kwargs.get("tokens", None)
        self.prefix = kwargs.get("prefix", None)
        self.defaults = kwargs.get("defaults", [])


        self.default = kwargs.get("default", None)
        if type(self.default) == str:
            self.default = [self.default]

def keyword_seperate(tokens, keywords=[], fillwords=None, unparsed=None):

    if type(tokens) == str:
        tokens = tokens.split(" ")

    if not fillwords:
        fillwords = mannerisms.FILLWORDS

    nono = False
    cur_k = None
    for arg in tokens:
        oldarg = arg
        arg = arg.lower()
        arg = arg.translate(None, string.punctuation.replace("#", ""))
        arg = arg.strip()
        if arg == "not" or arg == "but":
            nono = True
            continue

        # check to see if the current arg is a keyword
        set_k = False
        for k in keywords:
            if not k.tokens:
                continue

            if arg in k.tokens:
                cur_k = k
                set_k = 1

        if set_k:
            continue

        # check to see if current arg is a prefixed word
        set_p = False
        for k in keywords:
            if oldarg[0] != k.prefix:
                continue

            if nono:
                k.ignore.append(oldarg[1:])
            else:   
                k.topics.append(oldarg[1:])
                print "ADDING PREFIX", arg, "TO", k

                set_p = True

        if set_p:
            continue

        # place the current arg into our topics (or ignored topics)
        # for the current keyword
        if cur_k:
            if nono:
                cur_k.ignore.append(arg)
            else:
                cur_k.topics.append(arg)
        else:
            if unparsed:
                unparsed.topics.append(arg)

    for k in keywords:
        if not k.topics:
            if k.default:
                k.topics.extend(k.default)

