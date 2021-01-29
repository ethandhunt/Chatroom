import socket
import threading
import time
try:
    from notifypy import Notify

    def new_notification(title, message):
        try:
            notification = Notify()
            notification.title = title
            notification.message = message
            notification.send()
        except:
            pass
except:
    pass

HEADER = 64
port_got = False
PORT = 5050
FORMAT = 'utf-8'
NICKS = []
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


def handle_client(conn, addr, NICKS):
    print(f"[NEW CONNECTION] {str(addr)} Connected")
    CLIENTS.append(conn)
    nick = False
    nicks = NICKS
    crrnt_nick = ""

    connected = True
    while connected:
        try:
            if nick:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    if msg[0] == "!":
                        print(f"{crrnt_nick} sent a command string")
                        print(msg)
                        if msg == "!Ping":
                            print(f"{crrnt_nick} sent a !Ping command")
                            message = (f"!Ping{time.time()}").encode(FORMAT)
                            msg_length = len(message)
                            send_length = str(msg_length).encode(FORMAT)
                            send_length += b' ' * (HEADER - len(send_length))
                            conn.send(send_length)
                            conn.send(message)
                    elif msg[0] == "@":
                        broadcast(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                        print(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                    elif msg[0] == "#":
                        broadcast(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
                        print(f"{msg[0]}[{crrnt_nick}]: {msg[1:len(msg)]}")
            else:
                message = ("#[SERVER] Enter A Nick").encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(message)
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    crrnt_nick = conn.recv(msg_length).decode(FORMAT)
                    crrnt_nick = crrnt_nick[1:len(crrnt_nick)]
                    if not crrnt_nick == "SERVER" and not crrnt_nick in nicks:
                        nick = True
                        broadcast(f"@{crrnt_nick} Joined The Chat")
                        print(f"{addr} is now known as {crrnt_nick}")
                        print(f"@{crrnt_nick} Joined The Chat")
                        NICKS += [crrnt_nick]
                    else:
                        message = (
                            "#[SERVER] That Nick Wasn't Valid").encode(FORMAT)
                        msg_length = len(message)
                        send_length = str(msg_length).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(message)
        except:
            connected = False
            CLIENTS.remove(conn)
            if nick:
                NICKS.remove(crrnt_nick)
                print(f"[DISCONNECT] {crrnt_nick} Disconnected")
                broadcast(f"[SERVER] {crrnt_nick} Disconnected")
                new_notification("Chatroom: Client Disconnect",
                                f"{crrnt_nick} Disconnected")
            else:
                print(f"[DISCONNECT] {addr} Disconnected")


def server_chat_and_commands():
    while True:
        servertext = input()
        broadcast(f"@[SERVER]: {servertext}")


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
