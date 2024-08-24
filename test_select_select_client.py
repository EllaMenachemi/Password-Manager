import socket

def main():
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8820))
    while True:
        message = input("enter a name: ")
        my_socket.send(message.encode())
        if message =="":
            my_socket.close()
        input_of_server = my_socket.recv(int(1024)).decode()
        print("server sent: " + input_of_server)

if __name__ == "__main__":
    main()