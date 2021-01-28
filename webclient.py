import socket
import threading
import sys
import time
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

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def to():
    while True:
        try:
            send(input())
        except:
            print("[SERVER DISCONNECTED]")
            time.sleep(2)
            sys.exit()
            break

def back():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
                new_notification("Chatroom: Message", msg)
        except:
            new_notification("Chatroom: Alert", "[SERVER DISCONNECTED]")
            print("[SERVER DISCONNECTED]")
            time.sleep(2)
            sys.exit()
            break

print("[CONNECTED TO SERVER]")
thread = threading.Thread(target=to)
thread.start()
thread = threading.Thread(target=back)
thread.start()
