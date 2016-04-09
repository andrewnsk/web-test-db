from flask import Flask
from flask import request
from flask import render_template, current_app, g
from logic import validate_login
from logic import log_the_user_in
from logic import handle_message
from flask_paginate import Pagination
import sqlite3
from db import db_get_users, db_get_count
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


app = Flask(__name__)


@app.before_request
def before_request():
    g.conn = sqlite3.connect('test.db')
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()


@app.route('/')
def index():
    g.cur.execute('select count(id) from users')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_items()
    sql = 'select * from users order by username limit {}, {}'\
        .format(offset, per_page)
    g.cur.execute(sql)
    users = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                format_total=True,
                                format_number=True,
                                )
    return render_template('index.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )



@app.route('/search/<name>')
def search(name):
    '''This function is used to test multi values url'''
    sql = 'select count(*) from users where name like ?'
    args = ('%{}%'.format(name), )
    g.cur.execute(sql, args)
    total = g.cur.fetchone()[0]

    page, per_page, offset = get_page_items()
    sql = 'select * from users where name like ? limit {}, {}'
    g.cur.execute(sql.format(offset, per_page), args)
    users = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                )
    return render_template('index.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = current_app.config.get('PER_PAGE', 10)
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination('bootstrap3', **kwargs)
################################################################################
################################################################################


@app.route('/view')
def view():
    return "view"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/sendmessage', methods=['POST', 'GET'])
def send_message():

    if request.method == 'POST':
        logging.debug('sendmessage method post')
        if handle_message(request.form['name'], request.form['email'], request.form['message']):
            logging.debug('post ok')
            return 'ok'
        else:
            logging.debug('post error')
    logging.debug('pass')

    return 'not ok'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        logging.debug('method post')
        if validate_login(request.form['username'], request.form['password']):
            logging.debug('post ok')
            return log_the_user_in(request.form['username'])
        else:
            logging.debug('post error')
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    logging.debug('return login')
    return render_template('login.html', error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    logging.debug('running application')
    app.debug = True
    app.run()
