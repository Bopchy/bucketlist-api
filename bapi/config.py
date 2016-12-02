import string
import random


class Config(object):

    """Configurations class."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(32))

class TestingConfig(Config):

    """Testing database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'


class DevelopmentConfig(Config):

    """Development database."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_db.sqlite'


class ProductionConfig(Config):

    """Production database."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_db.sqlite'


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # If no coniguration specified
    'default': DevelopmentConfig
}
