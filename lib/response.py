class Response():
    def __init__(self, *args, **kwargs):
        pass

    def say(self, *args):
        print "RESPONSE SENDING", args
        self.bot.send("PRIVMSG", self.channel, ":" + " ".join(args))


