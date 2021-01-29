#1
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
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("[ERROR] Port Error, This Port May Already Be In Use On Your Machine")
client.connect(ADDR)

def send(msg, type):
    message = (f"{type}{msg}").encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def to():
    while True:
        try:
            string = input()
            if string[0] == "!":
                send(string, "")
            else:
                send(string, "#")
        except:
            print("[SERVER DISCONNECTED]")
            sys.exit()
            break

def back():
    while True:
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
