import channel
import facts
import interact
import listen_to
import reload_cmd
import scripted
import wolfram
import oeis

# algos needs to come before object picker, apparently
modules = [
    interact,
    listen_to,
    reload_cmd,
    channel,
    facts,
    scripted,
    # misc
    wolfram,
    oeis
]


COMMANDS = {}
def _reload():
    print 'LOADING COMMANDS'
    del_keys = COMMANDS.keys()
    errs = []
    for key in del_keys:
        del COMMANDS[key]

    for m in modules:
        try:
            reload(m)
        except Exception, e:
            errs.append((m,e))

    for m in modules:
        for c in m.COMMANDS:
            print 'Loading command %s as %s' % (m.COMMANDS[c], c)
            COMMANDS[c] = m.COMMANDS[c]

    for m,e in errs:
        print m,e
