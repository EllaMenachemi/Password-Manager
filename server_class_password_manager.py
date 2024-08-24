import socket
import pathlib
import os
import whois
import sys
from urllib.request import urlopen
from urllib.error import *
import tldextract
import glob


class Server:
    def __init__(self, host='0.0.0.0', port=8820, username_to_app=" ", site_name=" "):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.username_to_app = username_to_app
        self.site_name = site_name

    def listen_to_client(self):
        self.server_socket.bind(('0.0.0.0', 8820))
        self.server_socket.listen()
        print("Server is up and running")
        self.accept_connection_to_client()

    def accept_connection_to_client(self):
        (client_socket, client_address) = self.server_socket.accept()
        print("Client connected")
        self.receive_message(client_socket)

    def receive_message(self, client_socket):
        length = client_socket.recv(2).decode()
        data = client_socket.recv(int(length)).decode()
        self.check_client_message(data, client_socket)

    def check_client_message(self, data, client_socket):
        while data != "EXIT":
            if data[:17] == "username sign up:":
                self.check_username_sign_up(client_socket, data)
            elif data[:17] == "password sign up:":
                self.check_password_sign_up(client_socket, data)
            elif data[:16] == "username log in:":
                self.check_username_and_password_log_in(client_socket, data)
            elif data[:15] == "ADD check site:":
                self.add_username_to_new_website(client_socket, data)
            elif data[:19] == "ADD check password:":
                self.add_password(client_socket, data)
            elif data[:11] == "check site:":
                self.check_if_site_exists(client_socket, data)
            if data[:22] == "UPDATE check password:":
                self.add_password(client_socket, data)

            self.receive_message(client_socket)

        self.exit_program(client_socket)

    def send_client_message(self, client_socket, reply):
        length = str(len(reply))
        z_fill_length = length.zfill(2)
        message = z_fill_length + reply
        print("message: " + message)
        client_socket.send(message.encode())

    def check_if_site_exists(self, client_socket, data):
        #data = "check site:facebook"
        username_to_app = self.username_to_app
        site_name = data[12:]
        url = site_name
        self.site_name = site_name
        extracted_info = tldextract.extract(url)
        #site = extracted_info.domain + ".txt"
        site = site_name + ".txt"
        print("site " + site)
        file_path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + "\\" + site
        file = pathlib.Path(site)
        file = pathlib.Path(file_path)

        if not file.exists():
            reply = "The website you entered is not saved in the system"

        else:
            path = ("C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + "\\" + site)
            file = open(path, "r")
            content = file.readlines()
            password_line = content[1]
            password = password_line[10:]
            reply = "site in system" + password

        self.send_client_message(client_socket, reply)

    def check_password_validity(self, password):
        is_valid = True
        small = False
        capital = False
        if len(password) < 8:
            reply = "password not long enough"
            is_valid = False

        else:
            for letter in password:
                if letter.islower():
                    small = True
                if letter.isupper():
                    capital = True
            if not small or not capital:
                reply = "the password must contain at least one capital letter and one small letter"
                is_valid = False
            else:
                reply = "password good"

        return reply, is_valid

    def check_username_sign_up(self, client_socket, data):
        data = data[18:]
        self.username_to_app = data
        print("username:"+self.username_to_app)
        file_path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + data
        print("username  " + data)
        file = pathlib.Path(data)
        file = pathlib.Path(file_path)
        if file.exists():
            reply = "The username you entered is taken"
        else:
            reply = "username good"

            parent_dir = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager"
            path = os.path.join(parent_dir, data)
            os.mkdir(path)
            self.send_client_message(client_socket, reply)

    def check_password_sign_up(self, client_socket, data):
        username_to_app = self.username_to_app
        j = 0
        while j != len(data):
            if data[j] == "(":
                break
            j += 1
        password = data[18:j]
        i = 0
        while i != len(data):
            if data[i] == ")":
                break
            i += 1
        verify = data[i + 1:]
        is_valid = True
        #password = "Em123456789"
        #verify = "Em123456789"
        print("password: " + password)
        print("verify: " + verify)
        reply, is_valid = self.check_password_validity(password)

        if password != verify:
            reply = "password and your verify not the same"
            is_valid = False

        if is_valid:
            reply = "password good"

            path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app
            file_name = 'main password.txt'
            with open(os.path.join(path, file_name), 'w') as fp:
                fp.write('main password: ' + password)

        self.send_client_message(client_socket, reply)

    def check_username_and_password_log_in(self, client_socket, data):
        #data = "username log in:zvika1(verify:)Em123456789"
        j = 0
        while j != len(data):
            if data[j] == "(":
                break
            j += 1
        username = data[17:j]
        print("username" + username)
        i = 0
        while i != len(data):
            if data[i] == ")":
                break
            i += 1
        password = data[i + 1:]
        self.username_to_app = username
        print("username: " + username)
        print("password: " + password)

        file_path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username
        file = pathlib.Path(username)
        file = pathlib.Path(file_path)

        if not file.exists():
            reply = "username dont exist"

        else:
            path = ("C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username +
                    "\\" + "main password.txt")
            file = open(path, "r")
            content = file.read()
            real_password = content[15:]
            if real_password != password:
                reply = "wrong password"
            else:
                reply = "good"

        self.send_client_message(client_socket, reply)

    def add_username_to_new_website(self, client_socket, data):
        #data = "ADD check site:https://www.facebook.com/"
        username_to_app = self.username_to_app
        site_name = data[16:]
        print("site name:" + site_name)
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
                print("website does not exist")
                reply = "The website you entered is not valid"
            else:
                print("website exists")
                path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + site_name
                file = pathlib.Path(site_name)
                file = pathlib.Path(path)
                if file.exists():
                    reply = "The website you entered is already saved in teh system"
                else:
                    file_name = site_name + ".txt"
                    path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app
                    with open(os.path.join(path, file_name), 'w') as fp:
                        fp.write('Website: ' + site_name)
                        reply = "added"

        else:
            url = site_name
            extracted_info = tldextract.extract(url)
            site_name = extracted_info.domain
            try:
                html = urlopen(url)

            except HTTPError as e:
                print("HTTP error", e)
                reply = "The website you entered is not valid"

            except URLError as e:
                print("Opps ! Page not found!", e)
                reply = "The website you entered is not valid"

            else:
                print('Yeah !  found ')
                path_with_file_name = ("C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + "\\"
                                       + site_name + ".txt")
                file = pathlib.Path(site_name)
                file = pathlib.Path(path_with_file_name)
                if file.exists():
                    reply = "The website you entered is already saved in the system"

                else:
                    file_name = site_name + ".txt"
                    path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app
                    with open(os.path.join(path, file_name), 'w') as fp:
                        fp.write('Website: ' + site_name)
                        reply = "added"
        print("reply:" + reply)
        self.send_client_message(client_socket, reply)

    def add_password(self, client_socket, data):
        #data = "ADD check password:Em1702200717$"
        # data = "UPDATE check password:Em1702200717$@ella)facebook"
        username_to_app = self.username_to_app
        site = self.site_name
        if data[:3] == "ADD":
            add = True
            site_password = data[19:]
        else:
            add = False
            site_password = data[23:]
            print("password: " + site_password)
            print("site: " + site)
        reply, is_valid = self.check_password_validity(site_password)
        if is_valid:
            if add:
                path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + "\\*"
                list_of_files = glob.glob(path)
                latest_file = max(list_of_files, key=os.path.getctime)
                with open(os.path.join(path, latest_file), 'a') as fp:
                    fp.write('\npassword: ' + site_password)
                reply = "password added successfully"
            else:
                path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app
                file_name = site + ".txt"
                with open(os.path.join(path, file_name), 'r+') as fp:
                    content = fp.readlines()
                    current_password = content[1]
                    if current_password[10:] == site_password:
                        reply = "The password you entered is your current password"
                    else:
                        fp.seek(0)
                        for line in content:
                            if "password:" not in line:
                                fp.write(line)
                        fp.truncate()
                        with open(os.path.join(path, file_name), 'a') as fp:
                            fp.write('password: ' + site_password)
                        reply = "password added successfully"

        print("reply = " + reply)
        self.send_client_message(client_socket, reply)

    def exit_program(self, client_socket):
        client_socket.close()
        self.server_socket.close()


def main():
    password_manager_server = Server()
    password_manager_server.listen_to_client()

if __name__ == "__main__":
    main()

