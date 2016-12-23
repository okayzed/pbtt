#!/usr/local/bin/python

import socket
import ssl
import sys
import threading
import time
import Queue
import string


def add_import_paths():
    import os,sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    sys.path.insert(0,currentdir) 
    sys.path.insert(0,os.path.join(currentdir, "lib")) 

add_import_paths()

import commands
import mannerisms
import helpers
import auth
import interactions as intrs
import response

reloadables = [mannerisms, helpers, auth, intrs, commands, response]

CHANNEL_CMDS = {"JOIN": 1, "PART": 1, "PRIVMSG": 1}
PRINT_LINES = True

botnick = "mybot"
channel = "##crowtalk"

def load():
    for r in reloadables:
        reload(r)
        if hasattr(r, '_reload'):
            r._reload()
load()

# load local settings
try:
    from local import *
except:
    pass

SSLError = ssl.SSLError
try:
    SSLError = ssl.SSLWantReadError
except:
    pass
    
class IRC_Bot():
    def __init__(self,
                 server="chat.freenode.net",
                 port=6697,
                 channel="##crowtalk",
                 botnick="jb",
                 password="nopassass"):

        print "Establishing connection to [%s]" % (server)
        self.server = server
        self.port = port
        self.channel = channel
        self.botnick = botnick
        self.password = password

        self.cooldown = {}

        self.s_mutex = threading.Lock()

    # connects to the IRC server using the settings
    # supplied in __init__
    def connect(self):
        #defines the socket
        irc = self.irc = ssl.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        # Connect
        irc.connect((self.server, self.port))
        irc.setblocking(False)
        self.send("PASS", self.password)

        # https://tools.ietf.org/html/rfc2812#section-3.1.3
        mode = '0'
        unused = '*'

        client = ":tobi-chat"

        self.send("USER", self.botnick, mode, unused, client)
        self.send("NICK", self.botnick)
        self.send("PRIVMSG nickserv :identify %s %s\r\n" %
                  (self.botnick, self.password))
        self.send("JOIN", self.channel)

    # *args is default arguments
    # self.send(a, b, c, d='f', e='g')
    # args = [a,b,c]
    # kwargs = { d: 'f', e: 'g' }
    def send(self, *args, **kwargs):
        msg_str = " ".join(args)
        print "SENDING", msg_str.strip()
        self.s_mutex.acquire()
        self.irc.send(msg_str + "\r\n")
        self.s_mutex.release()

    def say(self, *args):
        self.send("PRIVMSG", self.channel, ":" + " ".join(args))

    # this is a generator function that uses our irc socket connection to read
    # and stitch together lines from the network
    def readlines(self):
        irc = self.irc
        overflow = ""

	input_queue = Queue.Queue()

	def add_input(input_queue):
	    while True:
		input_queue.put(sys.stdin.read(1))

	input_thread = threading.Thread(target=add_input, args=(input_queue,))
	input_thread.daemon = True
	input_thread.start()

        next_sleep = 0.0
	waiting_input = []
        while True:
            # if we previously received a line, we try not to sleep
            # if we timed out, we sleep 0.1 seconds
            time.sleep(next_sleep)

	    while not input_queue.empty():
                q = input_queue.get()
                if q == '\n':
                    flush = "".join(waiting_input)
                    waiting_input = []
                    self.say(flush)
                else:
                    waiting_input.append(q)	

            try:
                # if the last character is not a newline, we hold onto the
                # characters from the previous newline and feed them to the
                # next line (because we might have a partially interrupted
                # line)
                text = overflow + irc.recv(2040)
                last_newline = text.rfind('\n') + 1
                next_sleep = 0.0

                if last_newline > 0:
                    overflow = text[last_newline + 1:]
                    text = text[:last_newline]
                else:
                    next_sleep = 0.1

                lines = text.split("\n")
                for line in lines:
                    l = line.strip()
                    if not l:
                        continue

                    yield l

            except Exception, e:
                if type(e) == SSLError:
                    next_sleep = 0.1
                    continue
                print e

    def make_response(self, cmd_data):
        bot = response.Response()
        bot.bot = self
        bot.channel = cmd_data["channel"]
        bot.from_nick = cmd_data["nick"]
        if bot.channel == self.botnick:
            bot.channel = bot.from_nick

        print "MAKING RESPONSE FOR", cmd_data

        return bot

    def handle_numeric_reply(self, sendername, intcommand, tokens):
        if intcommand == 433: # nick in USE?!
            self.botnick = self.botnick + "_"
            print "NICK ALREADY IN USE, SWITCHING TO %s" % self.botnick
            self.send("NICK", self.botnick)
            self.send("JOIN", self.channel)


            

    def handle_opcode_reply(self, sendername, command, tokens):
        channel = None
        if command in CHANNEL_CMDS:
            channel = tokens.pop(0).strip()

        if command == "PRIVMSG":
            self.handle_privmsg_with_cooldown(sendername, channel, tokens)
        elif command == "JOIN":
            self.handle_join(sendername, channel)
        elif command == "PART":
            self.handle_part(sendername, channel)

    def handle_privmsg_with_cooldown(self, sendername, channel, tokens):
        print "HANDLING PRIVMSG", sendername, channel, tokens
        to = tokens[0]
        if to.find(self.botnick) != 1:
            return

        if not sendername in self.cooldown:
            self.cooldown[sendername] = [(sendername, channel, tokens)]
            

            def cb():
                if sendername in self.cooldown:
                    if not self.cooldown[sendername]:
                        print "REMOVING %s FROM COOLDOWN" % sendername
                        del self.cooldown[sendername]
                    else:
                        try:
                            args = self.cooldown[sendername].pop(0)
                            self.handle_privmsg(*args)
                        finally:
                            response_thread = threading.Timer(3, cb)
                            response_thread.start()

            cb()
        else:
            self.cooldown[sendername].append((sendername, channel, tokens))
            self.cooldown[sendername] = self.cooldown[sendername][-3:]

        print "COOLDOWN", self.cooldown
            

        
    def handle_privmsg(self, sendername, channel, tokens):
        to = tokens.pop(0)
        exclamationIndex = sendername.find("!")
        nick = sendername[1:exclamationIndex]

        print "HANDLING PRIVMSG", sendername, channel, tokens
        all_tokens = [t for t in tokens]
        if to.find(self.botnick) == 1 and nick in auth.ALLOWED:
            cmd = tokens.pop(0)
            cmd = cmd.translate(None, string.punctuation)
            while cmd in mannerisms.FILLWORDS and tokens:
                cmd = tokens.pop(0)
                cmd = cmd.translate(None, string.punctuation)

                if cmd == "":
                    cmd = "hey"

            print "CMD", cmd

            if cmd in commands.COMMANDS:
                self.do_command(sendername, channel, cmd, tokens)
            else:
                self.do_interact(sendername, channel, all_tokens)

    def handle_join(self, sendername, channel):
        exclamationIndex = sendername.find("!")
        nick = sendername[1:exclamationIndex]

    def handle_part(self, sendername, channel):
        pass

    def do_command(self, sendername, channel, cmd, tokens):
        if cmd in commands.COMMANDS:
            cmd_data = {
                "cmd" : cmd,
                "sender" : sendername,
                "channel" : channel,
                "nick" : helpers.nick_for(sendername)
            }

            bot_response = self.make_response(cmd_data)
            commands.COMMANDS[cmd](bot_response, cmd_data, *tokens)

    # we need to create a cooldown period for
    # anyone not in our list of authorized users
    # this way we can prevent them from noticing our bottiness
    def do_interact(self, sendername, channel, tokens):
        nick = helpers.nick_for(sendername)
        interactions = []
            
        import string
        tokens = [ t.translate(None, string.punctuation) for t in tokens ]
        print "INTERACTIONS", tokens

        cmd_data = {
            "sender" : sendername,
            "nick" : helpers.nick_for(sendername),
            "channel" : channel
        }

        bot_response = self.make_response(cmd_data)

        if nick not in auth.ALLOWED and "*" not in auth.ALLOWED:
            if random.random() > 0.9:
                self.say("%s: %s" % (nick, huh()))
            return

        for interaction in intrs.INTERACTIONS:
            score = interaction.score(cmd_data, tokens)

            if score and score > 0:
                interactions.append((score, interaction))


        if interactions:
            interactions.sort()
            print "LIKELY INTERACTIONS", interactions
            mannerisms.wait_small(lambda: interactions[-1][1].do(bot_response, cmd_data, tokens))
            

    def run_forever(self):
        for line in self.readlines():
            # Prevent Timeout
            if PRINT_LINES:
                print line.strip("\r\n ")
            if line.find('PING') != -1:
                print "PONGING..."
                self.irc.send('PONG ' + line.split()[1] + '\r\n')
                continue

            tokens = line.split(" ")
            if len(tokens) >= 3:
                sendername = tokens.pop(0).strip()
                command = tokens.pop(0).strip()

                intcommand = -1
                try:
                    intcommand = int(command)
                except ValueError:
                    pass

                try:
                    if intcommand != -1:
                        self.handle_numeric_reply(sendername, intcommand,
                                                  tokens)
                    else:
                        self.handle_opcode_reply(sendername, command, tokens)
                except Exception, e:
                    print e

