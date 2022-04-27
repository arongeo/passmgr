import crypt
import app
import sqlite3
import os

def create_db():
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr_data/passwords.db")
    cur = db.cursor()
    cur.execute('''CREATE TABLE passwords
                    (id integer PRIMARY KEY, websitename text NOT NULL, username text BLOB, password text BLOB, usernameiv text NOT NULL, passwordiv text NOT NULL)''')

    db.commit()
    db.close()

def insert_into_db(db_key, websitename, username, password, username_iv, password_iv):
    crypt.decrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr_data/passwords.db")
    cur = db.cursor()

    if os.path.isfile(f"{os.getenv('HOME')}/passmgr_data/sql_id"):
        sql_id_file = open(f"{os.getenv('HOME')}/passmgr_data/sql_id", "r")
        sql_id = int(sql_id_file.read())
        sql_id_file.close()
    else:
        sql_id = 1

    cur.execute("INSERT INTO passwords VALUES (" + str(sql_id) + ", '" + websitename + "', ?, ?, '" + username_iv + "', '" + password_iv + "')", [memoryview(username), memoryview(password)])

    db.commit()
    db.close()

    crypt.encrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)

    sql_id += 1

    sql_id_file = open(f"{os.getenv('HOME')}/passmgr_data/sql_id", "w")
    sql_id_file.write(str(sql_id))
    sql_id_file.close()

def reset_id():
    sql_id = 1
    sql_id_file = open(f"{os.getenv('HOME')}/passmgr_data/sql_id", "w")
    sql_id_file.write(str(sql_id))
    sql_id_file.close()
    
def read_from_db(db_key):
    crypt.decrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr_data/passwords.db")
    cur = db.cursor()   

    credentials = []

    for row in cur.execute("SELECT * FROM passwords ORDER BY id"):
        credentials.append(row)

    crypt.encrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)

    return credentials

def delete_from_db(db_key, sql_id):
    crypt.decrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr_data/passwords.db")
    cur = db.cursor()
    cur.execute('DELETE FROM passwords WHERE id = ' + str(sql_id) + ';')

    db.commit()
    db.close()

    crypt.encrypt_database(f"{os.getenv('HOME')}/passmgr_data/passwords.db", db_key)
