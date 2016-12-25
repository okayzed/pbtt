class Response():
    def __init__(self, *args, **kwargs):
        pass

    def say(self, *args):
        self.bot.send("PRIVMSG", self.channel, ":" + " ".join(args))


