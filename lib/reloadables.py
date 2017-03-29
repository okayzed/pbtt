import commands
import mannerisms
import helpers
import auth
import interactions as intrs
import response
import parser

import nl_parser


reloadables = [mannerisms, helpers, auth, intrs, commands, response, parser, nl_parser]

def load():
    for r in reloadables:
        reload(r)
        if hasattr(r, '_reload'):
            r._reload()