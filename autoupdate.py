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
        print(f"Updated {filestr}")
    except urllib.error.HTTPError:
        print("That File Doesn't Seem To Exist")

update("webclient.py")
update("webserver.py")
update("README.md")
update("autoupdate.py")
input("You Can Close This Window Now")
