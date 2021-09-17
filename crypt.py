from cryptography.fernet import Fernet
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import string
import random
import os

def sha256_hash(password):
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
    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/aes_key") is True:
        return os.path.isfile(f"{os.getenv('HOME')}/passmgr/db_key") is True
    else:
        return False

def getKey(password):
    sha512 = hashlib.sha512()
    sha512.update(advanced_password_hash(password).encode('UTF-8'))
    password_aes_key = sha512.hexdigest()
    password_aes_key = password_aes_key[:32]

    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv"):
        iv_file = open(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv", "r")
        iv = iv_file.read()
    else:
        iv = generateString(16)
        iv_file = open(f"{os.getenv('HOME')}/passmgr/password_aes_key_iv", "w")
        iv_file.write(iv)

    iv_file.close()
    cipher = Cipher(algorithms.AES(password_aes_key.encode('UTF-8')), modes.CBC(iv.encode('UTF-8')))

    del sha512
    del password_aes_key

    if do_aes_files_exist() is True:
        decryptor = cipher.decryptor()
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "rb")
        encrypted_aes_key = encrypted_aes_key_file.read()
        aes_key = decryptor.update(encrypted_aes_key) + decryptor.finalize()
        encrypted_aes_key_file.close()

        del decryptor

        decryptor = cipher.decryptor()
        
        encrypted_db_key_file = open(f"{os.getenv('HOME')}/passmgr/db_key", "rb")
        encrypted_db_key = encrypted_db_key_file.read()
        db_key = decryptor.update(encrypted_db_key) + decryptor.finalize()
        db_key = db_key.decode('UTF-8')
        encrypted_db_key_file.close()
        db_key = db_key.replace(' ', '')

        del decryptor
        del cipher

        aes = aes_key

        return aes, db_key
    else:
        encryptor = cipher.encryptor()
        aes_key = os.urandom(32)
        encrypted_aes_key = encryptor.update(aes_key) + encryptor.finalize()
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "wb")
        encrypted_aes_key_file.write(encrypted_aes_key)
        encrypted_aes_key_file.close()

        del encryptor

        encryptor = cipher.encryptor()

        db_key = Fernet.generate_key()
        db_key = db_key.decode('UTF-8')
        while len(db_key) % 16 != 0:
            db_key += " "
        encrypted_db_key = encryptor.update(db_key.encode('UTF-8')) + encryptor.finalize()
        encrypted_db_key_file = open(f"{os.getenv('HOME')}/passmgr/db_key", "wb")
        encrypted_db_key_file.write(encrypted_db_key)
        encrypted_db_key_file.close()

        del encryptor
        del cipher

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

    username_iv = generateString(16)
    cipher = Cipher(algorithms.AES(aes), modes.CBC(username_iv.encode('UTF-8')))
    encryptor = cipher.encryptor()
    encrypted_username = encryptor.update(username.encode('UTF-8')) + encryptor.finalize()

    del encryptor
    del cipher

    password_iv = generateString(16)
    cipher = Cipher(algorithms.AES(aes), modes.CBC(password_iv.encode('UTF-8')))
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode('UTF-8')) + encryptor.finalize()
    
    del encryptor
    del password
    del username
    del cipher
    password = [encrypted_password, password_iv]
    username = [encrypted_username, username_iv]
    return username, password

def decrypt_username_and_password(aes, encrypted_username, encrypted_password, username_iv, password_iv):
    cipher = Cipher(algorithms.AES(aes), modes.CBC(username_iv.encode('UTF-8')))
    decryptor = cipher.decryptor()
    username = decryptor.update(encrypted_username) + decryptor.finalize()
    username = username.decode('UTF-8')
    username = username.replace(' ', '')

    del decryptor
    del cipher

    cipher = Cipher(algorithms.AES(aes), modes.CBC(password_iv.encode('UTF-8')))
    decryptor = cipher.decryptor()
    password = decryptor.update(encrypted_password) + decryptor.finalize()
    password = password.decode('UTF-8')
    password = password.replace(' ', '')
    
    del decryptor
    del cipher

    return username, password
