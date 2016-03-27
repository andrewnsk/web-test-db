import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='system.log')


def validate_login():
    logging.debug('validate login')
    return False


def log_the_user_in():
    logging.debug('log the user in')
    return False
