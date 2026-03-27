from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

#KEY MANAGEMEMT 
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

if not os.path.exists("key.key"):
    write_key()

key = load_key()
fer = Fernet(key)

# FUNCTION 
def add_password():
    account = account_entry.get()
    password = password_entry.get()

    if account == "" or password == "":
        messagebox.showwarning("Error", "Fields cannot be empty")
        return

    encrypted_pwd = fer.encrypt(password.encode()).decode()

    with open("passwords.txt", "a") as f:
        f.write(account + "|" + encrypted_pwd + "\n")

    messagebox.showinfo("Success", "Password Added")
    account_entry.delete(0, END)
    password_entry.delete(0, END)

def view_passwords():
    try:
        with open("passwords.txt", "r") as f:
            data = f.readlines()

        output = ""
        for line in data:
            user, pwd = line.strip().split("|")
            decrypted_pwd = fer.decrypt(pwd.encode()).decode()
            output += f"{user} : {decrypted_pwd}\n"

        messagebox.showinfo("Saved Passwords", output)

    except FileNotFoundError:
        messagebox.showwarning("Error", "No passwords saved yet")

# GUI 
root = Tk()
root.title("Password Manager")
root.geometry("300x200")

Label(root, text="Account").pack()
account_entry = Entry(root)
account_entry.pack()

Label(root, text="Password").pack()
password_entry = Entry(root, show="*")
password_entry.pack()

Button(root, text="Add Password", command=add_password).pack(pady=5)
Button(root, text="View Passwords", command=view_passwords).pack(pady=5)

root.mainloop()
