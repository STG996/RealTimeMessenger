import socket
import threading
import sys
import os

CLEAR = "clear" if os.name != "nt" else "cls"

HOST = socket.gethostname()
PORT = 5000
MAX_MSG_LEN = 2048

cursor_pos = 6

def recv_msgs(server: socket.socket):
    global cursor_pos
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

    server.send(username.encode())

    os.system(CLEAR)
    print("***********************")
    print("* Real Time Messenger *")
    print("*   (C) 2025 STG996   *")
    print("***********************\n")

    threading.Thread(target=send_msgs, args={server,}).start()
    threading.Thread(target=recv_msgs, args={server,}).start()


if __name__ == "__main__":
    main()
