from client2_password_manager import Client
import tkinter
from tkinter import *


class GuiClient:
    def __init__(self, master, client, username = ""):
        self.master = master
        self.client = Client()
        self.client.connect_to_server()
        self.username = username

    def create_window(self):
        window = Tk()
        window.geometry("500x500")
        frame = Frame(window, highlightbackground="pink", highlightthickness=15)
        frame.pack(side="top", expand=True, fill="both")
        self.greeting_page()
        window.mainloop()

    def clear_page(self):
        for widgets in self.master.winfo_children():
            widgets.destroy()

    def greeting_page(self):
        master = self.master
        self.clear_page()
        greeting = tkinter.Label(master, text="Welcome To The Password Manager", font=("italic", 16))
        greeting.place(y=50, x=50)
        sign_up_button = tkinter.Button(master, text="sign up", height=5, width=20,
                                        command=lambda button_pressed="sign up button Clicked":
                                        self.sign_up1())
        sign_up_button.place(x=150, y=150)
        log_in_button = tkinter.Button(master, text="log in", height=5, width=20,
                                       command=lambda button_pressed="log in button Clicked": self.log_in_page())
        log_in_button.place(x=150, y=300)

    def sign_up1(self):
        master = self.master
        self.clear_page()
        sign_up = tkinter.Label(master, text="Sign Up", font=("italic", 16))
        sign_up.place(x=100, y=10)
        enter_username_text = tkinter.Label(master, text="username", font=("italic", 11))
        enter_username_text.place(x=100, y=50)
        username_entry = tkinter.Entry(master)
        username_entry.place(x=100, y=100)
        check_username_text = tkinter.Button(master, text="check username validity",
                                             height=5, width=20, fg="white", bg="pink",
                                             command=lambda button_pressed="check username validity Clicked":
                                             self.check_button_pressed(button_pressed, username_entry, username_entry))
        check_username_text.place(x=100, y=200)
        back_button = tkinter.Button(
            master, text="back to home page", height=3, width=15,
            fg="white", bg="pink", command=lambda button_pressed="back to home page":
            self.greeting_page())
        back_button.place(x=250, y=350)

    def check_button_pressed(self, button_pressed, data1, data2):
        master = self.master
        get_data = data1.get()
        print("get data: " + get_data)
        if button_pressed == "check username validity Clicked":
            self.username = get_data
            message = self.client.check_username_sign_up(get_data)
            if message == "username good":
                self.sign_up_page2()
            else:
                message_on_screen = tkinter.Label(master,
                                                  text=message,
                                                  font=("italic", 12))
                message_on_screen.place(x=100, y=300)

        elif button_pressed == "Sign up button Clicked":
            get_data2 = data2.get()
            final_message = get_data + "(verify)" + get_data2
            message = self.client.check_password_sign_up(final_message)
            if message == "password good":
                self.action_page()
            else:
                message_on_screen = tkinter.Label(master, text=message)
                message_on_screen.place(x=50, y=400)

        elif button_pressed == "Log in button Clicked":
            get_data2 = data2.get()
            self.username = get_data
            final_message = get_data + "(password:)" + get_data2
            message = self.client.check_username_and_password_validity_log_in(final_message)
            if message == "good":
                self.action_page()
            else:
                message_on_screen = tkinter.Label(master, text=message)
                message_on_screen.place(x=100, y=320)

        elif button_pressed == "ADD check site Clicked":
            message = self.client.check_site_add(get_data)
            if message == "added":
                self.add_page2()
            else:
                message_on_screen = tkinter.Label(master, text=message)
                message_on_screen.place(x=100, y=350)

        elif button_pressed == "ADD check password":
            message = self.client.check_password_site(get_data, True)
            message_on_screen = tkinter.Label(master, text=message)
            message_on_screen.place(x=100, y=430)

        elif button_pressed == "GET check site":
            message = self.client.check_site_validity(get_data)
            if message == "The website you entered is not saved in the system":
                error = tkinter.Label(master, text=message)
                error.place(x=100, y=350)
            else:
                password = message[14:]
                self.get_page2(password)

        elif button_pressed == "UPDATE check site":
            message = self.client.check_site_validity(get_data)
            if message == "The website you entered is not saved in the system":
                error = tkinter.Label(master, text=message)
                error.place(x=100, y=350)
            else:
                self.update_page2()

        elif button_pressed == "UPDATE check password":

            message = self.client.check_password_site(get_data, False)
            message_on_screen = tkinter.Label(master, text=message)
            message_on_screen.place(x=100, y=430)
        elif button_pressed == "Generate password":
            password = self.client.generate_password()
            message_on_screen = tkinter.Label(master, text="The generated password for this website is:")
            message_on_screen.place(x=100, y=270)
            show_password = tkinter.Label(master, text=password)
            show_password.place(x=100, y=295)
            copy_generated_password = tkinter.Button(master, text="Copy generated password", fg="white", bg="pink",
                                                     command=lambda button_pressed_now="copy generated password":
                                                     self.copy_password(password))
            copy_generated_password.place(x=250, y=290)


        else:
            self.client.exit_program()
            self.greeting_page()

        return button_pressed

    def sign_up_page2(self):
        master = self.master
        self.clear_page()
        sign_up = tkinter.Label(master, text="Sign Up", font=("italic", 16))
        sign_up.place(x=100, y=10)
        enter_password_text = tkinter.Label(master, text="password")
        enter_password_text.place(x=100, y=50)
        password = tkinter.Entry(master, show="*")
        password.place(x=100, y=100)
        verify_password = tkinter.Label(master, text="verify password")
        verify_password.place(x=100, y=150)
        verify = tkinter.Entry(master, show="*")
        verify.place(x=100, y=200)
        sign_up_button = tkinter.Button(master, text="sign up",
                                        height=5, width=20, fg="white", bg="pink",
                                        command=lambda button_pressed="Sign up button Clicked":
                                        self.check_button_pressed(button_pressed, password, verify))
        sign_up_button.place(x=100, y=300)

    def log_in_page(self):
        master = self.master
        self.clear_page()
        log_in = tkinter.Label(master, text="Log In", font=("italic", 16))
        log_in.place(x=100, y=10)
        enter_username_text = tkinter.Label(master, text="Enter Your Username")
        enter_username_text.place(x=100, y=50)
        username = tkinter.Entry(master)
        username.place(x=100, y=100)
        enter_password_text = tkinter.Label(master, text="Enter Your Password")
        enter_password_text.place(x=100, y=200)
        password = tkinter.Entry(master, show="*")
        password.place(x=100, y=250)
        log_in_button = tkinter.Button(master, text="log in", height=5, width=20, fg="white", bg="pink",
                                       command=lambda button_pressed="Log in button Clicked":
                                       self.check_button_pressed(button_pressed, username, password))
        log_in_button.place(x=100, y=350)
        back_button = tkinter.Button(
            master, text="back to home page", height=3, width=15, fg="white", bg="pink",
            command=lambda button_pressed="back to home page":
            self.greeting_page()
        )
        back_button.place(x=325, y=375)

    def action_page(self):
        master = self.master
        self.clear_page()
        opening = tkinter.Label(master, text="Choose An Action:", font=("italic", 16))
        opening.place(x=50, y=25)
        add_description = tkinter.Label(master, text="Add- Add a new password")
        add_description.place(x=50, y=75)
        get_description = tkinter.Label(master, text="Get- Retrieve an existing password")
        get_description.place(x=50, y=100)
        update_description = tkinter.Label(master, text="Update - Update the password for a site")
        update_description.place(x=50, y=125)
        add_button = tkinter.Button(master, text="ADD", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="ADD":
                                    self.add_page1())
        add_button.place(x=100, y=175)
        get_button = tkinter.Button(master, text="GET", height=3, width=15, fg="white", bg="light blue",
                                    command=lambda button_pressed="ADD":
                                    self.get_page1()
                                    )
        get_button.place(x=100, y=250)
        update_button = tkinter.Button(master, text="UPDATE", height=3, width=15, fg="white", bg="magenta",
                                       command=lambda button_pressed="ADD":
                                       self.update_page1())
        update_button.place(x=100, y=325)
        exit_button = tkinter.Button(master, text="EXIT", height=3, width=15, fg="white", bg="red",
                                     command=lambda button_pressed="EXIT":
                                     self.exit_page())
        exit_button.place(x=100, y=400)

    def add_page1(self):
        self.clear_page()
        master = self.master
        header1 = tkinter.Label(master, text="Add Page", font=("italic", 16))
        header1.place(x=100, y=25)
        header2 = tkinter.Label(master, text="Add a new website to your password manager")
        header2.place(x=50, y=55)
        instruction = tkinter.Label(master, text="Enter site name or URL")
        instruction.place(x=100, y=100)
        site_name = tkinter.Entry(master)
        site_name.place(x=100, y=130)
        check_site = tkinter.Button(master, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="ADD check site Clicked":
                                    self.check_button_pressed(button_pressed, site_name, site_name))
        check_site.place(x=100, y=200)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="Back to action page":
                                             self.action_page())
        back_to_action_page.place(x=100, y=270)

    def add_page2(self):
        master = self.master
        self.clear_page()
        instruction = tkinter.Label(master, text="Enter password for site:", font=("italic", 16))
        instruction.place(x=100, y=25)
        password = tkinter.Entry(master)
        password.place(x=100, y=75)
        check_password = tkinter.Button(master, text="check password", height=3, width=15, fg="white", bg="pink",
                                        command=lambda button_pressed="ADD check password":
                                        self.check_button_pressed(button_pressed, password, password))
        check_password.place(x=100, y=120)
        generate_password = tkinter.Button(master, text="Generate password",height=3, width=15, fg="white", bg="pink",
                                        command=lambda button_pressed="Generate password":
                                        self.check_button_pressed(button_pressed, password, password) )
        generate_password.place(x=100, y=190)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="Back to action page":
                                             self.action_page())
        back_to_action_page.place(x=100, y=340)

    def get_page1(self):
        self.clear_page()
        master = self.master
        header1 = tkinter.Label(master, text="Get Page", font=("italic", 16))
        header1.place(x=100, y=25)
        header2 = tkinter.Label(master, text="Get password to a chosen website")
        header2.place(x=50, y=55)
        instruction = tkinter.Label(master, text="Enter site name or URL")
        instruction.place(x=100, y=100)
        site_name = tkinter.Entry(master)
        site_name.place(x=100, y=130)
        check_site = tkinter.Button(master, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="GET check site":
                                    self.check_button_pressed(button_pressed, site_name, site_name))
        check_site.place(x=100, y=200)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="Back to action page":
                                             self.action_page())
        back_to_action_page.place(x=100, y=270)

    def get_page2(self, password):
        self.clear_page()
        master = self.master
        message = tkinter.Label(master, text="Your password for this website is:", font=("italic", 16))
        message.place(x=75, y=25)
        encoded_password = ""
        for letter in password:
            encoded_password += "* "

        show_encoded_password = tkinter.Label(master, text=encoded_password)
        show_encoded_password.place(x=150, y=75)
        show_password_button = tkinter.Button(master, text="Show Password", height=3, width=15, fg="white", bg="pink",
                                              command=lambda button_pressed="show password":
                                              self.show_password(password, show_encoded_password))
        show_password_button.place(x=150, y=125)
        copy_password_button = tkinter.Button(master, text="copy password", height=3, width=15, fg="white", bg="pink",
                                              command=lambda button_pressed="copy password":
                                              self.copy_password(password))
        copy_password_button.place(x=150, y=185)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="ADD check site":
                                             self.action_page())
        back_to_action_page.place(x=150, y=245)

    def show_password(self, password, show_encoded_password):
        master = self.master
        show_encoded_password.destroy()
        show_password_on_screen = tkinter.Label(master, text=password)
        show_password_on_screen.place(x=150, y=75)

    def copy_password(self, password):
        master = self.master
        master.clipboard_clear()
        master.clipboard_append(password.rstrip())
        success_message = tkinter.Label(master, text="password is copied to keyboard")
        success_message.place(x=150, y=400)

    def update_page1(self):
        self.clear_page()
        master = self.master
        header1 = tkinter.Label(master, text="Update Page", font=("italic", 16))
        header1.place(x=100, y=25)
        header2 = tkinter.Label(master, text="Update password to a chosen website")
        header2.place(x=50, y=55)
        instruction = tkinter.Label(master, text="Enter site name or URL")
        instruction.place(x=100, y=100)
        site_name = tkinter.Entry(master)
        site_name.place(x=100, y=130)
        check_site = tkinter.Button(master, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="UPDATE check site":
                                    self.check_button_pressed(button_pressed, site_name, site_name))
        check_site.place(x=100, y=200)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="Back to action page":
                                             self.action_page())
        back_to_action_page.place(x=100, y=270)

    def update_page2(self):
        self.clear_page()
        master = self.master
        instruction = tkinter.Label(master, text="Your new password:", font=("italic", 16))
        instruction.place(x=100, y=25)
        password = tkinter.Entry(master)
        password.place(x=100, y=75)
        check_password = tkinter.Button(master, text="check password", height=3, width=15, fg="white", bg="pink",
                                        command=lambda button_pressed="UPDATE check password":
                                        self.check_button_pressed(button_pressed, password, password))
        check_password.place(x=100, y=120)
        generate_password = tkinter.Button(master, text="Generate password",height=3, width=15, fg="white", bg="pink",
                                        command=lambda button_pressed="Generate password":
                                        self.check_button_pressed(button_pressed, password, password) )
        generate_password.place(x=100, y=190)
        back_to_action_page = tkinter.Button(master, text="Back to action page", height=3, width=15, fg="white",
                                             bg="pink",
                                             command=lambda button_pressed="Back to action page":
                                             self.action_page())
        back_to_action_page.place(x=100, y=340)

    def exit_page(self):
        self.clear_page()
        master = self.master
        message = tkinter.Label(master, text="Are you sure you want to exit the program?", font=("italic", 16))
        message.place(x=25, y=25)

        entry = tkinter.Entry(master)

        yes_button = tkinter.Button(master, text="yes", height=3, width=15, fg="white", bg="red",
                                    command=lambda button_pressed="EXIT":
                                    self.check_button_pressed(button_pressed, entry, entry))
        yes_button.place(x=100, y=100)
        no_button = tkinter.Button(master, text="no", height=3, width=15, fg="white", bg="green",
                                   command=lambda button_pressed="EXIT":
                                   self.action_page())
        no_button.place(x=250, y=100)
