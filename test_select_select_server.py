import socket
import select


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    MAX_MSG_LENGTH = 1024
    SERVER_PORT = 8820
    SERVER_IP = "0.0.0.0"
    server_socket = socket.socket()
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    open_client_sockets = []
    messages_to_send = []
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                open_client_sockets.append(connection)
                print_client_sockets(open_client_sockets)
            else:
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Connection closed", )
                    open_client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(open_client_sockets)
                else:
                    messages_to_send.append((current_socket, data))
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                current_socket.send(data.encode())
            messages_to_send.remove(message)


if __name__ == "__main__":
    main()