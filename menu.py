import app
import getch
import os
import math
import crypt
import database
import auth

def add_password_menu(aes, db_key):
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
        if c in ("e", "E"):
            continue
        if c in ("b", "B"):
            return
        else:
            password_verified = True
    username, password = crypt.encrypt_username_and_password(aes, username, password)
    database.insert_into_db(db_key, website, username[0], password[0], username[1], password[1])

def show_password(passid, credentials, aes):
    passid = passid - 1
    credentials = credentials[passid]
    encrypted_username = credentials[2]
    encrypted_password = credentials[3]
    username_iv = credentials[4]
    password_iv = credentials[5]

    username, password = crypt.decrypt_username_and_password(aes, encrypted_username, encrypted_password,
                                        username_iv, password_iv)

    height, width = os.popen("stty size", 'r').read().split()
    height = int(height)
    width = int(width)
    passwordScreen = True
    while passwordScreen is True:
        os.system("clear")

        for _ in range(math.floor((height-5)/2)):
            print("")

        username_text = "Username: " + username
        print(username_text.center(width))
        password_text = "Password: " + ("*"*len(password))
        print(password_text.center(width))
        print("")
        print("(B)ack, (Q)uit, or (R)eveal".center(width))

        for _ in range(math.floor((height-5)/2)):
            print("")

        c = getch.getch()

        if c in ("b", "B"):
            passwordScreen = False
        if c in ("q", "Q"):
            app.quit_app()
        if c in ("r", "R"):
            while True:
                os.system("clear")

                for _ in range(math.floor((height-5)/2)):
                    print("")
                
                username_text = "Username: " + username
                print(username_text.center(width))
                password_text = "Password: " + password
                print(password_text.center(width))
                print("")
                print("(B)ack or (Q)uit".center(width))

                for _ in range(math.floor((height-5)/2)):
                    print("")

                c2 = getch.getch()

                if c2 in ("b", "B"):
                    passwordScreen = False
                    break
                if c2 in ("q", "Q"):
                    app.quit_app()
    
    del passid
    del credentials
    del encrypted_username
    del encrypted_password
    del username_iv
    del password_iv
    del username
    del password
    del username_text
    del password_text

def get_password_menu(aes, db_key):
    c = None
    hadError = False
    credentials = database.read_from_db(db_key)
    del db_key
    credentials_length = len(credentials)
    while True:
        os.system("clear")
        print("Type the ID of the credentials or B to get back to the menu")
        print("")
        height = os.popen("stty size", 'r').read().split()[0]
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
        if c in range(1, credentials_length+1):
            show_password(c, credentials, aes)
        else:
            hadError = True
    del credentials
    del credentials_length

def remove_password_menu(db_key):
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
        if c in range(1, credentials_length+1):
            if auth.verified() is True:
                database.delete_from_db(db_key, credentials[c-1][0])
                os.system("clear")
                for _ in range(math.floor(int(height)/2)-2):
                    print("")
                print(("Deleted password with ID " + str(c) + ".").center(int(width)))
                print("Press Any key, to return to the Main Menu.".center(int(width)))
                for _ in range(math.floor(int(height)/2)-1):
                    print("")
                confirmation = getch.getch()
                break
            else:
                continue
        else:
            hadError = True
    del db_key
    del credentials
    del credentials_length

def menu(aes, db_key):
    while True:
        os.system("clear")
        height, width = os.popen("stty size", 'r').read().split()
        menu_options = "(A)dd Credentials, (G)et Credentials, (R)emove Credentials or (Q)uit"
        height_until_middle = math.floor(int(height)/2)
        for _ in range(height_until_middle):
            print("")
        print(menu_options.center(int(width)))
        for _ in range((int(height)-height_until_middle-1)):
            print("")
        c = getch.getch()
        if c in ("a", "A"):
            add_password_menu(aes, db_key)
        if c in ("g", "G"):
            get_password_menu(aes, db_key)
        if c in ("r", "R"):
            remove_password_menu(db_key)
        if c in ("c", "C"):
            os.system("clear")
            for _ in range(math.floor(int(height)/2)-5):
                print("")
            print("You discovered an Easter Egg!".center(int(width)))
            print("This program was created by arongeo.".center(int(width)))
            print("https://arongeo.com/".center(int(width)))
            print("")
            print("Press any key to return to the Main Menu.".center(int(width)))
            for _ in range(math.floor(int(height)/2)-1):
                print("")
            confirmation = getch.getch()
        if c in ("q", "Q"):
            app.quit_app()

