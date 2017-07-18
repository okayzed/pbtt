import scripted_helper
import auth
from mannerisms import *

DELIMITER="->"

# an easy script could look like:
# "regex" -> response

# is that lame, though?
def learn_script(bot, data, *args):
    scripted_helper.load_data()
    script = " ".join(args)
    if data["nick"] in auth.OWNERS:
        tokens = script.split(DELIMITER)
        prec = tokens[0]
        prec = prec.replace(" ", ".*")
        prec = prec.replace("_", ".")

        ante = tokens[1]

        antes = ante.split("|")

        for ante in antes:
            script_obj = scripted_helper.Script()
            script_obj.precedent = prec
            script_obj.antecedent = ante
            scripted_helper.SCRIPTS.append(script_obj)
            print "ADDING NEW SCRIPT", script_obj.precedent, script_obj.antecedent

        bot.say(data["nick"] + ":", affirmative())
        scripted_helper.save_data()

def forget_script(bot, data, *args):
    import re

    if data["nick"] in auth.OWNERS:
        full_args = " ".join(args)
        scripted_helper.load_data()
        prec = " ".join(args)
        prec = prec.replace(" ", ".*")
        prec = prec.replace("_", ".")
        
        to_remove = []
        match = re.search("\[(\d+)\]", full_args)

        full_args = re.sub("\[(\d+)\]", "", full_args)
        for script in scripted_helper.SCRIPTS:
            if re.search(prec.strip(), script.precedent.strip()):
                to_remove.append(script)

                print "REMOVE CANDIDATE", script.precedent, script.antecedent

       
        if not to_remove:
            print "NOTHING TO REMOVE..."
            return

        index = 0
        if match:
            index = int(match.group(1))

            if index < 0:
                index += len(cand.answers)

            if index > len(cand.answers):
                return

        print "REMOVING", to_remove[index].precedent, to_remove[index].antecedent
        to_remove.pop(index)

        bot.say(data["nick"] + ":", affirmative())
        scripted_helper.save_data()
    

COMMANDS={}
COMMANDS["!addscript"] = learn_script
COMMANDS["!forgetscript"] = forget_script
