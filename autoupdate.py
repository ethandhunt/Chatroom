#1
import urllib.request
import sys
import threading
import time
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
            if DEPTH < 10:
                print(f"{filestr} source hasn't updated yet, trying again in 20 seconds")
                thread = threading.Thread(target=update, args=filestr)
                time.sleep(20)
                thread.start()
            else:
                print("Depth Limit Exceeded, Aborting Update")
            sys.exit()
        else:
            print("Updated Source Found")
            file = open(f"v{filestr}.txt", "w")
            vstr = file.write(string.split("\n")[0])
            file.close()
        
        file = open(filestr, "w")
        file.write(string)
        file.close()
        print(f"Updated {filestr}")
    except urllib.error.HTTPError:
        print("That File Doesn't Seem To Exist")


update("webclient.py")
update("webserver.py")
update("autoupdate.py")
input("You Can Close This Window Now")
