# passmgr

[![codecov](https://codecov.io/gh/arongeo/passmgr/branch/master/graph/badge.svg?token=3WEX02TJH9)](https://codecov.io/gh/arongeo/passmgr)

A Password Manager in Terminal. Written in Python. Made by @mrmalac

THIS IS A WORK IN PROGRESS AND VERY MUCH NOT DONE, SO DON'T USE IT YET!

## How secure is it?
- Each username/e-mail and password is encrypted with AES-256 encryption before saving it into the SQLite Database.
- The SQLite Database is encrypted.
- Your master password is custom salted, then hashed with SHA-256 and MD-5, to produce the AES-256 key to decrypt your other AES-256 key, which is custom generated.

So, to sum it up, pretty secure.
