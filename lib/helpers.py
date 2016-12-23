import os
import pickle

def nick_for(sendername):
    exclamationIndex = sendername.find("!")
    return sendername[1:exclamationIndex]


USERS_FILE="users.pickle"

def load_data_for_module(module, key, default=None):
    try:
        os.makedirs("data")
    except OSError:
        pass

    path = os.path.join("data", "%s.%s.pickle" % (module, key))
    data = load_data(path)
    if not data:
        data = default

    return data

def load_data(filename):
    try:
        infile = open(filename, "rb")
        data = pickle.load(infile)
        print "READ %s" % (filename)
        return data
    except:
        pass
   
def save_data(filename, data):
    print "SAVED %s" % (filename)
    outfile = open(filename, "wb")
    pickle.dump(data, outfile)
    outfile.close()

def save_data_for_module(module_name, key, data):
    try:
        os.makedirs("data")
    except OSError:
        pass

    path = os.path.join("data", "%s.%s.pickle" % (module_name, key))
    save_data(path, data)
    
