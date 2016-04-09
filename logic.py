import logging
from flask import url_for
from flask import redirect
from db import db_write, db_read
import string
import random
from datetime import datetime


db_file_name = "config.db"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


def validate_login(username, password):
    logging.debug('validate login' + username + password)
    return True


def log_the_user_in(username):
    logging.debug('log the user in')
    return redirect(url_for('index'))


def handle_message(name, email, message):
    logging.debug(name + " " + email + " " + message)
    return True


def gen_pass(size=12, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gen_mail(size=3, chars=string.ascii_letters + string.digits):

    return ''.join(random.choice(chars) for _ in range(size)) + '@' + \
           ''.join(random.choice(chars) for _ in range(size)) + '.' + \
           ''.join(random.choice(chars) for _ in range(size))


def gen_name(size=5, first_sign=string.ascii_uppercase , chars=string.ascii_letters):
    return ''.join(random.choice(first_sign)) + ''.join(random.choice(chars) for _ in range(size))


def local_time():
    # Текущее время и дата
    time = datetime.now().replace(microsecond=0)
    return time


def fill_db(iteration=20):
    for hop in range(iteration):
        db_write(gen_mail(), gen_pass(), local_time(), 'none', 'false', gen_name())

fill_db()


def user_list():
    return db_read(db_file_name, 100, 0)

print(user_list()[0][0])

