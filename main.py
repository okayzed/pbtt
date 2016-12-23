import ircbot

if __name__ == "__main__":
    mybot = ircbot.IRC_Bot(botnick=ircbot.botnick, channel=ircbot.channel)
    mybot.connect()
    mybot.run_forever()
