#4
import socket
import threading
import sys
import time
import math
try:
    from notifypy import Notify
except:
    pass
def new_notification(title, message):
    try:
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.send()
    except:
        pass


HEADER = 64
FORMAT = 'utf-8'
#ip configuration
SERVER = input("Enter Local Network Server IP: ")
PORT = int(input("Enter Server Port: "))
ADDR = (SERVER, PORT)
KICKED = False
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("[ERROR] Port Error, This Port May Already Be In Use On Your Machine")
client.connect(ADDR)

def send(msg, type = ""):
    message = (f"{type}{msg}").encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def checkconnectiontimer(delay):
    global connection_confirmed
    global KICKED
    connection_confirmed = False
    time.sleep(delay)
    if not connection_confirmed:
        KICKED = True


def to():
    global KICKED
    while not KICKED:
        if not KICKED:
            try:
                string = input()
                if KICKED:
                    sys.exit()
                if not string == "":
                    if string[0] == "!":
                        if string == "!CheckConnection" or string == "!CheckConnec" or string == "!Chc":
                            send("!CheckConnec")
                            thread = threading.Thread(target=checkconnectiontimer, args=(10,))
                            thread.start()
                        else:
                            send(string)
                    else:
                        send(string, "#")
            except:
                print("[SERVER DISCONNECTED]")
                sys.exit()
                break

def back():
    global connection_confirmed
    global KICKED
    while not KICKED:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg[0] == "@":
                    new_notification("Chatroom: Message", msg[1:len(msg)])
                    print(msg[1:len(msg)])
                elif msg[0] == "!":
                    if msg[0:5] == "!Ping":
                        servertime = float(msg[5:len(msg)])
                        print(math.sqrt((time.time() - servertime) ** 2))
                    elif msg == "!You Have Been Kicked By The Server":
                        KICKED = True
                        print("You Have Been Kicked By The Server")
                    elif msg == "!ConnectTrue":
                        connection_confirmed = True
                        print("Connection Confirmed")

                else:
                    print(msg[1:len(msg)])

        except:
            new_notification("Chatroom: Alert", "[SERVER DISCONNECTED]")
            print("[SERVER DISCONNECTED]")
            sys.exit()
            break

print("[CONNECTED TO SERVER]")
thread = threading.Thread(target=to)
thread.start()
thread = threading.Thread(target=back)
thread.start()
