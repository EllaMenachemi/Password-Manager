import socket
import random
import string


class Client:
    def __init__(self,  host='127.0.0.1', port=8820):
        self.host = host
        self.port = port
        self.my_socket = socket.socket()

    def connect_to_server(self):
        self.my_socket.connect(('127.0.0.1', 8820))
        print("the server is connected")

    def send_message_to_server(self, content_of_message):
        length = str(len(content_of_message))
        z_fill_length = length.zfill(2)
        message = z_fill_length + content_of_message
        print("message:" + message)
        self.my_socket.send(message.encode())
        print("message sent")

    def receive_message_from_server(self):
        length_message_server_sent = self.my_socket.recv(2).decode()
        input_of_server = self.my_socket.recv(int(length_message_server_sent)).decode()
        return input_of_server

    def close_connection(self):
        self.my_socket.close()

    def check_username_sign_up(self, username):
        description = "username sign up:"
        words = (description, username)
        username_final = " ".join(words)
        self.send_message_to_server(username_final)

        input_of_server = self.receive_message_from_server()

        print("server sent:" + input_of_server)

        return input_of_server

    def check_password_sign_up(self, password_and_verify):
        description_of_data = "password sign up:"
        description_and_data = (description_of_data, password_and_verify)
        final_message = " ".join(description_and_data)

        self.send_message_to_server(final_message)

        input_of_server = self.receive_message_from_server()

        return input_of_server

    def check_username_and_password_validity_log_in(self, username_and_password):
        description_of_data = "username log in:"
        description_and_data = (description_of_data, username_and_password)
        username_and_password = " ".join(description_and_data)

        self.send_message_to_server(username_and_password)

        input_of_server = self.receive_message_from_server()

        print("server sent:" + input_of_server)

        return input_of_server

    def check_site_add(self, site):
        description_of_data = "ADD check site:"
        description_and_data = (description_of_data, site)
        site_final = " ".join(description_and_data)

        self.send_message_to_server(site_final)

        input_of_server = self.receive_message_from_server()

        print("input of server: " + input_of_server)

        return input_of_server

    def check_password_site(self, password, add):
        if add:
            description_of_data = "ADD check password:"
        else:
            description_of_data = "UPDATE check password:"
        description_and_data = (description_of_data, password)
        site_final = " ".join(description_and_data)

        self.send_message_to_server(site_final)

        input_of_server = self.receive_message_from_server()

        return input_of_server

    def check_site_validity(self, site):
        description_of_data = "check site:"
        description_and_data = (description_of_data, site)
        site_final = " ".join(description_and_data)

        self.send_message_to_server(site_final)

        input_of_server = self.receive_message_from_server()

        print("input of server: " + input_of_server)

        return input_of_server

    def generate_password(self):
        password = ""
        random_char = random.choice(string.ascii_uppercase)
        password += random_char
        random_char = random.choice(string.ascii_lowercase)
        password += random_char
        for x in range(13):
            random_number = random.randint(0, 4)
            if random_number == 0:
                random_char = random.choice(string.ascii_uppercase)
            elif random_number == 1:
                random_char = random.choice(string.ascii_lowercase)
            elif random_number == 2:
                random_char = random.randint(0, 10)
            else:
                random_char = random.choice(string.punctuation)
            password += str(random_char)

        return password

    def exit_program(self):
        message = "EXIT"
        self.send_message_to_server(message)

        self.my_socket.close()
