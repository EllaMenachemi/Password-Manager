from client2_password_manager import Client
from client_gui_password_manager import GuiClient
from tkinter import *


def main():
    window = Tk()
    window.geometry("500x500")
    frame = Frame(window, highlightbackground="pink", highlightthickness=15)
    frame.pack(side="top", expand=True, fill="both")
    logic_client = Client()
    password_manager_client_gui = GuiClient(frame,logic_client)

    password_manager_client = Client()

    #password_manager_client.connect_to_server()
    password_manager_client_gui.greeting_page()
    window.mainloop()

if __name__ == "__main__":
    main()

#class Manager:
#    @staticmethod
#    def main():
#        client_gui_password_manager.Gui_Client.greeting_page()

