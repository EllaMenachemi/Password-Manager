import tkinter as tk
from tkinter import Entry, Button, Label, font, Toplevel
import socket
class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Anti-Phishing Client")

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=14)

        self.client = Client()
        self.Start()

    def Start(self):
        master = self.master
        self.reset_screen()
        self.message_label = Label(master, text="Welcome to the ...........")
        self.message_label.pack()
        self.reset_button = tk.Button(master, text="SIGN IN",
        command=self.SIGN_IN)
        self.reset_button.pack(pady=10)
        self.reset_button = tk.Button(master, text="SIGN UP",
        command=self.SIGN_UP)
        self.reset_button.pack(pady=10)
        self.exit_button = Button(master, text="Exit",
        command=self.exit_application)
        self.exit_button.pack()
        self.received_message_label = Label(master, text="")
        self.received_message_label.pack()

    def reset_screen(self):
        # Destroy all widgets and recreate the main window
        for widget in self.master.winfo_children():
            widget.destroy()

    def SIGN_IN(self):
        self.reset_screen()

        self.entry_label = Label(self.master, text="Enter username and password")
        self.entry_label.pack()
        Label(self.master, text="Username:").pack()
        self.username_entry = Entry(self.master)
        self.username_entry.pack()
        Label(self.master, text="Password:").pack()
        self.password_entry = Entry(self.master, show="*")
        self.password_entry.pack()
        self.exit_button = Button(self.master, text="SIGN IN",
                                  command=self.CheckPassword)
        self.exit_button.pack()
        self.exit_button = Button(self.master, text="Exit",
                                  command=self.exit_application)
        self.exit_button.pack()
        self.received_message_label = Label(self.master, text="")
        self.received_message_label.pack()

    def CheckPassword(self):
        username = self.username_entry.get()

        password = self.password_entry.get()
        if username:
            if password:
                self.client.send_message("SIGN IN")
            self.client.send_message(username + "-")
            self.client.send_message(password)
            response = self.client.receive_message()
            if response == "VALID":
                self.AfterStart()
            if response == "USERNAME or PASSWORD incorrect":
                self.Incorrect()
            else:
                self.received_message_label.config(text="Please enter a username and password.")
        else:
            self.received_message_label.config(text="Please enter a username and password.")

    def Incorrect(self):
        self.reset_screen()
        self.entry_label = Label(self.master, text="USERNAME or PASSWORD incorrect")
        self.entry_label.pack()
        self.check_button = Button(self.master, text="TRY AGAIN",
                                       command=self.SIGN_IN)
        self.check_button.pack()
        self.exit_button = Button(self.master, text="Exit",
                                  command=self.exit_application)
        self.exit_button.pack()

    def SIGN_UP(self):
        self.reset_screen()

        self.entry_label = Label(self.master, text="Enter username and password you wish to have")
        self.entry_label.pack()
        Label(self.master, text="Username:").pack()
        self.username_entry = Entry(self.master)
        self.username_entry.pack()
        Label(self.master, text="Password:").pack()
        self.password_entry = Entry(self.master, show="*")
        self.password_entry.pack()
        self.exit_button = Button(self.master, text="SIGN UP",
                              command=self.SIGN_UP_SERVER)
        self.exit_button.pack()
        self.exit_button = Button(self.master, text="Exit",
                                  command=self.exit_application)
        self.exit_button.pack()
        self.received_message_label = Label(self.master, text="")
        self.received_message_label.pack()

class Client:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
    def receive_message(self):
        return self.client_socket.recv(1024).decode('utf-8')
    def send_message(self, message):
        self.client_socket.send(message.encode())
    def close_connection(self):
        self.client_socket.close()


class LoadingScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Loading...")
        self.geometry("200x100")
 # Add a label to display the loading GIF or text
        self.loading_label = Label(self, text="Loading...")
        self.loading_label.pack()
    def show_loading(self):
 # Make the loading screen visible
        self.transient(self.master)
        self.grab_set()
        self.update_idletasks()
    def destroy_loading(self):
 # Destroy the loading screen
        self.destroy()

def main():
 root = tk.Tk()
 root.attributes('-fullscreen', True)
 client_app = ClientApp(root)
 client_app.client.connect_to_server()
 root.protocol("WM_DELETE_WINDOW", client_app.exit_application)
 root.mainloop()
 client_app.client.close_connection()


if __name__ == "__main__":
 main()

