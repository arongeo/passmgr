# passmgr

![Python Build](https://github.com/arongeo/passmgr/workflows/Python-Build/badge.svg) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/42ae3d1011c34573b5faf0a56fc08483)](https://app.codacy.com/gh/arongeo/passmgr?utm_source=github.com&utm_medium=referral&utm_content=arongeo/passmgr&utm_campaign=Badge_Grade_Settings)

A Password Manager in Terminal. Written in Python. Made by @arongeo

THIS IS A WORK IN PROGRESS AND VERY MUCH NOT DONE, SO DON'T USE IT YET!

## Security
- Each username/e-mail and password is encrypted with AES-256 encryption before saving it into the SQLite Database.
- The SQLite Database is encrypted.
- Your master password is custom salted, then hashed with SHA-256 and MD-5, to produce the AES-256 key to decrypt your other AES-256 key, which is custom generated.

So, to sum it up, pretty secure.
