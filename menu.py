import app
import getch
import os
import math
import crypt
import database
import time

def add_password(aes, db_key):
    password_verified = False
    while password_verified is False:
        os.system("clear")
        height, width = os.popen("stty size", 'r').read().split()
        height = int(height)
        width = int(width)
        height_3 = int(math.floor(height/3))
        for _ in range(height_3):
            print("")
        website = input("App/Website: ")
        username = input("E-Mail/Username: ")
        password = input("Password: ")
        for _ in range(height_3-4):
            print("")
        verify_text = "(E)dit, (B)ack to menu, or press any other key to continue"
        print(verify_text.center(width))
        for _ in range(height_3-1):
            print("")
        c = getch.getch()
        if c == "E" or c == "e":
            continue
        if c == "B" or c == "b":
            return
        else:
            password_verified = True
    username, password = crypt.encrypt_username_and_password(aes, username, password)
    database.insert_into_db(db_key, website, username[0], password[0], username[1], password[1])

def get_passwords(aes, db_key):
    c = None
    hadError = False
    credentials = database.read_from_db(db_key)
    credentials_length = len(credentials)
    while True:
        os.system("clear")
        print("Type the ID of the credentials or B to get back to the menu")
        print("")
        height, width = os.popen("stty size", 'r').read().split()
        if (int(height)-5)>credentials_length:
            for i in range(credentials_length):
                print(str(i+1) + " " + credentials[i][1])
        print("")
        if hadError is True:
            print("Invalid Choice. (There is no password with ID " + str(c) + ")")
            hadError = False
        c = input("> ")
        if c in ("b", "B", "back", "Back", "BACK"):
            break
        try:
            c = int(c)
        except ValueError:
            hadError = True
            continue
        if c in range(1, credentials_length):
            break
        else:
            hadError = True

def menu(aes, db_key):
    while True:
        os.system("clear")
        height, width = os.popen("stty size", 'r').read().split()
        menu_options = "(A)dd Password, (G)et Password, (H)elp or (Q)uit"
        height_until_middle = math.floor(int(height)/2)
        for _ in range(height_until_middle):
            print("")
        print(menu_options.center(int(width)))
        for _ in range((int(height)-height_until_middle-1)):
            print("")
        c = getch.getch()
        if c == "A" or c == "a":
            add_password(aes, db_key)
        if c == "G" or c == "g":
            get_passwords(aes, db_key)
        if c == "H" or c == "h":
            pass
        if c == "Q" or c == "q":
            app.quit_app()

