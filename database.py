import crypt
import app
import sqlite3
import os

def create_db():
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr/passwords.db")
    cur = db.cursor()
    cur.execute('''CREATE TABLE passwords
                    (id integer PRIMARY KEY, username text NOT NULL, password text NOT NULL)''')

    db.commit()
    db.close()

def insert_into_db(username, password):
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr/passwords.db")
    cur = db.cursor()

    if os.path.isfile(f"{os.getenv('HOME')}/passmgr/sql_id"):
        sql_id_file = open(f"{os.getenv('HOME')}/passmgr/sql_id", "r")
        sql_id = int(sql_id_file.read())
        sql_id_file.close()
    else:
        sql_id = 1

    cur.execute("INSERT INTO passwords VALUES (" + str(sql_id) + ", '" + username + "', '" + password + "')")

    db.commit()
    db.close()

    sql_id += 1

    sql_id_file = open(f"{os.getenv('HOME')}/passmgr/sql_id", "w")
    sql_id_file.write(str(sql_id))
    sql_id_file.close()

def read_from_db(sql_id):
    db = sqlite3.connect(f"{os.getenv('HOME')}/passmgr/passwords.db")
    cur = db.cursor()
    
    # TODO: Save ids, usernames and passwords for temporary use
    for row in cur.execute("SELECT * FROM passwords ORDER BY id"):
        print(row)
