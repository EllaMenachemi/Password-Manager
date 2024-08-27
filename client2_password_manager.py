import socket
import random
import string
import hashlib
import whois
import sys
from urllib.request import urlopen
from urllib.error import *
import tldextract

class Client:
    def __init__(self,  host='127.0.0.1', port=8820, username_to_app="", site_name=""):
        self.host = host
        self.port = port
        self.my_socket = socket.socket()
        self.username_to_app = username_to_app
        self.site_name = site_name

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
        self.username_to_app = username
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
        j = 0
        while j != len(username_and_password):
            if username_and_password[j] == "(":
                break
            j += 1
        self.username_to_app = username_and_password[17:j]

        self.send_message_to_server(username_and_password)

        input_of_server = self.receive_message_from_server()

        print("server sent:" + input_of_server)
        print("hi")

        return input_of_server

    def check_site_add(self, site):
        is_website_valid = self.check_if_site_exists(site)
        if not is_website_valid:
            self.send_message_to_server(("ADD check site:not valid"))
        else:
            hashed_site = hashlib.sha1(site.encode()).hexdigest()
            description_of_data = "ADD check site:"
            description_and_data = (description_of_data, str(hashed_site))
            site_final = " ".join(description_and_data)

            self.send_message_to_server(site_final)

        input_of_server = self.receive_message_from_server()

        print("input of server: " + input_of_server)

        return input_of_server

    def check_if_site_exists(self, site_name):
        is_website_valid = True
        if site_name[0:4] == "http":
            is_url = True
        else:
            is_url = False

        if not is_url:
            try:
                domain = whois.whois(site_name)
                if domain.domain_name == None:
                    sys.exit(0)
            except:
               is_website_valid = False
            else:
                is_website_valid = True

        else:
            url = site_name
            extracted_info = tldextract.extract(url)
            site_name = extracted_info.domain
            try:
                html = urlopen(url)

            except HTTPError as e:
                is_website_valid = False

            except URLError as e:
                is_website_valid = False
            else:
                is_website_valid = True

        return is_website_valid

    def check_password_site(self, password, add):
        if add:
            description_of_data = "ADD check password:" + self.username_to_app + "("
        else:
            description_of_data = "UPDATE check password:" + self.site_name + "(" + self.username_to_app + ")"
        description_and_data = (description_of_data, password)
        site_final = " ".join(description_and_data)

        self.send_message_to_server(site_final)

        input_of_server = self.receive_message_from_server()
        print("input of server- update password:" + input_of_server)
        return input_of_server

    def check_site_validity(self, site):
        hashed_site = hashlib.sha1(site.encode()).hexdigest()

        description_of_data = "check site:" + str(hashed_site) + "("
        description_and_data = (description_of_data, self.username_to_app)
        site_final = " ".join(description_and_data)

        self.site_name = hashed_site
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
            random_number = random.randint(0,4)
            if random_number == 0:
                random_char = random.choice(string.ascii_uppercase)
            elif random_number == 1:
                random_char = random.choice(string.ascii_lowercase)
            elif random_number == 2:
                random_char = random.randint(0,10)
            else:
                random_char = random.choice(string.punctuation)
            password += str(random_char)

        return password



    def exit_program(self):
        message = "EXIT"
        self.send_message_to_server(message)

        self.my_socket.close()
