from cryptography.fernet import Fernet
import hashlib
from Crypto.Cipher import AES
import string
import random
import os

def hash(password):
    sha256 = hashlib.sha256()
    password += "YBf3i3uithAt3t3hgOHg4w4"
    sha256.update(password.encode('UTF-8'))
    final_hash = sha256.hexdigest()
    sha256 = hashlib.sha256()
    return final_hash

def generateString(length):
       return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

def advanced_password_hash(password):
    sha256 = hashlib.sha256()
    password_file = open(f"{os.getenv('HOME')}/passmgr/password", "r")
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password_salt_2"):
        password_salt_file = open(f"{os.getenv('HOME')}/passmgr/password_salt_2", "r")
        salt = password_salt_file.read()
    else:
        salt = generateString(16)
        password_salt_file = open(f"{os.getenv('HOME')}/passmgr/password_salt_2", "w")
        password_salt_file.write(salt)

    sha256.update(str(password_file.read()+password+salt).encode('UTF-8'))
    sha256_hash = sha256.hexdigest()
    password_salt_file.close()
    password_file.close()
    return sha256_hash

def do_aes_files_exist():
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/aes_key") == True:
        if os.path.isfile(f"{os.getenv('HOME')}/passmgr/db_key") == True:
            return True
        else:
            return False
    else:
        return False

def getKey(password):
    md5 = hashlib.md5()
    md5.update(advanced_password_hash(password).encode('UTF-8'))
    password_aes_key = md5.hexdigest()

    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv"):
        iv_file = open(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv", "r")
        iv = iv_file.read()
    else:
        iv = generateString(16)
        iv_file = open(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv", "w")
        iv_file.write(iv)

    iv_file.close()
    aes_object = AES.new(password_aes_key, AES.MODE_CBC, iv)

    if do_aes_files_exist() == True:
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "rb")
        encrypted_aes_key = encrypted_aes_key_file.read()
        aes_key = aes_object.decrypt(encrypted_aes_key)
        encrypted_aes_key_file.close()

        encrypted_db_key_file = open(f"{os.getenv('HOME')}/passmgr/db_key", "rb")
        encrypted_db_key = encrypted_db_key_file.read()
        db_key = aes_object.decrypt(encrypted_db_key).decode('UTF-8')
        encrypted_db_key_file.close()
        db_key = db_key.replace(' ', '')

        aes = aes_key

        return aes, db_key
    else:
        aes_key = generateString(32)
        encrypted_aes_key = aes_object.encrypt(aes_key)
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "wb")
        encrypted_aes_key_file.write(encrypted_aes_key)
        encrypted_aes_key_file.close()

        db_key = Fernet.generate_key()
        db_key = db_key.decode('UTF-8')
        while len(db_key) % 16 != 0:
            db_key += " "
        encrypted_db_key = aes_object.encrypt(db_key)
        encrypted_db_key_file = open(f"{os.getenv('HOME')}/passmgr/db_key", "wb")
        encrypted_db_key_file.write(encrypted_db_key)
        encrypted_db_key_file.close()

        aes = aes_key

        return aes, db_key

def encrypt_database(db_filepath, db_key):
    fernet = Fernet(db_key.encode('UTF-8'))

    db_file = open(db_filepath, "rb")
    db = db_file.read()
    db_file.close()

    encrypted_db = fernet.encrypt(db)

    encrypted_db_file = open(db_filepath, "wb")
    encrypted_db_file.write(encrypted_db)
    encrypted_db_file.close()


def decrypt_database(db_filepath, db_key):
    fernet = Fernet(db_key.encode('UTF-8'))

    encrypted_db_file = open(db_filepath, "rb")
    encrypted_db = encrypted_db_file.read()
    encrypted_db_file.close()

    decrypted_db = fernet.decrypt(encrypted_db)

    db_file = open(db_filepath, "wb")
    db_file.write(decrypted_db)
    db_file.close()

def encrypt_username_and_password(aes, username, password):
    while len(username) % 16 != 0:
        username += " "
    while len(password) % 16 != 0:
        password += " "
    succeeded = False
    encrypted_username = ""
    encrypted_password = ""
    username_iv = ""
    password_iv = ""
    username_iv = generateString(16)
    aes_object = AES.new(aes, AES.MODE_CBC, username_iv)
    encrypted_username = aes_object.encrypt(username)
    succeeded = True

    password_iv = generateString(16)
    aes_object = AES.new(aes, AES.MODE_CBC, password_iv)
    encrypted_password = aes_object.encrypt(password)
    succeeded = True

    password = "nothingtoseeherenothingtoseeherenothingtoseeherenothingtoseehere"
    username = "nothingtoseeherenothingtoseeherenothingtoseeherenothingtoseehere"
    aes_object = "nothingtoseeherenothingtoseeherenothingtoseeherenothingtoseehere"
    password = [encrypted_password, password_iv]
    username = [encrypted_username, username_iv]
    return username, password


