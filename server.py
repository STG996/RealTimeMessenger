import socket
import threading

HOST = socket.gethostname()
PORT = 5000
LISTEN_LIMIT = 5
MAX_MSG_LEN = 2048

usernames = {}

def handle_conn(conn: socket.socket):
    username = conn.recv(MAX_MSG_LEN).decode()
    usernames[conn] = username
    print(username)

    while True:
        message = conn.recv(MAX_MSG_LEN).decode()
        for client in usernames:
            client.send(f"\x1b[31m[{usernames[conn]}]~\x1b[m {message}".encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    # Make connections and usernames
    server.listen(LISTEN_LIMIT)
    while True:
        conn, addr = server.accept()
        print(f"{addr[0]}:{addr[1]} connected")

        threading.Thread(target=handle_conn, args=(conn,)).start()


if __name__ == "__main__":
    main()
