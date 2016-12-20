import os


class Config(object):

    """Configurations class."""
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):

    """Testing database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):

    """Development database."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DEV_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):

    """Production database."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_PROD_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
