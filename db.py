import sqlite3
import os.path
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')

#############################################################################
db_file_name = "test.db"


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


def db_write(mail, password, reg_date, userpic, is_admin, username, db_file_name_local=db_file_name):
    # База с данными пользователей
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()
    db_conn_cursor.execute('''INSERT INTO users(mail, password, reg_date, userpic, is_admin, username)
                  VALUES(?,?,?,?,?,?)''', (mail, password, reg_date, userpic, is_admin, username))
    # Save (commit) the changes
    db_connection.commit()
    db_connection.close()


def db_read(db_file_name_local, limit, last_value):
    # База с данными пользователей
    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()

    db_conn_cursor.execute('SELECT * '
                           'FROM users '
                           'WHERE id > {0} '
                           'ORDER BY id '
                           'LIMIT {1}'.format(last_value, limit))
# sql = 'select name from users order by name limit {}, {}'.format(offset, per_page)
    data = db_conn_cursor.fetchall()
    db_connection.close()
    return data


def db_get_users(offset, per_page, db_file_name_local="config.db"):

    db_connection = sqlite3.connect(db_file_name_local)
    db_conn_cursor = db_connection.cursor()

    db_conn_cursor.execute('SELECT name '
                           'FROM users '
                           'ORDER BY name '
                           'LIMIT {0}, {1}'.format(offset, per_page))
    data = db_conn_cursor.fetchall()
    db_connection.close()
    return data


def db_get_count():
    g.cur.execute('select count(*) from users')
    total = g.cur.fetchone()[0]

'''
    db_conn_cursor.execute('SELECT * '
                           'FROM users '
                           'WHERE id > {0} '
                           'ORDER BY id '
                           'LIMIT {1}'.format(last_value, limit))

SELECT *
FROM MyTable
WHERE SomeColumn > LastValue
ORDER BY SomeColumn
LIMIT 100

'''

if not (os.path.isfile(db_file_name)):
    logging.debug('db file not exist')
    db_create(db_file_name)
