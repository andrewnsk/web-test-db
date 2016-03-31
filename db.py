import sqlite3
from datetime import datetime
import os.path
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


def local_time():
    # Текущее время и дата
    time = datetime.now().replace(microsecond=0)
    return time


#############################################################################
db_file_name = "config.db"
date_time = local_time()


#############################################################################


def db_create(db_file_name_local):
    # База с данными пользователей
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()
    db_conn_cursor.execute('''CREATE TABLE users
        (id INTEGER PRIMARY KEY,
        mail TEXT,
        password TEXT,
        reg_date TEXT,
        userpic TEXT,
        is_admin TEXT,
        username TEXT)''')
    db_connection.commit()
    db_connection.close()
    logging.debug('db file created')


def db_write(db_file_name_local, mail, password, reg_date, userpic, is_admin, username):
    # База с данными пользователей
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


def db_read(db_file_name_local, limit, last_value):
    # База с данными пользователей
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()
    data = db_conn_cursor.fetchall()
    for row in db_conn_cursor.execute('SELECT * '
                                      'FROM users '
                                      'WHERE id > {0} '
                                      'ORDER BY id '
                                      'LIMIT {1}'.format(last_value, limit)):
        print(row)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    db_connection.close()
    return data


'''
SELECT *
FROM MyTable
WHERE SomeColumn > LastValue
ORDER BY SomeColumn
LIMIT 100

'''

if not (os.path.isfile(db_file_name)):
    logging.debug('db file not exist')
    db_create(db_file_name)


print(random.randint(0, 1000))
