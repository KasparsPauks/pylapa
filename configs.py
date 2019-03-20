import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 'you-will-never-guess'


# Check Configuration section for more details
# SESSION_TYPE = 'mogodb'

