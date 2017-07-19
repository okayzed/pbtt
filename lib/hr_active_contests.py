from lxml import etree
import requests


def filterActiveContests(address, response, nick):
    if "hackerrank.com" not in address:
        return None
    #navigate to hackerrank contests page
    result = requests.get("https://www.hackerrank.com/contests")
    root = etree.HTML(result._content)
    
    #filter "view details" links (only active contests have them)
    links = root.xpath("//a[@class='psR psL fnt-wt-500 xsmall details-link']")
    
    #extract contest names through "view details" links
    contests = [link.items()[0][1] for link in links]

    scoldString = "Don't link HR problems for ongoing contests. people will need to register for specific contest to view. Explain problem in a few words instead. If you are kadoban, you should know better by now"

    for contest in contests:
        if contest in address and "challenges" in address:
            response.say("%s: %s" % (nick, scoldString))
