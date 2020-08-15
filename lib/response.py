import time
import helpers
import requests
from lxml import etree

SEEN = {}
def load_data():
    global SEEN
    loaded_data = helpers.load_data_for_module("response", "db", {})
    SEEN=loaded_data
    return loaded_data

def save_data():
    helpers.save_data_for_module("response", "db", SEEN)

# we want to avoid dobby saying the same thing over and over again in our channels
# so in Response, we will try to keep track of how recently dobdob said something.

# if dobdob said something recently, we don't repeat it!
# this could mean that 1) dobdob runs out of things to say, even

# or it could mean that we start using typos and mistakes in what dobdob says
# after its been said more than once?
def have_seen(channel, sentence):
    load_data()
    if not channel in SEEN:
        SEEN[channel] = {}

    if not sentence in SEEN[channel]:
        return False

    now = time.time()
    last_seen = SEEN[channel][sentence]
    if now - last_seen > 3600:  # we try not to repeat for an hour
        del SEEN[channel][sentence]
        return False

    print "SEEN RECENTLY, IGNORING SENTENCE:", sentence
    return True

def mark_seen(channel, sentence):
    now = time.time()
    if not channel in SEEN:
        SEEN[channel] = {}

    SEEN[channel][sentence] = now
    save_data()

class Response():
    def __init__(self, *args, **kwargs):
        self.is_whisper = False # for twitch whispers

    def whisper(self, nick, *args):
        full_sentence = " ".join(args)
        if have_seen(nick, full_sentence):
            return

        self.bot.send("PRIVMSG", nick, ":" + full_sentence)
        mark_seen(nick, full_sentence)

    def say(self, *args):
        full_sentence = " ".join(args)
        tokens = full_sentence.split(" ")

        if tokens[0][-1] == ":":
            tokens.pop(0)

        seen_sentence = " ".join(tokens)

        # TODO: undupe the below code
        if self.is_whisper:
            if have_seen(self.from_nick, seen_sentence):
                return

            self.bot.send("PRIVMSG", self.channel, ":/w", self.from_nick, full_sentence)
            mark_seen(self.from_nick, seen_sentence)
        else:
            if have_seen(self.channel, seen_sentence):
                return

            self.bot.send("PRIVMSG", self.channel, ":" + full_sentence)
            mark_seen(self.channel, seen_sentence)


