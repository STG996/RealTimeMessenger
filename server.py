import socket
import threading

HOST = socket.gethostname()
PORT = 5000
LISTEN_LIMIT = 5
MAX_MSG_LEN = 2048
MODULO = 4289372549372 # Random number

connections = {}

def manage_conn(conn: socket.socket):
    handle_conn(conn)
    main_loop(conn)

def handle_conn(conn: socket.socket):
    username = conn.recv(MAX_MSG_LEN).decode()
    connections[conn] = username
    print(username)

    # Diffie-Hellman key exchange
    for starting_client_index in range(len(connections)):
        contribution = 2

        list(connections)[starting_client_index].send("NEW JOIN".encode()) # -> dict converted to list to allow indexing
        list(connections)[starting_client_index].send(username.encode())
        list(connections)[starting_client_index].send(str(MODULO).encode())

        for i in range(starting_client_index+1, len(connections)): # Begin revolution about circle of clients
            list(connections)[i].send(str(contribution).encode())
            contribution = list(connections)[i].recv(MAX_MSG_LEN).decode()
        for j in range(0, starting_client_index): # Complete revolution about circle of clients
            list(connections)[j].send(str(contribution).encode())
            contribution = list(connections)[j].recv(MAX_MSG_LEN).decode()

        list(connections)[starting_client_index].send("UPCOMING FINAL".encode())
        list(connections)[starting_client_index].send(str(contribution).encode())

def main_loop(conn: socket.socket):
    while True:
        message = conn.recv(MAX_MSG_LEN).decode()
        for client in connections:
            client.send(f"\033[31m[{connections[conn]}]~\033[m {message}".encode())

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
