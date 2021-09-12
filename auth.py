import os
import crypt
import database
import menu
import app

def register(password):
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") == True:
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
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") == False:
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
            if os.path.isfile(f"{os.getenv('HOME')}/passmgr/passwords.db") == False:
                database.create_db()
                crypt.encrypt_database(f"{os.getenv('HOME')}/passmgr/passwords.db", db_key)
            menu.menu(aes, db_key)
        else:
            return False

