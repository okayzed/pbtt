from lxml import etree
import requests

def pegFirstParagraph(URL):
    result = requests.get(URL)
    root = etree.HTML(result._content)
    firstParagraph = root.xpath("//p")[0]
    return firstParagraph

def peg(query):
    correctQuery = ''
    for character in query.strip():
        if character == ' ':
            correctQuery += '_'
        else:
            correctQuery += character
    URL = 'http://wcipeg.com/wiki/' + correctQuery
    firstParagraph = pegFirstParagraph(URL)
    explanation = ' '.join([text.strip() for text in firstParagraph.itertext()])
    if "You can search for this page" in explanation:
        a = [link for link in firstParagraph.iter("a")][0]
        newQuery = a.items()[0][1]
        newURL = "http://wcipeg.com" + newQuery
        newFirstParagraph = pegFirstParagraph(newURL)
        explanation = ' '.join([text.strip() for text in newFirstParagraph.itertext()])
        URL = newURL
    lastIndex = 0
    curIndex = 0
    while curIndex < 366 - len(URL) - 15:
        if explanation[curIndex] == '.':
            lastIndex = curIndex
        curIndex += 1
    explanation = explanation[:lastIndex + 1] + ' -- ' + URL
    return explanation


def do_peg(bot, data, *args):
    ans = peg(" ".join(args))
    bot.say("%s: %s" % (data["nick"], ans))

COMMANDS = {}

COMMANDS["research"] = do_peg