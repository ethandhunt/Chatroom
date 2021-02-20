import socket
import threading
import time
import urllib.request
import os
import sys
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
port_got = False
PORT = 55555
FORMAT = 'utf-8'
NICKS = []
VOTE_IN_PROGRESS = False
VOTES = 0
VOTE_ID = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# gets ipv4 address of local machine
# ONLY WORKS ON LOCAL NETWORK
SERVER = socket.gethostbyname(socket.gethostname())
while not port_got:
    ADDR = (SERVER, PORT)
    try:
        server.bind(ADDR)
        port_got = True
        print(f'[PORT] {PORT}')
    except:
        PORT += 1


CLIENTS = []
KICKED_CLIENTS = []


def broadcast(msg):
    try:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        if msg[0] == "@":
            new_notification("Chatroom: Message", msg[1:len(msg)])
        for client in CLIENTS:
            try:
                client.send(send_length)
                client.send(message)
            except:
                print("[ALERT] Client Disconnected, Handling...")
                CLIENTS.remove(client)
    except ConnectionResetError:
        pass
    except:
        print("[ERROR] An Unknown Error Occured")


def send(connection, message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    connection.send(send_length)
    connection.send(message)


def get_clientnum(nick):
    return NICKS.index(nick)


def get_client(nick):
    return CLIENTS[get_clientnum(nick)]


def client_count():
    return len(CLIENTS)

def remove_nick_FULL(nick):
    CLIENTS.remove(get_client(nick))
    NICKS.remove(nick)


def NC_continuity(print_do=False):
    if len(CLIENTS) == len(NICKS):
        if print_do:
            print("NC_Continuity Check Passed")
        return True
    else:
        if print_do:
            print("NC_Continuity Check Failed")
        return False


def votekick_timer(delay, initiator, Subject):
    global VOTES
    global VOTE_IN_PROGRESS
    global VOTE_ID
    VOTES = 0
    time.sleep(delay)
    broadcast("#Votekick Over")
    broadcast(f"#{Subject} got {VOTES} votes against them")
    if VOTES > client_count() / 2:
        broadcast(f"#{VOTES} is greater than half of the current online clients")
        broadcast(f"@{Subject} has been kicked")
        send(get_client(Subject), "!You Have Been Kicked By The Server")
        remove_nick_FULL(Subject)
    else:
        broadcast(f"#{VOTES} is not greater than half of the online clients")
        broadcast(f"#{Subject} has not been kicked")
    VOTES = False
    VOTE_IN_PROGRESS = False
    VOTE_ID += 1


def handle_client(conn, addr, NICKS):
    global CLIENTS
    global KICKED_CLIENTS
    global VOTEKICK_SUBJECT
    global VOTE_IN_PROGRESS
    global VOTES
    Voted = False
    print(f"[NEW CONNECTION] {str(addr)} Connected")
    CLIENTS.append(conn)
    nick = False
    kicked = False
    crrnt_nick = ""
    myclientnum = CLIENTS.index(conn)

    connected = True
    while connected:
        try:
            if nick:
                if myclientnum in KICKED_CLIENTS:
                    kicked = True
                    break
                myclientnum = CLIENTS.index(conn)
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg[0] == "!":
                        print(f"[COMMAND INVOCATION]: [{crrnt_nick}]: {msg}")
                        if msg == "!Ping":
                            send(conn, "!Pong")
                        elif msg[:9] == "!Whisper ":
                            whispersubject = msg.split(" ")[1]
                            if whispersubject in NICKS:
                                clientnum = NICKS.index(whispersubject)
                                send(
                                    CLIENTS[clientnum], f"@WHISPER:[{crrnt_nick}]: {' '.join(msg.split()[2:])}")
                            else:
                                send(conn, f"#Invalid Subject For !Whisper")
                        elif msg[:3] == "!w ":
                            whispersubject = msg.split(" ")[1]
                            if whispersubject in NICKS:
                                clientnum = NICKS.index(whispersubject)
                                send(
                                    CLIENTS[clientnum], f"@WHISPER:[{crrnt_nick}]: {' '.join(msg.split()[2:])}")
                            else:
                                send(conn, f"#Invalid Subject For !Whisper")
                        elif msg == "!Online":
                            for nickname in NICKS:
                                send(conn, f"#{nickname} is Online")
                        elif msg == "!CheckConnec":
                            send(conn, f"!ConnectTrue")
                        elif msg[:9] == "!VoteKick":
                            if not VOTE_IN_PROGRESS:
                                try:
                                    Subject = msg.split(" ")[1]
                                    flag_badsubject = False
                                except:
                                    send(conn, "#Invalid Subject For !Votekick")
                                    flag_badsubject = True
                                if flag_badsubject:
                                    pass
                                elif Subject in NICKS:
                                    if not Subject == crrnt_nick:
                                        VOTEKICK_SUBJECT = Subject
                                        VOTE_IN_PROGRESS = True
                                        broadcast(
                                            f"@{crrnt_nick} has initiated a votekick on {Subject}, use !Vote to vote them out")
                                        thread = threading.Thread(
                                            target=votekick_timer, args=(30, crrnt_nick, Subject))
                                        thread.start()
                                    else:
                                        send(conn, "#You Cannot !VoteKick Yourself")
                                else:
                                    send(
                                        conn, "#Invalid Subject For !VoteKick, That Nick Doesn't Exist")
                            else:
                                send(conn, "#")
                        elif msg == "!Vote":
                            if VOTE_IN_PROGRESS and not Voted:
                                Voted = True
                                Voted_ID = VOTE_ID
                                VOTES += 1
                                send(conn, "#You Have Voted")
                            elif VOTE_IN_PROGRESS and not Voted_ID == VOTE_ID:
                                Voted = True
                                Voted_ID = VOTE_ID
                                VOTES += 1
                                send(conn, "#You Have Voted")
                            else:
                                send(conn, "#You Cannot Vote")
                        else:
                            send(conn, f"@Invalid Command")
                    elif msg[0] == "@":
                        broadcast(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                        print(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                    elif msg[0] == "#":
                        broadcast(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                        print(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
            else:
                send(conn, "#[SERVER] Enter A Nick")
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    crrnt_nick = conn.recv(msg_length).decode(FORMAT)
                    crrnt_nick = crrnt_nick[1:len(crrnt_nick)]
                    if not crrnt_nick == "SERVER" and not crrnt_nick in NICKS and not " " in crrnt_nick:
                        nick = True
                        broadcast(f"@{crrnt_nick} Joined The Chat")
                        print(f"{addr} is now known as {crrnt_nick}")
                        print(f"@{crrnt_nick} Joined The Chat")
                        NICKS += [crrnt_nick]
                    else:
                        send(conn, "#[SERVER] That Nick Wasn't Valid")
        except Exception as err:
            #This is for debugging false disconnects:
            print(err)

            if not kicked:
                connected = False
                try:
                    CLIENTS.remove(conn)
                except:
                    pass
                if nick:
                    try:
                        NICKS.remove(crrnt_nick)
                    except:
                        pass
                    print(f"[DISCONNECT] {crrnt_nick} Disconnected")
                    broadcast(f"@[SERVER] {crrnt_nick} Disconnected")
                    new_notification("Chatroom: Client Disconnect",
                                     f"{crrnt_nick} Disconnected")
                else:
                    print(f"[DISCONNECT] {addr} Disconnected")


def server_chat_and_commands():
    global KICKED_CLIENTS
    while True:
        servertext = input()
        if servertext[0] == "!":
            if servertext[:5] == "!Kick":
                try:
                    target = servertext.split()[1]
                except:
                    print("[ERROR] Command Had No Target")
                if target in NICKS:
                    clientnum = NICKS.index(target)
                    send(CLIENTS[clientnum],
                         "!You Have Been Kicked By The Server")
                    KICKED_CLIENTS.append(clientnum)
                    CLIENTS.pop(clientnum)
                    NICKS.remove(target)
                    broadcast(f"@[SERVER] Kicked {target}")
                    print(f"[SERVER] Kicked {target}")
            elif servertext == "!Update":
                print("Updating")
                fp = urllib.request.urlopen("https://raw.githubusercontent.com/ethandhunt/Chatroom/main/webserver.py")
                mybytes = fp.read()
                string = mybytes.decode("utf-8")
                fp.close()
                file = open("webserver.py", "w")
                file.write(string)
                file.close()
                print("Update Complete")
                print("Relaunch for new update")
                broadcast("@Server has updated")
            else:
                print("Invalid Command")
        else:
            broadcast(f"@[SERVER]: {servertext}")
            print(f"@[SERVER]: {servertext}")


def start():
    server.listen()
    print(f"[IP] {SERVER}")
    thread = threading.Thread(target=server_chat_and_commands)
    thread.start()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client, args=(conn, addr, NICKS))
        thread.start()


start()
