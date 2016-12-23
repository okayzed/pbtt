from helpers import *
from interaction import Interaction
from mannerisms import *

GREET = random_cycles([
    "yo",
    "what's up?",
    "oy",
    "hey",
    "o/",
    "\o"
])

EXIT = random_cycles([
    "bye",
    "see you",
    "latre",
    "later",
    "laters",
    "take it easy",
    "next time"
])

YOURWELCOME = random_cycles([
    "np",
    "you're welcome",
    "np - its on me",
    "sure",
    "yeah, yeah... do it yourself next time",
    "no problem",
    "yup"
])

GOING = random_cycles([
    "not much - you?",
    "...",
    "do you want something?",
    "lol - not again. what do you want?",
    "same as before"
])

RECEIVE_PRAISE = random_cycles([
    "thanks",
    "aw shucks",
    ":-D",
    "happy to hear it",
    "i suppose so",
])

RECEIVE_CONDEMN = random_cycles([
    "if thats how you feel about it...",
    "ok, ok - i get it",
    "yeah - you're not so nice yourself",
    "you know what you can do with that attitude?",
    "i have feelings, you know",
])

class Thanks(Interaction):
    def score(self, data, tokens):
        for tok in tokens:
            if tok in ["thanks", "thank", "thx", "thnk" ]:
                return 1
                

    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(YOURWELCOME)))

class Greet(Interaction):
    def score(self, sendername, tokens):
        for tok in tokens:
            if tok in ["hey", "hello", "hi", "yo", "o/", "\o"]:
                return 1
                

    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(GREET)))

class Inquire(Interaction):
    def score(self, data, tokens):
        all_tok = "".join(tokens)
        for tok in [ "howsitgoing", "howareyou", "howsit", "whatsup", "whatsgood", "whatsthegoodword" ]:
            if all_tok.find(tok) >= 0:
                return 2

    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(GOING)))

class Valediction(Interaction):
    def score(self, data, tokens): 
        all_tok = "".join(tokens)
        for tok in [ "bye", "seeyou", "cya", "later", "gtg", "gottogo", "seeya", "bbl", "bebacklater" ]:
            if all_tok.find(tok) >= 0:
                return 1

    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(EXIT)))
            

class Praise(Interaction):
    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(RECEIVE_PRAISE)))
            

    def score(self, data, tokens): 
        all_tok = "".join(tokens)
        for tok in [ "nicework", "goodjob", "welldone", "goodbot"]:
            if all_tok.find(tok) >= 0:
                return 1


class Condemn(Interaction):
    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(RECEIVE_CONDEMN)))
    def score(self, data, tokens): 
        all_tok = "".join(tokens)
        for tok in ["fuckoff", "badjob", "hateyou"]:
            if all_tok.find(tok) >= 0:
                return 1


INTERACTIONS = [ Greet, Thanks, Inquire, Valediction, Praise, Condemn ] 
