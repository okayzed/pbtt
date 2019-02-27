== algorithm picking ==

keywords: "ABOUT", "FROM", "THATS"
so it looks like: "<fillwords> <pick|find|suggest> a problem FROM ... ABOUT ... THATS...


pbtt: can you pick a problem from hackerrank?
pbtt: can you pick a problem thats easy from hackerrank?
pbtt: pick a problem from hackerrank thats easy 
pbtt: pick a problem about math #combinatorics (easy or medium) from hackerrank?
pbtt: suggest a problem from hackerrank about algorithms #graph (easy or medium)

== interactions db ==

# add a new scripted interaction
addscript regex -> response1 | response2 | response3
# pbtt will respond with one of the three responses when the below is sent
pbtt: string_that_matches_regex

# example:
pbtt: addscript what type of bot are you? -> i'm not the bot, you're the bot | uhhh...
pbtt: what type of bot are you?


== facts db ==

try to write everything after "learn" as a full sentence. for example:

# is good because the whole statement reads
# as a full sentence
learn "pbtt" is really cool

# is bad because pbtt appears twice in a row and
# the whole statement does not read as a full sentence
learn "pbtt" pbtt is really cool

# this will cause dobby to say 'a new topic and the rest of the details'
# when any word from 'a new topic' is queried if its the best match
pbtt: learn "a new topic" and the rest of the details

# pbtt will say: "the best coding site is codechef" when "coding site" or
# "best site" are asked
pbtt: learn "the best coding site" is codechef
pbtt: recall coding sites

# pbtt will explain its reasoning behind what it said if ~explain
# is added
pbtt: recall topic and ~explain

# use recall[index] to get the next topic
pbtt: recall "a new topic"[1]

# forget a specific definition of a topic
pbtt: forget "key words"[3]

# move a topic into another topic
pbtt: merge "a new topic" into "other topic"

# some examples of adding FILLWORDS
pbtt: what do you recall about leetcode?
pbtt: please recall "a new topic"[2]

# ADVANCED USAGE OF 'remember'. if you have 'WHAT' in
# the stopwords before remember, it recalls a fact
# if not, we learn the fact (as seen below)
# if there is a "?" at the end, we treat it as a query
pbtt: please remember "leetcode is terrible"
pbtt: what do you remember about leetcode?

== interactions ==

pbtt: poke poke
pbtt: hey
pbtt: thanks
pbtt: bye
pbtt: i hate you
