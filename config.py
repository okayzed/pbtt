# BOT DEFAULTS
twitch = False
server="chat.freenode.net"
port=6697
channel="##crowtalk"
botnick="jb"
password="nopassass"
WOLFRAM_APPID="DEMO"

# load local settings
import local
reload(local)
try:
    from local import *
except:
    pass

