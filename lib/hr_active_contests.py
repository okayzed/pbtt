from lxml import etree
import requests


def filterActiveContests(address):
    #navigate to hackerrank contests page
    result = requests.get("https://www.hackerrank.com/contests")
    root = etree.HTML(result._content)
    
    #filter "view details" links (only active contests have them)
    links = root.xpath("//a[@class='psR psL fnt-wt-500 xsmall details-link']")
    
    #extract contest names through "view details" links
    contests = [link.items()[0][1] for link in links]

    for contest in contests:
        if contest in address and "challenges" in address:
            return True
    return False
