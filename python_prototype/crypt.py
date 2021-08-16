import cryptography
import rsa
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

    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/aes_key"):
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "rb")
        encrypted_aes_key = encrypted_aes_key_file.read()
        aes_key = aes_object.decrypt(encrypted_aes_key)
        encrypted_aes_key_file.close()
        return aes_key
    else:
        aes_key = generateString(32)
        encrypted_aes_key = aes_object.encrypt(aes_key)
        encrypted_aes_key_file = open(f"{os.getenv('HOME')}/passmgr/aes_key", "wb")
        encrypted_aes_key_file.write(encrypted_aes_key)
        encrypted_aes_key_file.close()
        return aes_key
