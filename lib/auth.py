import pickle
import helpers

ALLOWED = {
    "oky" : 0xFFFF,
    "guf" : 0xFFFF,
}


OWNERS = {
    "oky" : 0xFFFF,
    "guf" : 0xFFFF
}

def add_user(username, by):
    if not username in ALLOWED:
        ALLOWED[username] = by

    save_users()

def remove_user(username, by):
    if username in ALLOWED:
        del ALLOWED[username]

    save_users()

def _reload():
    allowed = helpers.load_data_for_module(__name__, "allowed", ALLOWED)
    ALLOWED.clear()
    for a in allowed:
        ALLOWED[a] = allowed[a]

    print "LOADED USERS", ALLOWED

def save_users():
    helpers.save_data_for_module(__name__, "allowed", ALLOWED)

_reload()
