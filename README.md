# passmgr

![Python Build](https://github.com/arongeo/passmgr/workflows/Python-Build/badge.svg) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/42ae3d1011c34573b5faf0a56fc08483)](https://app.codacy.com/gh/arongeo/passmgr?utm_source=github.com&utm_medium=referral&utm_content=arongeo/passmgr&utm_campaign=Badge_Grade_Settings)

[![DeepSourceActive](https://deepsource.io/gh/arongeo/passmgr.svg/?label=active+issues&token=_bvaZSawPpTjojuKB3RBavc7)](https://deepsource.io/gh/arongeo/passmgr/?ref=repository-badge)
[![DeepSourceResolved](https://deepsource.io/gh/arongeo/passmgr.svg/?label=resolved+issues&token=_bvaZSawPpTjojuKB3RBavc7)](https://deepsource.io/gh/arongeo/passmgr/?ref=repository-badge)

A Password Manager in Terminal. Written in Python. Made by @arongeo

! Passmgr is still in works, although it is usable. There may still be some security risks, so use it at your own risk. !

## Security
- Each username/e-mail and password is encrypted with AES-256 encryption before saving it into the SQLite Database.
- The SQLite Database is encrypted.
- Your master password is custom salted, then hashed with SHA-256 and SHA-512 to produce the AES-256 key to decrypt your other AES-256 key, which is custom generated.
