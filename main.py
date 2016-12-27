import ircbot

if __name__ == "__main__":
    mybot = ircbot.IRC_Bot(
        server=ircbot.server,
        botnick=ircbot.botnick, 
        channel=ircbot.channel,
        password=ircbot.password,
        twitch=ircbot.twitch
        )
    mybot.connect()
    mybot.run_forever()
