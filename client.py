import socket
import threading
import sys

HOST = socket.gethostname()
PORT = 5000
MAX_MSG_LEN = 2048

def recv_msgs(server: socket.socket):
    while True:
        message = server.recv(MAX_MSG_LEN).decode()
        sys.stdout.write("\x1b[u")
        print(message)
        sys.stdout.write("\x1b[s")


def send_msgs(server: socket.socket):
    while True:
        sys.stdout.write("\x1b[6;3H\x1b[K")
        message = sys.stdin.readline()
        server.send(message.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    username = ""
    while username == "" or len(username) > MAX_MSG_LEN:
        username = input("Enter username: ")

    server.send(username.encode())

    sys.stdout.write("\x1b[2J\x1b[H")
    print("***********************")
    print("* Real Time Messenger *")
    print("*   (C) 2025 STG996   *")
    print("***********************\n")
    print("> ")
    print("\n\n")
    sys.stdout.write("\x1b[s")

    threading.Thread(target=send_msgs, args={server,}).start()
    threading.Thread(target=recv_msgs, args={server,}).start()


if __name__ == "__main__":
    main()
