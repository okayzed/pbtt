from . import COMMANDS

lines = [l.strip() for l in sys.stdin.readlines()]


class DummyBot():
    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args):
        print "(NOT) SENDING", *args

for line in lines:
    tokens = line.split(" ")
    if tokens[0] in COMMANDS:
        cmd = tokens.pop(0)
        COMMANDS[cmd](

