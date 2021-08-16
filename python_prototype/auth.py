import crypt
import os

def register(password):
    if os.path.isfile("~/passmgr/password") == True:
        os.system("clear")
        print("[ERROR] Password file already exists, quitting!")
        quit()
    else:
        os.makedirs(f"{os.getenv('HOME')}/passmgr")
        password = crypt.hash(password)
        file = open(f"{os.getenv('HOME')}/passmgr/password", "w")
        file.write(password)
        file.close()
        return

def login(password):
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password") == False:
        os.system("clear")
        print("[ERROR] Password file doesn't exist, quitting!")
        quit()
    else:
        password_hash = crypt.hash(password)
        file = open(f"{os.getenv('HOME')}/passmgr/password", "r")
        file_password_hash = file.read()
        file.close()
        if password_hash == file_password_hash:
            print("Log In Successful!")
            # TODO: Decrypt the keys with the password
        else:
            return False

