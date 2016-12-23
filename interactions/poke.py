from helpers import *
from interaction import Interaction
from mannerisms import *

POKE = random_cycles([
    "pok pok pok",
    "poke",
    "pokeh",
    "pokeypoke",
    "pokepokepoke!"
    "poke!",
    "stop..."
])

class Poke(Interaction):
    def score(self, data, tokens):
        for tok in tokens:
            if tok == "poke":
                return 1
                

    def do(self, bot, data, tokens):
        bot.say("%s: %s" % (data["nick"], next(POKE)))


INTERACTIONS = [ Poke ] 
