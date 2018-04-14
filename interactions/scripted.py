from helpers import *
from interaction import Interaction
from mannerisms import *

import scripted_helper
import re
import random


# TODO:
# add cooldown so we don't see the same answer too many times in a row this
# should hopefully prevent people from bothering us and getting the same
# answers


def get_match(channel, script, line):
    match = re.search(script.precedent.strip(), line, re.IGNORECASE)

    if related_channel(script, channel):
        return match

def related_channel(script, channel):
    channels = getattr(script, 'channels', [])

    for ch in channels:
        if channel == ch:
            return True



class ScriptedInteraction(Interaction):
    def score(self, data, tokens):
        scripted_helper.load_data()
        line = " ".join(tokens)

        can_do = []
        for script in scripted_helper.SCRIPTS:
            match = get_match(data["channel"], script, line)

            if match:
                # we found a match, so let's perform the script
                # we have several replacements to do, too
                can_do.append(script)
                print "FOUND", script.precedent, script.antecedent
                return 1


        if can_do:
            script = random.choice(can_do)




    def do(self, bot, data, tokens):
        scripted_helper.load_data()
        line = " ".join(tokens)

        can_do = []
        for script in scripted_helper.SCRIPTS:
            match = get_match(data["channel"], script, line)

            if match:
                # we found a match, so let's perform the script
                # we have several replacements to do, too
                can_do.append(script)


        if "explain" in data and data["explain"]:
            bot.say("[%s/%s] interactions found" % (len(can_do), len(scripted_helper.SCRIPTS)))
        elif can_do:
                script = random.choice(can_do)
                replacements = {
                    "%%nick": data["nick"]
                }

                msg = script.antecedent.strip()
                for r in replacements:
                    msg = msg.replace(r, replacements[r])

                wait_small()
                bot.say("%s: %s" % (data["nick"], msg))

INTERACTIONS = [ ScriptedInteraction ]
