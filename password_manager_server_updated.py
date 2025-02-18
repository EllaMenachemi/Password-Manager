import socket
import pathlib
import os
import tldextract
import glob
import select


class Server:
    def __init__(self, host='0.0.0.0', port=8820, username_to_app = "", current_socket = socket.socket()):
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.current_socket = current_socket
        self.username_to_app = username_to_app
        self.read_list = []
        self.write_list = []
        self.x_list = []

    def listen_to_clients(self):
        self.server_socket.bind(('0.0.0.0', 8820))
        self.server_socket.listen()
        print("Server is up and running")
        open_client_sockets = []
        messages_to_send = []
        self.handle_clients(open_client_sockets, messages_to_send)

    def handle_clients(self, open_client_sockets, messages_to_send):
        while True:
            self.read_list, self.write_list, self.x_list = select.select([self.server_socket] + open_client_sockets,
                                                                         open_client_sockets, [])
            for current_socket in self.read_list:
                print("current socket: " + str(current_socket))
                self.current_socket = current_socket
                if current_socket is self.server_socket:
                    current_socket, client_address = current_socket.accept()
                    print("New client joined!", client_address)
                    open_client_sockets.append(current_socket)
                else:
                    data = self.receive_message(current_socket)
                    print("current socket again: " + str(self.current_socket))
                    self.current_socket = current_socket
                    print("data sent: " + data)
                    reply = self.check_client_message(data, open_client_sockets)
                    messages_to_send.append((current_socket, reply))

            for message in messages_to_send:
                current_socket, reply = message
                if current_socket in self.write_list:
                    length = str(len(reply))
                    z_fill_length = length.zfill(2)
                    message_to_send = z_fill_length + reply
                    print("message: " + message_to_send)
                    self.current_socket.send(message_to_send.encode())

                messages_to_send.remove(message)



    def accept_connection_to_client(self):
        (self.current_socket, client_address) = self.server_socket.accept()
        print("Client connected")
        self.receive_message()

    def receive_message(self, current_socket):
        length = current_socket.recv(2).decode()
        data = current_socket.recv(int(length)).decode()
        return data

    def send_client_message(self, reply):
        length = str(len(reply))
        z_fill_length = length.zfill(2)
        message = z_fill_length + reply
        print("message: " + message)
        self.current_socket.send(message.encode())



    def check_client_message(self, data, open_client_sockets):
        while data != "EXIT":
            print("data: " + data)
            if data[:17] == "username sign up:":
                reply = self.check_username_sign_up(data)
            elif data[:17] == "password sign up:":
                reply = self.check_password_sign_up(data)
            elif data[:16] == "username log in:":
                reply = self.check_username_and_password_log_in(data)
            elif data[:15] == "ADD check site:":
                reply = self.add_username_to_new_website(data)
            elif data[:19] == "ADD check password:":
                reply = self.add_password(data)
            elif data[:11] == "check site:":
                reply = self.check_if_site_exists(data)
            elif data[:22] == "UPDATE check password:":
                reply = self.add_password(data)
            return reply

        self.exit_program()
        return ""

            #self.handle_clients(open_client_sockets)



    def check_if_site_exists(self, data):
        j = 0
        while j != len(data):
            if data[j] == "(":
                break
            j += 1
        site_name = data[11:j]
        username_to_app = data[j+2:]
        print("site name: " + site_name)
        print("username to app: " + username_to_app)
        url = site_name
        extracted_info = tldextract.extract(url)
        site = site_name + ".txt"
        print("site " + site)
        file_path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + "\\" + site
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

        return reply

    def check_password_validity(self, password):
        is_valid = True
        small = False
        capital = False
        special_char = False
        for letter in password:
            if letter.islower():
                small = True
            elif letter.isupper():
                capital = True
            if not letter.isdigit() and not letter.isupper() and not letter.islower():
                special_char = True
        if small and capital and special_char == False:
            reply = "The password must contain at least one capital letter,\n one small letter and one special letter"
            is_valid = False
        if len(password) < 8:
            reply = "password not long enough"
            is_valid = False
        else:
            i = 0
            count = 0
            while i != len(password) -2:
                if password[i].isdigit() and password[i+1].isdigit():
                    if int(password[i]) == int(password[i+1]) + 1:
                        count = count + 1
                    elif int(password[i]) == int(password[i+1]) - 1:
                        count = count+1
                    else:
                        count = 0
                if count == 4:
                    reply = "The password contains illegal series of chars"
                    is_valid = False
                    break
                i = i + 1

                if "asdf" in password:
                    reply = "The password contains illegal series of chars"
                    is_valid = False
                if "qwerty" in password:
                    reply = "The password contains illegal series of chars"
                    is_valid = False


        if is_valid:
            reply = "password good"

        return reply, is_valid

    def check_username_sign_up(self, data):
        data = data[18:]
        self.username_to_app = data
        print("username:"+self.username_to_app)
        file_path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + data
        print("username  " + data)
        file = pathlib.Path(file_path)
        if file.exists():
            reply = "The username you entered is taken"
        else:
            reply = "username good"

            parent_dir = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager"
            path = os.path.join(parent_dir, data)
            os.mkdir(path)

        return reply

    def check_password_sign_up(self, data):
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

        return reply

    def check_username_and_password_log_in(self, data):
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

        return reply

    def add_username_to_new_website(self, data):
        username_to_app = self.username_to_app
        site_name = data[16:]
        print("site name:" + site_name)
        if site_name == "not valid":
            reply = "The website you entered is not valid"
        if site_name[0:4] == "http":
            is_url = True
        else:
            is_url = False

        if not is_url:
            print("website exists")
            path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app + site_name
            file = pathlib.Path(path)
            if file.exists():
                reply = "The website you entered is already saved in the system"
            else:
                file_name = site_name + ".txt"
                path = "C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" + username_to_app
                with open(os.path.join(path, file_name), 'w') as fp:
                    fp.write('Website: ' + site_name)
                    reply = "added"

        else:
            path_with_file_name = ("C:\\Users\\Ella Menachemi\\OneDrive\\Desktop\\password_manager\\" +
                                   username_to_app + "\\"
                                   + site_name + ".txt")
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
        return reply

    def add_password(self, data):
        if data[:3] == "ADD":
            add = True
            j = 0
            while j != len(data):
                if data[j] == "(":
                    break
                j += 1
            username_to_app = data[19:j]
            print("username to site: " + username_to_app)
            site_password = data[j+1:]
            print("site password: " + site_password)
        else:
            add = False
            j = 0
            while j != len(data):
                if data[j] == "(":
                    break
                j += 1
            site = data[22:j]
            print("site: " + site)
            i = 0
            while i != len(data):
                if data[i] == ")":
                    break
                i += 1
            username_to_app = data[j + 1:i]
            print("username to app: " + username_to_app)
            site_password = data[i + 2:]
            print("password: " + site_password)



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
        return reply

    def exit_program(self):
        self.current_socket.close()
        self.server_socket.close()


def main():
    password_manager_server = Server()
    password_manager_server.listen_to_clients()


if __name__ == "__main__":
    main()

