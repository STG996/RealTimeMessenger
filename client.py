import socket
import threading
import sys
import os
from random import randint

CLEAR = "clear" if os.name != "nt" else "cls"

HOST = socket.gethostname()
PORT = 5000
MAX_MSG_LEN = 2048

class Client:
    def __init__(self):
        self.__private_key = randint(1000000, 9999999)
        self.__shared_key = None

    def contribute(self, g, n):
        result = (g ** self.__private_key) % n
        return result

    def set_shared_key(self, g, n):
        self.__shared_key = self.contribute(g, n)

    def encrypt_msg(self, msg):
        pass

    def decrypt_msg(self, msg):
        pass

def recv_msgs(server: socket.socket):
    cursor_pos = 6
    while True:
        message = server.recv(MAX_MSG_LEN).decode()
        sys.stdout.write(f"\033[{cursor_pos};0H")  # Moves cursor back to last position
        print(message)
        cursor_pos += 1

def send_msgs(server: socket.socket):
    while True:
        message = input()
        server.send(message.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    username = ""
    while username == "" or len(username) > MAX_MSG_LEN:
        username = input("Enter username: ")

    # Initialise client object and send username
    client = Client()
    server.send(username.encode())

    # Diffie-Hellman key exchange
    n = int(server.recv(MAX_MSG_LEN).decode())
    final = False
    while not final:
        recvd = server.recv(MAX_MSG_LEN).decode()
        if recvd == "UPCOMING FINAL":
            final = True
        else:
            server.send(client.contribute(int(recvd), n))
    recvd = int(server.recv(MAX_MSG_LEN).decode())
    client.set_shared_key(recvd, n)

    os.system(CLEAR)
    print("***********************")
    print("* Real Time Messenger *")
    print("*   (C) 2025 STG996   *")
    print("***********************\n")

    threading.Thread(target=send_msgs, args={server,}).start()
    threading.Thread(target=recv_msgs, args={server,}).start()


if __name__ == "__main__":
    main()
