import socket
import threading

HEADER = 64
PORT = 65432
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    connected = True
    while connected:
        message_length = conn.recv(HEADER).decode(FORMAT) # decode from bytes format to string using utf-8
        message_length = int(message_length)
        message = conn.recv(message_length).decode(FORMAT) # blocking line of code, wont pass before we recieve message
        if message == DISCONNECT_MESSAGE:
            connected = False
        print(f"[{addr}] {message}")
    
    conn.close()

def start():
    server.listen()
    print(f"[Server] Listening on {SERVER}")
    while True:
        conn, addr = server.accept() # waits for new connection, stores object in conn and address in addr
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # new thread with function handle_client as target and conn object and addr as arguments
        thread.start() # starts new thread
        print("[Server]",addr,"has connected to the server.",threading.activeCount()-1,"clients are currently connected.")

print("[Server] Socket created succesfully. Starting server.")
start()

