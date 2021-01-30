#10
import sys
import threading
import time
import urllib.request

CRL = 3


def update(filestr, DEPTH=0):
    try:
        fp = urllib.request.urlopen(
            f"https://raw.githubusercontent.com/ethandhunt/Chatroom/main/{filestr}")
        mybytes = fp.read()
        newstring = mybytes.decode("utf8")
        fp.close()
        try:
            file = open(f"{filestr}")
            oldstring = file.read()
            file.close()
            if newstring == oldstring:
                if DEPTH < CRL:
                    DEPTH += 1
                    print(
                        f"[{filestr}] Source hasn't updated yet, trying again in 20 seconds")
                    thread = threading.Thread(
                        target=update, args=(filestr, DEPTH))
                    time.sleep(20)
                    thread.start()
                else:
                    print(f"[{filestr}] Aborting Update")
            else:
                print(f"[{filestr}] Updated Source Found")
                file = open(filestr, "w")
                file.write(newstring)
                file.close()
                print(f"[{filestr}] Update Complete")
        except:
            file = open(filestr, "w")
            file.write(newstring)
            file.close()
            print(f"[{filestr}] Install Complete")

    except urllib.error.HTTPError:
        print(f"[{filestr}] That File Doesn't Seem To Exist")


def do_update(filestr):
    update(filestr)


thread = threading.Thread(target=do_update, args=(["webclient.py"]))
thread.start()
thread = threading.Thread(target=do_update, args=(["webserver.py"]))
thread.start()
thread = threading.Thread(target=do_update, args=(["autoupdate.py"]))
thread.start()
thread = threading.Thread(target=do_update, args=(["basicupdate.py"]))
thread.start()
thread = threading.Thread(target=do_update, args=(["client_commands.txt"]))
thread.start()
thread = threading.Thread(target=do_update, args=(["server_commands.txt"]))
thread.start()
