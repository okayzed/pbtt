import requests
from lxml import etree

from config import WOLFRAM_APPID

#Wolfram Alpha queries:
def wa(query):
    '''takes a wolfram alpha query (text)
       and returns the answer from the <pod>
       labeled "Result" and returns all <pod>
       info if "Result" doesn't exist'''
    # GET request for xml -- plaintext format
    URL = 'http://api.wolframalpha.com/v2/query?input=' + query + '&appid=' + WOLFRAM_APPID + '&format=image,plaintext'
    correctURL = ''
    for char in URL:
        if char == '+':
            correctURL += '%2B'
        else:
            correctURL += char
    result = requests.get(correctURL)
    # find desired element
    root = etree.XML(result._content)
    try:
        answer_pod = root.xpath("//pod[@title='Result']")[0]
        answer_subpods = [subelement for subelement in answer_pod.getchildren() if subelement.tag == 'subpod']
        # return plaintext answers
        return '|'.join([element.text.encode('utf-8', 'ignore') for subpod in answer_subpods for element in subpod.getchildren() if
                         element.tag == 'plaintext' and element.text])
    # if there is no pod named "Result"
    except IndexError:
        # retrieves all pods that aren't titled "Input interpretation"
        answer_pods = [element for element in root.getchildren() if
                       element.tag == 'pod' and element.get('title') != 'Input interpretation']
        # flattens list of subpods within answer pods
        subpods = [subelement for element in answer_pods for subelement in element.getchildren() if
                   subelement.tag == 'subpod']
        subpod_titles = [element.get('title') for element in subpods]
        # flattens list of plaintext elemends within subpods
        plaintext = [element.text.encode('utf-8', 'ignore') for item in subpods for element in item.getchildren() if element.tag == 'plaintext' and element.text]
        return ', '.join('{0}: {1}'.format(title, value) for title, value in zip(subpod_titles, plaintext))


def do_wolfram(bot, data, *args):
    ans = wa(" ".join(args))
    bot.say("%s: %s" % (data["nick"], ans))

COMMANDS = {}
COMMANDS["wolfram"] = do_wolfram
COMMANDS["wat"] = do_wolfram
COMMANDS["solve"] = do_wolfram
COMMANDS["calculate"] = do_wolfram
