from mannerisms import *
import re
import helpers

SCRIPTS=None
def load_data():
    global SCRIPTS
    loaded_data = helpers.load_data_for_module("scripts", "db", [])
    SCRIPTS=loaded_data
    return loaded_data

def save_data():
    helpers.save_data_for_module("scripts", "db", SCRIPTS)

# this thing gets saved to our DB
# for now, interactions look like:
# Script:
#   matchings
#   action sequence
class Script():
    def __init__(self, *args, **kwargs):
        pass
        self.antecedents = []
        self.precedent = None
