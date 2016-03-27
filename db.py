import sqlite3
from datetime import datetime
import os.path


def local_time():
    # Текущее время и дата
    time = datetime.now().replace(microsecond=0)
    return time

#############################################################################
db_file_name = "config.db"
date_time = local_time()

#############################################################################


def create_db(db_file_name_local):
    # База с данными пользователей
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()
    db_conn_cursor.execute('''CREATE TABLE users
        (id INTEGER PRIMARY KEY,
        mail TEXT,
        password TEXT,
        reg_date TEXT,
        userpic INTEGER,
        is_admin TEXT,
        username TEXT)''')
    db_connection.commit()
    db_connection.close()
    print("File created")


def open_and_write_db(db_file_name_local, mail, password, reg_date, userpic, is_admin, username):
    # База с погодными данными
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()
    db_conn_cursor.execute('''INSERT INTO users(mail, password, reg_date, userpic, is_admin, username)
                  VALUES(?,?,?,?,?,?)''', (mail, password, reg_date, userpic, is_admin, username))
    # Save (commit) the changes
    db_connection.commit()
    for row in db_conn_cursor.execute('SELECT * FROM users ORDER BY id'):
            print(row)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    db_connection.close()

if not (os.path.isfile(db_file_name)):
    create_db(db_file_name)

open_and_write_db(db_file_name)