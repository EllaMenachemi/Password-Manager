import socket
import tkinter
from tkinter import *


def main():
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8820))
    create_window(my_socket)


def create_window(my_socket):
    window = Tk()
    window.geometry("500x500")
    frame = Frame(window, highlightbackground="pink", highlightthickness=15)
    frame.pack(side="top", expand=True, fill="both")
    greeting_page(frame, my_socket)
    window.mainloop()


def greeting_page(frame, my_socket):
    clear_page(frame)
    greeting_text = tkinter.Label(frame, text="Welcome To The Password Manager", font=("italic", 16))
    greeting_text.place(y=50, x=50)
    sign_up_button = tkinter.Button(frame, text="sign up", height=5, width=20,
                                    command=lambda button_pressed="sign up button Clicked":
                                    sign_up_page1(frame, my_socket))
    sign_up_button.place(x=150, y=150)
    log_in_button = tkinter.Button(frame, text="log in", height=5, width=20,
                                   command=lambda button_pressed="log in button Clicked":
                                   log_in_page(frame, my_socket))
    log_in_button.place(x=150, y=300)


def send_to_server(my_socket, content_of_message):
    length = str(len(content_of_message))
    z_fill_length = length.zfill(2)
    message = z_fill_length + content_of_message
    print("message:" + message)
    my_socket.send(message.encode())


def sign_up_page1(frame, my_socket):
    sign_up_text = tkinter.Label(frame, text="Sign Up", font=("italic", 16))
    sign_up_text.place(x=100, y=10)
    enter_username_text = tkinter.Label(frame, text="username", font=("italic", 11))
    enter_username_text.place(x=100, y=50)
    username_entry = tkinter.Entry(frame)
    username_entry.place(x=100, y=100)
    get_username = username_entry.get()
    print("get username:" + username_entry.get())
    check_username_text = tkinter.Button(frame, text="check username validity",
                                         height=5, width=20, fg="white", bg="pink",
                                         command=lambda button_pressed="check username validity Clicked":
                                         check_username_sign_up(get_username, frame, my_socket))
    check_username_text.place(x=100, y=200)
    back_to_homepage_button = tkinter.Button(
        frame, text="back to home page", height=3, width=15,
        fg="white", bg="pink", command=lambda button_pressed="back to home page":
        greeting_page(frame, my_socket)
    )
    back_to_homepage_button.place(x=250, y=350)


def check_username_sign_up(username, frame, my_socket):
    description_of_data = "username sign up:"
    description_and_data = (description_of_data, username)
    final_message = " ".join(description_and_data)
    send_to_server(my_socket, final_message)
    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()
    print("server sent:" + input_of_server)
    if input_of_server == "username not good":
        username_not_good = tkinter.Label(frame,
                                          text="The username you wrote is already taken",
                                          font=("italic", 12))
        username_not_good.place(x=100, y=300)
    else:
        sign_up_page2(frame, my_socket)


def sign_up_page2(frame, my_socket):
    clear_page(frame)
    sign_up_text = tkinter.Label(frame, text="Sign Up", font=("italic", 16))
    sign_up_text.place(x=100, y=10)
    enter_password_text = tkinter.Label(frame, text="password")
    enter_password_text.place(x=100, y=50)
    password = tkinter.Entry(frame)
    password.place(x=100, y=100)
    get_password = password.get()
    verify_password = tkinter.Label(frame, text="verify password")
    verify_password.place(x=100, y=150)
    verify = tkinter.Entry(frame)
    verify.place(x=100, y=200)
    get_verify = verify.get()
    sign_up_button = tkinter.Button(frame, text="sign up", height=5, width=20, fg="white", bg="pink",
                                    command=lambda button_pressed="sign up":
                                    check_password_sign_up(frame, get_password, get_verify, my_socket))
    sign_up_button.place(x=100, y=300)


