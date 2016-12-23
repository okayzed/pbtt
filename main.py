import ircbot

if __name__ == "__main__":
    mybot = ircbot.IRC_Bot(botnick=botnick, channel=channel)
    mybot.connect()
    mybot.run_forever()
