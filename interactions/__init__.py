import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import poke,greet,scripted
modules = [ poke, greet, scripted ]

INTERACTIONS = []
def _reload():
    print "LOADING INTERACTIONS"
    while INTERACTIONS:
        INTERACTIONS.pop()

    for m in modules:
        reload(m)

    for m in modules:
        for c in m.INTERACTIONS:
            print 'Loading interaction', c
            INTERACTIONS.append(c())

