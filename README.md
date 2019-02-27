== about ==

pbtt is a simple irc bot that executes commands and interactions.

== running ==

requires python and beautiful soup 4

run `python dummybot.py` to work on new commands and interactions.
run `python main.py` to connect to a real IRC server

== commands ==

commands are specific commands that evoke a specific response. examples:
"reload", "find", etc. any number of FILLWORDs can come before a command, so
'can you reload' is the same as 'please reload' is the same as 'reload'

=== list of commands ===

OWNER ONLY

* channel commands (leave / join channel)
* listen (tell bot to accept commands from new person)
* reload: reload all interactions and commands for bot
 
AUTHORIZED ONLY

* facts: learn, recall (tell, know), merge, forget
* pick object: find, pick, suggest. (only supports algo problem for now)

== interactions ==

interactions are triggers for pbtt to interact back with. these are more
light hearted and do not have actual functional usage. examples would be poking
pbtt or saying hi.

=== list of interactions ===

* greetings: hi, bye, thank
* pokes


== source code ==

can find the commands in src/commands/ and interactions in src/interactions/
