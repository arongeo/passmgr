import os
import crypt
import database
import menu
import app
import getpass

def register(password):
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") is True:
        os.system("clear")
        print("[ERROR] Password file already exists, quitting!")
        app.quit_app()
    else:
        os.makedirs(f"{os.getenv('HOME')}/passmgr")
        password_hash = crypt.sha256_hash(password)
        file = open(f"{os.getenv('HOME')}/passmgr/password", "w")
        file.write(password_hash)
        file.close()
        del password
        return

def login(password):
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") is False:
        os.system("clear")
        print("[ERROR] Password file doesn't exist, quitting!")
        app.quit_app()
    else:
        password_hash = crypt.sha256_hash(password)
        file = open(f"{os.getenv('HOME')}/passmgr/password", "r")
        file_password_hash = file.read()
        file.close()
        if password_hash == file_password_hash:
            # DONE: Decrypt the key with the password
            # Keyscheme:
            #
            # -PASSWORD--AESKEY--ENCRYPTED_PASSWORDS
            #
            aes, db_key = crypt.getKey(password)
            if os.path.isfile(f"{os.getenv('HOME')}/passmgr/passwords.db") is False:
                database.create_db()
                crypt.encrypt_database(f"{os.getenv('HOME')}/passmgr/passwords.db", db_key)
            menu.menu(aes, db_key)
        else:
            return False

def verified():
    lock = ["", " @@@@@@@ ", " @@     @@ ", " @       @ "," @       @ ","@@@@@@@@@@@","@@@@@@@@@@@","@@@@@ @@@@@","@@@@@ @@@@@","@@@@@@@@@@@","@@@@@@@@@@@", "", "passmgr", "", ""]
    width = os.popen("stty size", 'r').read().split()[1]
    login_status = True
    with open(f"{os.getenv('HOME')}/passmgr/password", 'r') as file:
        hashed_password = file.read()
        file.close()
    while True:
        os.system("clear")
        # Print Lock Icon
        for i in range(len(lock)):
            print(lock[i].center(int(width)))
        print("")
        print("Press B and ENTER to go back.".center(int(width)))
        print("")
        if login_status is False:
            print("Master Password is incorrect, please try again!")
            print("")
        print("Enter Master Password to verify:".center(int(width)))
        password = getpass.getpass("".center(round(int(width)/2)-1))
        if password in ("b", "B"):
            break
        elif crypt.sha256_hash(password) == hashed_password:
            del password
            del hashed_password
            return True
    return False
