

class Config(object):

    """Configurations class."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


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
