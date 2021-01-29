import urllib.request

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

update("basicupdate.py")
update("autoupdate.py")
update("webserver.py")
update("webclient")
