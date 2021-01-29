#3
import urllib.request
import threading

def update(filestr):
    try:
        fp = urllib.request.urlopen(f"https://raw.githubusercontent.com/ethandhunt/Chatroom/main/{filestr}")
        mybytes = fp.read()
        string = mybytes.decode("utf8")
        fp.close()
        
        file = open(filestr, "w")
        file.write(string)
        file.close()
        print(f"[{filestr}] Update Complete")
    except urllib.error.HTTPError:
        print(f"[{filestr}] That File Doesn't Seem To Exist")

def do_update(filestr):
    thread = threading.Thread(target=update, args=filestr)

do_update("basicupdate.py")
do_update("autoupdate.py")
do_update("webserver.py")
do_update("webclient.py")