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
    prev = 0
    for d in delimiters:
        s = sentence
        idx = s.find(d)

        while idx != -1:
            indices.append(prev + idx)
            prev += idx

            idx += 1
            if idx < len(s):
                s = s[idx:]
            else:
                break

            idx = s.find(d)

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

def build_declarations(orig_sentence):
    if orig_sentence[0] == ":":
        orig_sentence = orig_sentence[1:]

    parsed = split_sentence(orig_sentence)
    print "PARSED", parsed

    declarations = {
        "i thought" : None,
        "i am" : "is",
        "i'm" : "is",
        "i generally avoid" : "avoids",
        "i was" : "was",
        "i had" : "had",
        "i have" : "has",
        "i don't" : "doesn't",
        "i haven't" : "has not",
        "i have not" : "has not",
        "i've" : "has",
        "i used to have" : "had",
        "i used to" : "used to",
        "i wish i had" : "wants",
        "i wish i was" : "wants to be",
        "i want to be" : "wants to be",
        "i want" : "wants",
    }

    ret = []
    for sent in parsed:
        # look for each declarative statement in the sentence
        lsent = str(sent).lower().strip()
        rp = None
        for d in declarations:
            match = re.match(d, lsent)
            if not match:
                continue


            if declarations[d] is None:
                # we skip learning if we set None in the decls dictionary
                break

            rp = re.sub(d, declarations[d], lsent)
            ret.append(("", rp.strip()))

            break

    return ret
