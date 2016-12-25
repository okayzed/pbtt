import random
import time

import threading


def add_typo(string):
    if random.random > 0.75:
        return string

    idx = random.randint(0, len(string)-2)

    split = [c for c in string]
    split[idx], split[idx+1] = split[idx+1],split[idx]

    return "".join(split)

def random_cycles(msgs):
    msg_copy = [x for x in msgs]

    while True:
        random.shuffle(msg_copy)
        for x in msg_copy:
            yield add_typo(x)

AFFIRM = random_cycles([
    "alright - ",
    "can do",
    "will do!",
    "got it",
    "fine...",
])

WAIT = random_cycles([
    "one sec...",
    "hold on. ",
    "ok... ",
    "err... ",
    "err... one sec. ",
    "h/o ",
    "alright, ",
])

ENCOURAGE = random_cycles([
    "should be easy for you :P",
    "i think this one should be interesting",
    "this one will be interesting",
    "i think you'll like it",
    "this one should be fun",
    ":P",
    ";)",
])

HUH = random_cycles([
    "huh?",
    "...",
    "?",
    "pardon?"
])

FILLWORDS = [
    "yo",
    "go",
    "no way",
    "alright",
    "good",
    "haha",
    "anyways",
    "meh",
    "lol",
    "heh",
    "hey",
    "sure",
    "please",
    "yeah",
    "no",
    "now",
    "ok",
    "can",
    "will",
    "you"
]

def affirmative():
    return next(AFFIRM)

def hold_on():
    return next(WAIT)

def encouragement():
    return next(ENCOURAGE)

def huh():
    return next(HUH)


ACTUALLY_WAIT=True
def wait_small(cb=None):
    if not ACTUALLY_WAIT:
        if cb:
            cb()
        return

    amount = random.random() * 5 + 3
    if cb:
        print "WAITING SMALL"
        response_thread = threading.Timer(amount, cb)
        response_thread.start()
    else:
        print "WAITING SMALL"
        time.sleep(amount)
        print "DONE SMALL"

def wait_large(cb=None):
    if not ACTUALLY_WAIT:
        if cb:
            cb()
        return
    amount = random.random() * 5 + 3
    if cb:
        print "WAITING LARGE"
        response_thread = threading.Timer(amount, cb)
        response_thread.start()
    else:
        print "WAITING LARGE"
        time.sleep(amount)
        print "DONE LARGE"

