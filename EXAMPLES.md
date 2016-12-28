== algorithm picking ==

keywords: "ABOUT", "FROM", "THATS"
so it looks like: "<fillwords> <pick|find|suggest> a problem FROM ... ABOUT ... THATS...


dobodob: can you pick a problem from hackerrank?
dobodob: can you pick a problem thats easy from hackerrank?
dobodob: pick a problem from hackerrank thats easy 
dobodob: pick a problem about math #combinatorics (easy or medium) from hackerrank?
dobodob: suggest a problem from hackerrank about algorithms #graph (easy or medium)

== interactions db ==

# add a new scripted interaction
addscript regex -> response1 | response2 | response3
# dobodob will respond with one of the three responses when the below is sent
dobodob: string_that_matches_regex

# example:
dobodob: addscript what type of bot are you? -> i'm not the bot, you're the bot | uhhh...
dobodob: what type of bot are you?


== facts db ==

try to write everything after "learn" as a full sentence. for example:

# is good because the whole statement reads
# as a full sentence
learn "dobodob" is really cool

# is bad because dobodob appears twice in a row and
# the whole statement does not read as a full sentence
learn "dobodob" dobodob is really cool

# this will cause dobby to say 'a new topic and the rest of the details'
# when any word from 'a new topic' is queried if its the best match
dobodob: learn "a new topic" and the rest of the details

# dobodob will say: "the best coding site is codechef" when "coding site" or
# "best site" are asked
dobodob: learn "the best coding site" is codechef
dobodob: recall coding sites

# dobodob will explain its reasoning behind what it said if ~explain
# is added
dobodob: recall topic and ~explain

# use recall[index] to get the next topic
dobodob: recall "a new topic"[1]

# forget a specific definition of a topic
dobodob: forget "key words"[3]

# move a topic into another topic
dobodob: merge "a new topic" into "other topic"

# some examples of adding FILLWORDS
dobodob: what do you recall about leetcode?
dobodob: please recall "a new topic"[2]

# ADVANCED USAGE OF 'remember'. if you have 'WHAT' in
# the stopwords before remember, it recalls a fact
# if not, we learn the fact (as seen below)
# if there is a "?" at the end, we treat it as a query
dobodob: please remember "leetcode is terrible"
dobodob: what do you remember about leetcode?

== interactions ==

dobodob: poke poke
dobodob: hey
dobodob: thanks
dobodob: bye
dobodob: i hate you
