import object_picker, listen_to

import reload_cmd

modules = [ object_picker, listen_to, reload_cmd, algos ]

COMMANDS = {}
def _reload():
    print 'LOADING COMMANDS'
    del_keys = COMMANDS.keys()
    for key in del_keys:
        del COMMANDS[key]

    for m in modules:
        reload(m)

    for m in modules:
        for c in m.COMMANDS:
            print 'Loading command %s as %s' % (m.COMMANDS[c], c)
            COMMANDS[c] = m.COMMANDS[c]
