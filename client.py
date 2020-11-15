import socket
import threading
import time
from os import system
import sys

HEADER = 64
PORT = 65432
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "46.9.226.154"
ADDR = (SERVER, PORT)
VERSION = "Client"
DEVELOPER = "github.com/mattiastofte/"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
system("title "+VERSION)

def send(message):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    message = message.encode(FORMAT) # encodes to utf-8
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT) # sends a string with length of message
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    print("[Client] Initializing receive thread.\n")
    while True:
        message_length = client.recv(HEADER).decode(FORMAT) # decode from bytes format to string using utf-8
        if message_length: # first message is empty (null), to tell that the client is connected, therefor you have to check if message_length has content. 
            message_length = int(message_length)
            message = client.recv(message_length).decode(FORMAT)
            print(f"\r{message}")

def start():
    print(f"\n[Client] Succesfully connected to server.")
    x = threading.Thread(target=receive, args=())
    x.start()
    while True:
        send(input(""))

print(f"simple-chat\nmade with love <3 by {DEVELOPER}\n")
print("━━━━━━━━━━━━━━━━━━━━━━━━\n")
start()
    