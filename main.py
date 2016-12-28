import ircbot

if __name__ == "__main__":
    mybot = ircbot.IRC_Bot()
    mybot.connect()
    mybot.run_forever()
