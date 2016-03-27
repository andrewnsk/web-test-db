from flask import Flask
from flask import request
from flask import render_template
from logic import validate_login
from logic import log_the_user_in
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


app = Flask(__name__)


@app.route('/')
def main_page():
    return "index page"


@app.route('/view')
def view():
    return "view"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/about')
def about():
    return 'The about page'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        logging.debug('method post')
        if validate_login(request.form['mail'], request.form['password']):
            logging.debug('post ok')
            return log_the_user_in(request.form['mail'])
        else:
            logging.debug('post error')
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    logging.debug('return login')
    return render_template('login.html', error=error)

if __name__ == '__main__':
    logging.debug('running application')
    app.debug = True
    app.run()
