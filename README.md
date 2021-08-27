# passmgr
A Password Manager in Terminal. Written in Python. Made by @mrmalac

## How secure is it?
- Each username/e-mail and password is encrypted with AES-256 encryption before saving it into the SQLite Database.
- The SQLite Database is encrypted with SQLCipher.
- Your master password is custom salted, then hashed with SHA-256 and MD-5.

So, to sum it up, pretty secure.
