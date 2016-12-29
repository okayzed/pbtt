from ircbot import IRC_Bot
import os
import sys

# USED FOR TESTING COMMANDS INSTEAD OF HAVING TO CONNECT TO IRC
from auth import ALLOWED, OWNERS
import mannerisms

class DummyBot(IRC_Bot):
    def readlines(self):
        while True:
            txt=raw_input()
            mannerisms.ACTUALLY_WAIT = False
            if 'NICK' in os.environ:
                nick = os.environ['NICK']
            else:
                nick = OWNERS.keys()[0]

            if 'TO' in os.environ:
                botname = os.environ['TO']
            else:
                botname = self.botnick
            yield ":%s!mydummyurl.10 PRIVMSG %s :%s"%(nick, botname, txt)

    def send(self, *args):
        print "SENDING", args


db = DummyBot()
print "BUILDING DUMMY BOT", db.botnick
db.run_forever()
