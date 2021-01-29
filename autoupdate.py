#5
#???
import urllib.request
import sys
import threading
import time
CRL = 10
DEPTH = 0


def update(filestr):
    try:
        fp = urllib.request.urlopen(f"https://raw.githubusercontent.com/ethandhunt/Chatroom/main/{filestr}")
        mybytes = fp.read()
        string = mybytes.decode("utf8")
        fp.close()
        try:
            file = open(f"v{filestr}.txt")
            thing = file.read()
            vint = int(thing[1:len(thing)])
            file.close()
        except:
            vint = 0
        if int(string.split("\n")[0][1:len(string.split("\n")[0])]) == vint:
            if DEPTH < CRL:
                print(f"{filestr} source hasn't updated yet, trying again in 20 seconds")
                thread = threading.Thread(target=update, args=filestr)
                time.sleep(20)
                thread.start()
                sys.exit()
            else:
                print("Depth Limit Exceeded, Aborting Update")
        else:
            print("Updated Source Found")
            file = open(f"v{filestr}.txt", "w")
            file.close()
        
        file = open(filestr, "w")
        file.write(string)
        file.close()
        print(f"Updated {filestr}")
    except urllib.error.HTTPError:
        print("That File Doesn't Seem To Exist")


thread = threading.Thread(target=update, args=(["webclient.py"]))
thread.start()
thread = threading.Thread(target=update, args=(["webserver.py"]))
thread.start()
thread = threading.Thread(target=update, args=(["autoupdate.py"]))
thread.start()
input("You Can Close This Window Now")
