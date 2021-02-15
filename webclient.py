import socket
import threading
import sys
import time
import math
try:
    from notifypy import Notify
except:
    pass

def base_notifc(title, message):
    try:
        notification = Notify()
        notification.title = title
        notification.message = message
        notification.send()
    except:
        pass

def new_notification(title, message):
    thread = threading.Thread(target=base_notifc, args=(title, message))
    thread.start


HEADER = 64
FORMAT = 'utf-8'
#ip configuration
SERVER = input("Enter Local Network Server IP: ")
PORT = int(input("Enter Server Port: "))
ADDR = (SERVER, PORT)
KICKED = False
PingTime = time.time()
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("[ERROR] Port Error, This Port May Already Be In Use On Your Machine")

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
    global PingTime
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
                        elif string == "!Ping":
                            PingTime = time.time()
                            send("!Ping")
                        elif string[:6] == "!File ":
                            try:
                                path = string[6:]
                                file = open(path)
                                send(file.read(), "$")
                                file.close()
                            except Exception as err:
                                print(f"ERROR: {err}")
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
        #try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                if msg[0] == "@":
                    new_notification("Chatroom: Message", msg[1:len(msg)])
                    print(msg[1:len(msg)])
                elif msg[0] == "!":
                    if msg[0:5] == "!Pong":
                        print(f"Round trip time: {time.time() - PingTime}")
                    elif msg == "!You Have Been Kicked By The Server":
                        KICKED = True
                        print("You Have Been Kicked By The Server")
                    elif msg == "!ConnectTrue":
                        connection_confirmed = True
                        print("Connection Confirmed")
                elif msg[0] == "$":
                    file = open("Receive.txt", 'w')
                    file.write(msg[1:])
                    file.close()
                    print("File Received, Saved to Receive.txt")
                else:
                    print(msg[1:len(msg)])

        #except Exception as err:
            #print(err)
            #new_notification("Chatroom: Alert", "[SERVER DISCONNECTED]")
            #print("[SERVER DISCONNECTED]")
            #sys.exit()
            #break

print("[CONNECTED TO SERVER]")
thread = threading.Thread(target=to)
thread.start()
thread = threading.Thread(target=back)
thread.start()
