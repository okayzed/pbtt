from helpers import *
import mannerisms
import time

MESSAGES={}
def load_data():
    global MESSAGES
    loaded_data = load_data_for_module("answering_machine", "db", {})
    MESSAGES=loaded_data
    return loaded_data

load_data()

def save_data():
    save_data_for_module("answering_machine", "db", MESSAGES)

seconds_in_day = 60 * 60 * 24
seconds_in_week = seconds_in_day * 7
def make_timedelta(timestamp):
    now = time.time()
    delta = now - timestamp

    ts = []

    w = delta // seconds_in_week
    delta %= seconds_in_week
    if w > 0:
        ts.append("%iw" % w)

    d = delta // seconds_in_day
    delta %= seconds_in_day

    if d > 0:
        ts.append("%id" % d)

    h = delta // 3600
    delta %= 3600

    if h > 0:
        ts.append("%ih" % h)

    m = delta // 60
    delta %= 60

    if m > 0:
        ts.append("%im" % m)

    s = delta % 60
    if s > 0:
        ts.append("%is" % s)

    return "".join(ts)

def check(response, channel, line, nick):
    tokens = line.split(" ")
    if tokens[0] == ":.tell":
        to = tokens[1]
        msg = " ".join(tokens[2:])
        if not to in MESSAGES:
            MESSAGES[to] = []

        MESSAGES[to].append((channel, "%s says %s" % (nick, msg), time.time()))
        save_data()
        response.whisper(nick, "i'll tell %s you said '%s'" % (to, msg))
        return True
    elif nick in MESSAGES:
        now = time.time()
        msgs = MESSAGES[nick]
        for channel, msg, timestamp in msgs:
            wh = "%s (%s ago in #%s)" % (msg, make_timedelta(timestamp), channel)
            response.whisper(nick, wh)

        del MESSAGES[nick]
        save_data()
        return True
