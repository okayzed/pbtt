import requests
from lxml import etree

#oeis queries
def oeis(query):
    #correctly format query
    correctQuery = ""
    for char in query:
        try:
            int(char)
            correctQuery += char
        except ValueError:
            if correctQuery[-1] != ',':
                correctQuery += ','
    #search results URL
    URL = "https://oeis.org/search?q=" + correctQuery
    #GET request
    result = requests.get(URL)
    root = etree.HTML(result._content)
    #results information
    resultsElement = root.xpath("//table[@bgcolor='#FFFFCC']")[0]
    resultsInfo = [text.strip() for text in resultsElement.itertext() if text.strip()]
    message = resultsInfo[0]
    try:
        #find element with relevant info (first result)
        linkElement = root.xpath("//tr[@bgcolor='#EEEEFF']")[0]
        linkInfo = [text.strip() for text in linkElement.itertext() if text.strip()]
        sequenceNumber = linkInfo[0]
        sequenceTitle = linkInfo[1]
        #construct link to first result]
        link = "https://oeis.org/" + sequenceNumber
        #first result sequence
        sequence = [text.strip() for text in root.xpath("//tt")[0].itertext() if text.strip() != ',' and text.strip() != '']
        sequence = ', '.join([text.strip(', ') for text in sequence])
        ##add 7 results to sequence, store in sequencePreview
        additionalChars = len(query.split(',')) + 8
        sequencePreview = ''
        commaCounter = 0
        sequenceIndex = 0
        while commaCounter < additionalChars and sequenceIndex < len(sequence):
            if sequence[sequenceIndex] == ',':
                commaCounter += 1
            sequencePreview += sequence[sequenceIndex]
            sequenceIndex += 1
        sequencePreview += ' ...'
        #number of results
        message = message.split(' of ')
        numberOfResults = message[1]
        return '{0} | Title: {1} | Sequence preview: {2} | Link: {3} | Search results: {4}'.format(numberOfResults, sequenceTitle, sequencePreview, link, URL)
    except IndexError:
        if message[0] =='S':
            return "Nothing found."
        elif message[0] == 'F':
            return "Too many results ({0}). Please refine your search.".format(message.split()[1])

def do_oeis(bot, data, *args):
    ans = oeis(" ".join(args))
    bot.say("%s: %s" % (data["nick"], ans))

COMMANDS = {}
COMMANDS["sequence"] = do_oeis
COMMANDS["pattern"] = do_oeis

