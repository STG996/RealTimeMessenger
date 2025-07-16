import socket
import threading
import sys
import os
from random import randint

CLEAR = "clear" if os.name != "nt" else "cls"

HOST = socket.gethostname()
PORT = 5000
MAX_MSG_LEN = 4096
DELIMITER = "\t"

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

def process_recvd(recvd):
    messages = []
    started = False
    for character in recvd:
        if character == DELIMITER and not started:
            started = True
            messages.append("")
        elif character == DELIMITER and started:
            started = False
        else:
            messages[-1] += character

    return messages

def process_to_send(to_send):
    return f"{DELIMITER}{to_send}{DELIMITER}"

def handle_new_join(server: socket.socket, client: Client, username: str, n: int):
    # username = server.recv(MAX_MSG_LEN).decode()
    print(f"\033[31m{username}\033[m has joined.")

    # Diffie-Hellman key exchange
    # n = int(server.recv(MAX_MSG_LEN).decode())
    final = False
    while not final:
        recvd = process_recvd(server.recv(MAX_MSG_LEN).decode())
        if recvd[0] == "UPCOMING FINAL": # ERROR: UPCOMING FINAL NOT FIRST ELEMENT OF LIST
            final = True
        else:
            server.send(process_to_send(client.contribute(int(recvd[0]), n)).encode())
    client.set_shared_key(recvd[1], n)

def recv_msgs(server: socket.socket, client: Client):
    cursor_pos = 6
    while True:
        #message = server.recv(MAX_MSG_LEN).decode()
        messages = process_recvd(server.recv(MAX_MSG_LEN).decode())

        sys.stdout.write(f"\033[{cursor_pos};0H")  # Moves cursor back to last position
        if messages[0] == "NEW JOIN":
            handle_new_join(server, client, messages[1], int(messages[2]))
            server.send(process_to_send("RECEIVED SUCCESSFULLY").encode())
        else:
            print(messages[0])
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

    os.system(CLEAR)
    print("***********************")
    print("* Real Time Messenger *")
    print("*   (C) 2025 STG996   *")
    print("***********************\n")

    threading.Thread(target=send_msgs, args=(server,)).start()
    threading.Thread(target=recv_msgs, args=(server, client,)).start()


if __name__ == "__main__":
    main()