def check_password_sign_up(frame, get_password, verify, my_socket):
    description_of_data = "password sign up:"
    get_password += "(verify:)" + verify
    description_and_data = (description_of_data, get_password)
    final_message = " ".join(description_and_data)
    send_to_server(my_socket, final_message)
    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()

    if input_of_server == "error 1":
        error = tkinter.Label(frame, text="password not long enough")
        error.place(x=100, y=400)
    elif input_of_server == "error 2":
        error = tkinter.Label(frame, text="password and your verify not the same")
        error.place(x=100, y=400)
    elif input_of_server == "error 3":
        error = tkinter.Label(
            frame, text="the password must contain at least one capital letter and one small letter")
        error.place(x=50, y=400)
    else:
        action_page(frame, my_socket)


def log_in_page(frame, my_socket):
    log_in_text = tkinter.Label(frame, text="Log In", font=("italic", 16))
    log_in_text.place(x=100, y=10)
    enter_username_text = tkinter.Label(frame, text="Enter Your Username")
    enter_username_text.place(x=100, y=50)
    username = tkinter.Entry(frame)
    username.place(x=100, y=100)
    get_username = username.get()
    enter_password_text = tkinter.Label(frame, text="Enter Your Password")
    enter_password_text.place(x=100, y=200)
    password = tkinter.Entry(frame)
    password.place(x=100, y=250)
    get_password = password.get()
    log_in_button = tkinter.Button(frame, text="log in", height=5, width=20, fg="white", bg="pink",
                                   command=lambda button_pressed="log in":
                                   check_username_and_password_validity_log_in(frame,
                                                                               get_username, get_password,  my_socket))
    log_in_button.place(x=100, y=350)
    back_to_homepage_button = tkinter.Button(
        frame, text="back to home page", height=3, width=15, fg="white", bg="pink",
        command=lambda button_pressed="back to home page":
        greeting_page(frame, my_socket)
    )
    back_to_homepage_button.place(x=325, y=375)


def check_username_and_password_validity_log_in(frame, username, password, my_socket):
    description_of_data = "username log in:"
    username += "(password:)" + password
    description_and_data = (description_of_data, username)
    username_and_password = " ".join(description_and_data)

    send_to_server(my_socket, username_and_password)

    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()
    print("server sent:" + input_of_server)

    if input_of_server == "username dont exist":
        error = tkinter.Label(frame, text="wrong username")
        error.place(x=100, y=320)
    elif input_of_server == "wrong password":
        error = tkinter.Label(frame, text="wrong password")
        error.place(x=100, y=320)
    else:
        action_page(frame, my_socket)


def action_page(frame, my_socket):
    clear_page(frame)
    title = tkinter.Label(frame, text="Choose An Action:", font=("italic", 16))
    title.place(x=50, y=25)
    add_description = tkinter.Label(frame, text="Add- Add a new password")
    add_description.place(x=50, y=75)
    get_description = tkinter.Label(frame, text="Get- Retrieve an existing password")
    get_description.place(x=50, y=100)
    update_description = tkinter.Label(frame, text="Update - Update the password for a site")
    update_description.place(x=50, y=125)
    add_button = tkinter.Button(frame, text="ADD", height=3, width=15, fg="white", bg="pink",
                                command=lambda button_pressed="ADD":
                                add_page1(frame, my_socket))
    add_button.place(x=100, y=175)
    get_button = tkinter.Button(frame, text="GET", height=3, width=15, fg="white", bg="light blue",
                                command=lambda button_pressed="ADD":
                                get_page1(frame, my_socket)
                                )
    get_button.place(x=100, y=250)
    update_button = tkinter.Button(frame, text="UPDATE", height=3, width=15, fg="white", bg="magenta",
                                   command=lambda button_pressed="ADD": update_page1(frame, my_socket))
    update_button.place(x=100,y=325)
    exit_button = tkinter.Button(frame, text="EXIT", height=3, width=15, fg="white", bg="red",
                                 command=lambda button_pressed="EXIT":
                                 exit_page(frame, my_socket))
    exit_button.place(x=100, y=400)


