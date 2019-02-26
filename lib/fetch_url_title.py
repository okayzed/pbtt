import requests
import re
from bs4 import BeautifulSoup
def grab_url(line):
    m = re.search("(?P<url>https?://[^\s]+)", line)
    if m:
        return m.group("url")

def print_url_title(response, line, nick):
    url = grab_url(line)
    if not url:
        return

    u  = requests.get(url)
    print "RETRIEVING URL", url
    soup = BeautifulSoup(u._content, "lxml")
    if soup.title:
        response.say("> %s" % soup.title.string)
