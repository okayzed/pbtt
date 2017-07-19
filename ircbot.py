#!/usr/local/bin/python

import socket
import ssl
import sys
import datetime
import threading
import time
import Queue
import string


def add_import_paths():
    import os, sys, inspect
    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))

    print "ADDING IMPORT PATH", currentdir, currentdir+"/lib"
    sys.path.insert(0, currentdir)
    sys.path.insert(0, os.path.join(currentdir, "lib"))


add_import_paths()

import auth
import commands
import config
import helpers
import interactions as intrs
import mannerisms
import response
import nl_parser
import hr_active_contests as hac

CHANNEL_CMDS = {"JOIN": 1, "PART": 1, "PRIVMSG": 1}
PRINT_LINES = True

# NOTE:
# reloadables is responsible for reloading modules when reload command is used.
# new modules in lib/ need to be added to it to enforce their reloading
import reloadables
reloadables.load()

SSLError = ssl.SSLError
try:
    SSLError = ssl.SSLWantReadError
except:
    pass


class BotTransferException(Exception):
    pass


class IRC_Bot():
    def __init__(self):
        print "Establishing connection to [%s]" % (config.server)
        self.server = config.server
        self.port = config.port
        self.channel = config.channel
        self.botnick = config.botnick
        self.password = config.password
        self.twitch = config.twitch
        self.members = {}

        if self.twitch:
            self.send("CAP REQ :twitch.tv/commands")
            self.send("CAP REQ :twitch.tv/membership")

        self.cooldown = {}
        self.history = {}
        self.expired = False

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

        self.join_channel(self.channel)


    def join_channel(self, channel):
        self.send("JOIN", channel)
        self.send("WHO", channel)

    def leave_channel(self, channel):
        print "LEAVING CHANNEL", channel
        self.send("PART", channel)
        if channel in self.members:
            del self.members[channel]

    # *args is default arguments
    # self.send(a, b, c, d='f', e='g')
    # args = [a,b,c]
    # kwargs = { d: 'f', e: 'g' }
    def send(self, *args, **kwargs):
        msg_str = " ".join(args)
        self.debug("SENDING", msg_str.strip())
        self.s_mutex.acquire()
        self.irc.send(msg_str + "\r\n")
        self.s_mutex.release()

    def say(self, *args):
        self.send("PRIVMSG", self.channel, ":" + " ".join(args))

    def debug(self, *args):
        now = datetime.datetime.now()
        print str(now), " ".join(map(str, args))

    # this is a generator function that uses our irc socket connection to read
    # and stitch together lines from the network
    def readlines(self):
        irc = self.irc
        overflow = ""

        input_queue = Queue.Queue()

        def add_input(input_queue):
            while True:
                input_queue.put(sys.stdin.read(1))

        input_thread = threading.Thread(target=add_input, args=(input_queue, ))
        input_thread.daemon = True
        input_thread.start()

        next_sleep = 0.0
        waiting_input = []
        while True:
            # if we previously received a line, we try not to sleep
            # if we timed out, we sleep 0.1 seconds
            time.sleep(next_sleep)
            if self.expired:
                print "EXPIRING OLD BOT"
                break

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
        rsp = response.Response()
        rsp.bot = self
        rsp.is_whisper = False
        rsp.channel = cmd_data["channel"]
        rsp.from_nick = cmd_data["nick"]

        if rsp.channel == self.botnick:
            # in twitch mode, we use :/w to whisper instead of privmsg
            if self.twitch:
                rsp.is_whisper = True
            else:
                rsp.channel = rsp.from_nick

        self.debug("MAKING RESPONSE FOR", cmd_data)

        return rsp

    def handle_numeric_reply(self, sendername, intcommand, tokens):
        if intcommand == 352:  # nick in USE?!
            to = tokens.pop(0)
            channel = tokens.pop(0)
            username = tokens.pop(0)
            hostname = tokens.pop(0)
            server = tokens.pop(0)
            nick = tokens.pop(0)

            self.handle_join(":%s!%s" % (nick, hostname), channel)

        if intcommand == 433:  # nick in USE?!
            self.botnick = self.botnick + "_"
            self.debug("NICK ALREADY IN USE, SWITCHING TO %s" % self.botnick)
            self.send("NICK", self.botnick)
            self.join_channel(self.channel)

    def handle_opcode_reply(self, sendername, command, tokens):
        channel = None
        if command in CHANNEL_CMDS:
            channel = tokens.pop(0).strip()

        if command == "PRIVMSG":
            self.handle_privmsg_with_cooldown(sendername, channel, tokens)
        if command == "WHISPER":
            self.handle_privmsg_with_cooldown(sendername, self.botnick, tokens)
        elif command == "JOIN":
            self.handle_join(sendername, channel)
        elif command == "PART":
            self.handle_part(sendername, channel)


    def add_line_to_history(self, sendername, channel, tokens):
        if not channel in self.history:
            self.history[channel] = []

        # record history
        nick = helpers.nick_for(sendername)
        line = " ".join(tokens)
        self.history[channel].append((sendername, line))

        MAX_HISTORY=200
        while len(self.history[channel]) > MAX_HISTORY:
            self.history[channel].pop(0)

    def handle_unaddressed_line(self, sendername, channel, tokens):
        nick = helpers.nick_for(sendername)

        # if the message was addressed to someone, remove the prefix
        # so we can try and learn any declarations they made to the
        # other person. maybe we should keep around the fact about
        # who they told?
        if channel in self.members:
            members = self.members[channel]
            while tokens:
                word = tokens[0].translate(None, string.punctuation).strip()

                if word in members:
                    tokens.pop(0)
                else:
                    break

        line = " ".join(tokens)

        #filter out hackerrank stuff
        scoldString = "Don't link HR problems from ongoing contests, people will need to register for specific contest to view. Explain problem in a few words instead. If you are kadoban, you should know better by now ~love, cherim"

        if "hackerrank.com" in line:
            if hac.filterActiveContests(line):
                response = self.make_response({"nick": nick, "channel": channel})
                response.say(nick + ": " + scoldString)

        decls = nl_parser.build_declarations(line, name=nick)
        if not decls:
            return

        for decl in decls:
            # add a new fact, like: nick, is, sentence
            sentence = " ".join(decl.split(" "))
            print "SAVING DECLARATION", sentence
            commands.facts.load_data()
            cand = commands.facts.Topic(sentence)
            DECL="decl"
            cand.topic.add(DECL)
            commands.facts.FACTS.append(cand)
            commands.facts.save_data()


    def handle_privmsg_with_cooldown(self, sendername, channel, tokens):
        self.debug("RECEIVING PRIVMSG", sendername, channel, tokens)
        to = tokens[0]

        self.add_line_to_history(sendername, channel, tokens)

        if to.find(self.botnick) != 1:
            if channel == self.botnick:
                tokens.insert(0, ":" + self.botnick)
            else:
                self.handle_unaddressed_line(sendername, channel, tokens)
                return

        if not sendername in self.cooldown:
            self.cooldown[sendername] = [(sendername, channel, tokens)]

            def cb():
                if sendername in self.cooldown:
                    if not self.cooldown[sendername]:
                        self.debug("REMOVING %s FROM COOLDOWN" % sendername)
                        del self.cooldown[sendername]
                    else:
                        try:
                            args = self.cooldown[sendername].pop(0)
                            self.handle_privmsg(*args)
                        finally:
                            response_thread = threading.Timer(3, cb)
                            response_thread.start()

            if mannerisms.ACTUALLY_WAIT:
                response_thread = threading.Timer(3, cb)
            else:
                response_thread = threading.Timer(0.1, cb)

            response_thread.start()
        else:
            self.cooldown[sendername].append((sendername, channel, tokens))
            self.cooldown[sendername] = self.cooldown[sendername][-3:]

        self.debug("COOLDOWN", self.cooldown)

    def handle_privmsg(self, sendername, channel, tokens):
        to = tokens.pop(0)
        exclamationIndex = sendername.find("!")
        nick = sendername[1:exclamationIndex]

        self.debug("HANDLING PRIVMSG", sendername, channel, tokens)
        all_tokens = [t for t in tokens]
        addressed_to_bot = False
        if to.find(self.botnick) == 1:
            addressed_to_bot = True

        needs_explain = False
        for t in tokens:
            if t.find("~explain") != -1:
                needs_explain = True

        # order of our router resolution is:
        # COMMAND PHRASE: single phrase
        # COMMAND: STOPWRODS COMMAND ARGS
        # INTERACTION: PHRASE
        if addressed_to_bot and nick in auth.ALLOWED:
            stopwords = set()

            orig_cmd = tokens.pop(0).lower().strip()
            if orig_cmd[0] == ":":
                orig_cmd = orig_cmd[1:]

            cmd = orig_cmd.translate(None, string.punctuation).strip()
            while cmd in mannerisms.FILLWORDS and tokens:
                stopwords.add(cmd)
                orig_cmd = tokens.pop(0).lower()
                cmd = orig_cmd.translate(None, string.punctuation)

                if cmd == "":
                    cmd = "hey"

            cmd_data = {
                "sender": sendername,
                "channel": channel,
                "stopwords": stopwords,
                "nick": helpers.nick_for(sendername),
                "tokens": tokens,
                "explain": needs_explain
            }

            if cmd in commands.COMMANDS or orig_cmd in commands.COMMANDS:
                if cmd in commands.COMMANDS:
                    cmd_data["cmd"] = cmd
                else:
                    cmd_data["cmd"] = orig_cmd

                cmd_data["tokens"] = tokens
                self.do_command(cmd_data)
            else:
                cmd_data["tokens"] = all_tokens
                self.do_interact(cmd_data)

    def handle_join(self, sendername, channel):
        nick = helpers.nick_for(sendername)

        if not channel in self.members:
            self.members[channel] = {}

        self.members[channel][nick] = sendername

    def handle_part(self, sendername, channel):
        nick = helpers.nick_for(sendername)

        if not channel in self.members:
            return

        if nick in self.members[channel]:
            del self.members[channel][nick]

    def do_command(self, cmd_data):
        cmd = cmd_data["cmd"]
        tokens = cmd_data["tokens"]

        if cmd in commands.COMMANDS:
            self.debug("RECEIVED COMMAND", cmd)

            bot_response = self.make_response(cmd_data)
            commands.COMMANDS[cmd](bot_response, cmd_data, *tokens)

    # we need to create a cooldown period for
    # anyone not in our list of authorized users
    # this way we can prevent them from noticing our bottiness
    def do_interact(self, cmd_data):
        import string

        nick = cmd_data["nick"]
        auth_nick = nick
        if "auth_nick" in cmd_data:
            auth_nick = cmd_data["auth_nick"]

        if auth_nick not in auth.ALLOWED and "*" not in auth.ALLOWED:
            import random
            if random.random() > 0.9:
                self.say("%s: %s" % (nick, huh()))
            return

        cmd_data["tokens"] = [
            t.translate(None, string.punctuation).lower()
            for t in cmd_data["tokens"]
        ]

        tokens = cmd_data["tokens"]
        self.debug("INTERACTIONS", tokens)
        bot_response = self.make_response(cmd_data)

        interactions = []

        for interaction in intrs.INTERACTIONS:
            score = interaction.score(cmd_data, tokens)

            if score and score > 0:
                interactions.append((score, interaction))

        if interactions:
            interactions.sort()
            self.debug("LIKELY INTERACTIONS", interactions)
            mannerisms.wait_small(
                lambda: interactions[-1][1].do(bot_response, cmd_data, tokens))

    def run_forever(self):
        self.debug("RUNNING FOREVER")
        for line in self.readlines():
            # Prevent Timeout
            if PRINT_LINES:
                self.debug(line.strip("\r\n "))
            if line.find('PING') != -1:
                self.debug("PONGING...")
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
                except BotTransferException, e:
                    break
                except Exception, e:
                    print "EXCEPTION!", str(e)
                except KeyboardInterrupt, e:
                    break