def add_page1(frame, my_socket):
    clear_page(frame)
    header1 = tkinter.Label(frame, text="Add Page", font=("italic", 16))
    header1.place(x=100, y=25)
    header2 = tkinter.Label(frame, text="Add a new website to your password manager")
    header2.place(x=50, y=55)
    instruction = tkinter.Label(frame, text="Enter site name or URL")
    instruction.place(x=100, y=100)
    site_name = tkinter.Entry(frame)
    site_name.place(x=100, y=130)
    site = site_name.get()
    check_site = tkinter.Button(frame, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                command=lambda button_pressed="ADD check site":
                                check_site_add(frame, my_socket, site))
    check_site.place(x=100, y=200)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="ADD check site":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=100, y=270)


def check_site_add(frame, my_socket, site):
    description_of_data = "ADD check site:"
    description_and_data = (description_of_data, site)
    site_final = " ".join(description_and_data)

    send_to_server(my_socket, site_final)

    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()
    print("input of server: " + input_of_server)
    if input_of_server == "website does not exist":
        error = tkinter.Label(frame, text="The website you entered is not valid")
        error.place(x=100, y=350)
    elif input_of_server == "website already exists":
        error = tkinter.Label(frame, text="website already in system")
        error.place(x=100, y=350)
    else:
        add_page2(frame, my_socket)


def add_page2(frame, my_socket):
    clear_page(frame)
    instruction = tkinter.Label(frame, text="Enter password for site:", font=("italic", 16))
    instruction.place(x=100, y=25)
    enter_password = tkinter.Entry(frame)
    enter_password.place(x=100, y=75)
    password = enter_password.get()
    check_password = tkinter.Button(frame, text="check password", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="ADD check password":
                                    check_password_site(frame, my_socket, password, True))
    check_password.place(x=100, y=200)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="back to action page":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=100, y=270)


def check_password_site(frame, my_socket, password, add):
    if add:
        description_of_data = "ADD check password:"
    else:
        description_of_data = "UPDATE check password:"
    description_and_data = (description_of_data, password)
    site_final = " ".join(description_and_data)

    send_to_server(my_socket, site_final)

    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()

    if input_of_server == "error 1":
        message = tkinter.Label(frame, text="password not long enough")
        message.place(x=100, y=400)
    elif input_of_server == "error 2":
        message = tkinter.Label(frame, text="password and your verify not the same")
        message.place(x=100, y=400)
    elif input_of_server == "error 3":
        message = tkinter.Label(
            frame, text="the password must contain at least one capital letter and one small letter")
        message.place(x=100, y=400)
    elif input_of_server == "error 4":
        message = tkinter.Label(frame, text="The password you entered is your current password")
        message.place(x=100, y=400)
    else:
        message = tkinter.Label(frame, text="Password added successfully")
        message.place(x=100, y=400)


def get_page1(frame, my_socket):
    clear_page(frame)
    header1 = tkinter.Label(frame, text="Get Page", font=("italic", 16))
    header1.place(x=100, y=25)
    header2 = tkinter.Label(frame, text="Get password to a chosen website")
    header2.place(x=50, y=55)
    instruction = tkinter.Label(frame, text="Enter site name or URL")
    instruction.place(x=100, y=100)
    site_name = tkinter.Entry(frame)
    site_name.place(x=100, y=130)
    site = site_name.get()
    check_site = tkinter.Button(frame, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                command=lambda button_pressed="Check site":
                                check_site_validity(frame, my_socket, site, True))
    check_site.place(x=100, y=200)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="Back to action page":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=100, y=270)


def check_site_validity(frame, my_socket, site, get):
    description_of_data = "check site:"
    description_and_data = (description_of_data, site)
    site_final = " ".join(description_and_data)

    send_to_server(my_socket, site_final)

    length_message_server_sent = my_socket.recv(2).decode()
    input_of_server = my_socket.recv(int(length_message_server_sent)).decode()
    print("input of server: " + input_of_server)
    if input_of_server == "site not in system":
        error = tkinter.Label(frame, text="The website you entered is not saved in the system")
        error.place(x=100, y=350)
    else:
        if get:
            password = input_of_server[14:]
            get_page2(frame, my_socket, password)
        else:
            update_page2(frame, my_socket, site)


