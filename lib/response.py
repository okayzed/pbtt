class Response():
    def __init__(self, *args, **kwargs):
        self.is_whisper = False # for twitch whispers

    def say(self, *args):
        if self.is_whisper:
            self.bot.send("PRIVMSG", self.channel, ":/w", self.from_nick, " ".join(args))
        else:
            self.bot.send("PRIVMSG", self.channel, ":" + " ".join(args))


