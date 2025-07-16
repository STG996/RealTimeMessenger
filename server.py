import socket
import threading
from client import process_recvd, process_to_send

HOST = socket.gethostname()
PORT = 5000
LISTEN_LIMIT = 5
MAX_MSG_LEN = 4096
MODULO = 4289372549372  # Random number

connections = {}


def manage_conn(conn: socket.socket) -> None:
    handle_conn(conn)
    main_loop(conn)


def handle_conn(conn: socket.socket) -> None:
    username = conn.recv(MAX_MSG_LEN).decode()
    connections[conn] = username
    print(username)

    # Diffie-Hellman key exchange
    for starting_client_index in range(len(connections)):
        contribution = 2
        confirmation_recvd = False

        while not confirmation_recvd:
            list(connections)[starting_client_index].send(
                process_to_send("NEW JOIN").encode())  #-> dict converted to list to allow indexing
            list(connections)[starting_client_index].send(process_to_send(username).encode())
            list(connections)[starting_client_index].send(process_to_send(MODULO).encode())
            recvd = process_recvd(list(connections)[starting_client_index].recv(MAX_MSG_LEN).decode())[0]
            if recvd == "RECEIVED SUCCESSFULLY":
                confirmation_recvd = True

        for i in range(starting_client_index + 1, len(connections)):  # Begin revolution about circle of clients
            list(connections)[i].send(process_to_send(str(contribution)).encode())
            contribution = process_recvd(list(connections)[i].recv(MAX_MSG_LEN).decode())[0]
        for j in range(0, starting_client_index):  # Complete revolution about circle of clients
            list(connections)[j].send(process_to_send(str(contribution)).encode())
            contribution = process_recvd(list(connections)[j].recv(MAX_MSG_LEN).decode())[0]

        list(connections)[starting_client_index].send(process_to_send("UPCOMING FINAL").encode())
        list(connections)[starting_client_index].send(process_to_send(contribution).encode())


def main_loop(conn: socket.socket) -> None:
    while True:
        message = conn.recv(MAX_MSG_LEN).decode()
        for client in connections:
            client.send(process_to_send(f"\033[31m[{connections[conn]}]~\033[m {message}").encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    # Make connections and usernames
    server.listen(LISTEN_LIMIT)
    while True:
        conn, addr = server.accept()
        print(f"{addr[0]}:{addr[1]} connected")

        threading.Thread(target=manage_conn, args=(conn,)).start()


if __name__ == "__main__":
    main()