def get_page2(frame, my_socket, password):
    clear_page(frame)
    message = tkinter.Label(frame, text="Your password for this website is:", font=("italic", 16))
    message.place(x=75, y=25)
    encoded_password = ""
    for letter in password:
        encoded_password += "* "

    show_encoded_password = tkinter.Label(frame, text=encoded_password)
    show_encoded_password.place(x=150, y=75)
    show_password_button = tkinter.Button(frame, text="Show Password", height=3, width=15, fg="white", bg="pink",
                                          command=lambda button_pressed="show password":
                                          show_password(frame, password, show_encoded_password))
    show_password_button.place(x=150, y=125)
    copy_password_button = tkinter.Button(frame, text="copy password", height=3, width=15, fg="white", bg="pink",
                                          command=lambda button_pressed="copy password":
                                          copy_password(frame, password))
    copy_password_button.place(x=150, y=185)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="Back to action page":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=150, y=245)


def show_password(frame, password, show_encoded_password):
    show_encoded_password.destroy()
    show_password_on_screen = tkinter.Label(frame, text=password)
    show_password_on_screen.place(x=150, y=75)


def copy_password(frame, password):
    frame.clipboard_clear()
    frame.clipboard_append(password.rstrip())
    success_message = tkinter.Label(frame, text="password is copied to keyboard")
    success_message.place(x=150, y=350)


def update_page1(frame, my_socket):
    clear_page(frame)
    header1 = tkinter.Label(frame, text="Update Page", font=("italic", 16))
    header1.place(x=100, y=25)
    header2 = tkinter.Label(frame, text="Update password to a chosen website")
    header2.place(x=50, y=55)
    instruction = tkinter.Label(frame, text="Enter site name or URL")
    instruction.place(x=100, y=100)
    site_name = tkinter.Entry(frame)
    site_name.place(x=100, y=130)
    site = site_name.get()
    check_site = tkinter.Button(frame, text="Check Site", height=3, width=15, fg="white", bg="pink",
                                command=lambda button_pressed="UPDATE check site":
                                check_site_validity(frame, my_socket, site, False))
    check_site.place(x=100, y=200)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="ADD check site":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=100, y=270)


def update_page2(frame, my_socket, site):
    clear_page(frame)
    instruction = tkinter.Label(frame, text="Your new password:", font=("italic", 16))
    instruction.place(x=100, y=25)
    enter_password = tkinter.Entry(frame)
    enter_password.place(x=100, y=75)
    password = enter_password.get()
    check_password = tkinter.Button(frame, text="check password", height=3, width=15, fg="white", bg="pink",
                                    command=lambda button_pressed="UPDATE check site":
                                    check_password_site(frame, my_socket, (password + " " + site), False))
    check_password.place(x=100, y=200)
    back_to_action_page = tkinter.Button(frame, text="Back to action page", height=3, width=15, fg="white", bg="pink",
                                         command=lambda button_pressed="back to action page":
                                         action_page(frame, my_socket))
    back_to_action_page.place(x=100, y=270)


def exit_page(frame, my_socket):
    clear_page(frame)
    message = tkinter.Label(frame, text="Are you sure you want to exit the program?", font=("italic", 16))
    message.place(x=25, y=25)
    yes_button = tkinter.Button(frame, text="yes", height=3, width=15, fg="white", bg="red",
                                command=lambda button_pressed="EXIT":
                                exit_program(frame, my_socket))
    yes_button.place(x=100, y=100)
    no_button = tkinter.Button(frame, text="no", height=3, width=15, fg="white", bg="green",
                               command=lambda button_pressed="EXIT": action_page(frame, my_socket))
    no_button.place(x=250, y=100)


def exit_program(frame, my_socket):
    message = "EXIT"
    send_to_server(my_socket, message)

    greeting_page(frame, my_socket)
    my_socket.close()


def clear_page(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


if __name__ == "__main__":
    main()
