import socket
import threading
from os import system
from datetime import datetime

HEADER = 64
PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
VERSION = "Server"
DEVELOPER = "github.com/mattiastofte/"

clients = [] 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
system("title "+VERSION)

def handle_client(conn, addr):
    clients.append(conn)
    connected = True
    while connected: 
        message_length = conn.recv(HEADER).decode(FORMAT) # decode from bytes format to string using utf-8
        if message_length: # first message is empty (null), to tell that the client is connected, therefor you have to check if message_length has content. 
            message_length = int(message_length)
            message = conn.recv(message_length).decode(FORMAT) # blocking line of code, wont pass before we recieve message
            if message == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{get_time()}] [{addr[0]}] {message}")
            sendallclients((f"[{get_time()}] [#{addr[1]}] {message}").encode(FORMAT))
    clients.remove(conn)
    conn.close()

def sendallclients(message):
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT) # sends a string with length of message
    send_length += b' '*(HEADER-len(send_length))
    for client in clients:
        client.send(send_length)
        client.send(message)
def get_time():
    return datetime.now().strftime("%H:%M")
def start():
    server.listen()
    print(f"[Server] Listening on {SERVER}")
    while True:
        conn, addr = server.accept() # waits for new connection, stores object in conn and address in addr
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # new thread with function handle_client as target and conn object and addr as arguments
        thread.start() # starts new thread
        print(f"[Server] [{get_time()}] Client with id #{addr[1]} has connected to the server.")
        print(f"[Server] [{get_time()}] {threading.activeCount()-1} client(s) currently connected.")
print(f"simple-chat\nmade with love <3 by {DEVELOPER}")
print("━━━━━━━━━━━━━━━━━━━━━━━━\n")
print(f"\n[Server] Socket created succesfully. Starting server.")
start()


