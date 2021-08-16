import cryptography
import rsa
import hashlib

def hash(password):
    sha256 = hashlib.sha256()
    password += "YBf3i3uithAt3t3hgOHg4w4"
    sha256.update(password.encode('UTF-8'))
    final_hash = sha256.hexdigest()
    sha256 = hashlib.sha256()
    return final_hash
