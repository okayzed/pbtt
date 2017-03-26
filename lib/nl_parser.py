# declarative parsing for determining information
# about the world.

# previously using textblob to read declarations.
# unfortunately, declarations are pretty annoying
# to read because they can be of so many forms.

# instead, i want to do something like:
# "I am hungry" -> X is hungry
# "I wish I was" -> X is/was
# "I have a cookie" -> X has
# "I was a cookie" -> X was
# "I had a cookie" -> X
import re

def split_sentence(sentence):
    delimiters = ".?!;"

    indices = []
    for d in delimiters:
        s = sentence
        idx = s.find(d)
        prev = 0

        while idx != -1:
            if idx >= len(s) - 1:
                break

            if s[idx+1].strip() == "":
                indices.append(prev + idx + 1)

            prev += idx

            idx += 1
            if idx < len(s):
                s = s[idx:]
            else:
                break

            idx = s.find(d)

            if idx >= len(s) - 1:
                break

    indices.sort()

    p = 0
    ret = []
    i = 0
    for i in indices:
        if p == i:
            continue

        sl = sentence[p:i].strip()

        p = i+1

        if sl:
            ret.append(sl)

    sl = None
    if not indices:
        if i < len(sentence):
            sl = sentence[i:].strip()
    else:
        sl = sentence[i+1:].strip()

    if sl:
        ret.append(sl)
    return ret

def build_declarations(orig_sentence, name="%%NICK%%"):
    if orig_sentence[0] == ":":
        orig_sentence = orig_sentence[1:]

    parsed = split_sentence(orig_sentence)

    declarations = {
        "i thought" : None,
        "i am" : "is",
        "i'm" : "is",
        "i'd" : "would",
        "i generally avoid" : "avoids",
        "i was" : "was",
        "i can" : "can",
        "i could" : "could",
        "i like" : "likes",
        "i had" : "had",
        "i have" : "has",
        "i have" : "has",
        "i don't" : "doesn't",
        "i still have" : "has",
        "i still have not" : "hasn't",
        "i still haven't " : "hasn't",
        "i haven't" : "has not",
        "i have not" : "has not",
        "i've" : "has",
        "i used to have" : "had",
        "i used to" : "used to",
        "i wish i had" : "wants",
        "i wish i was" : "wants to be",
        "i want to be" : "wants to be",
        "i want" : "wants",
        "\x01ACTION " : "",
    }

    replaced_decls = {
        "^i " : " ",
        " i " : " "
    }

    ret = []
    for sent in parsed:
        # look for each declarative statement in the sentence
        lsent = str(sent).lower().strip()

        # you and yours have to replaced
        if lsent.find("your") != -1:
            continue

        rp = sent
        matched = False
        for d in declarations:
            if not matched:
                match = re.match(d, rp.lower(), flags=re.I)
            else:
                match = re.search(d, rp.lower(), flags=re.I)

            if not match:
                continue


            if declarations[d] is None:
                # we skip learning if we set None in the decls dictionary
                break

            matched = True

            print "MATCHED DECL", d
            rp = re.sub(d, name + " " + declarations[d], str(rp), flags=re.I)



        if matched:
            for d in replaced_decls:
                rp = re.sub(d, name + " " + replaced_decls[d], str(rp), flags=re.I)

            rp = re.sub("\x01", "", rp, flags=re.I)
            rp = re.sub("(\W)me(\W)", "\\1them\\2", rp, flags=re.I)
            rp = re.sub("(\W)my(\W)", "\\1their\\2", rp, flags=re.I)
            rp = re.sub("(\W)myself", "\\1themself", rp, flags=re.I)

            ret.append(rp.strip())
            matched = False


    return ret
