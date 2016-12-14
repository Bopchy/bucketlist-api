
class Config(object):

    """Configurations class."""
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = 'JdN!$Jzxor^ecdjIoEMuRw8ozD!MtB'


class TestingConfig(Config):

    """Testing database"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    # PRAGMA foreign_keys = ON
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False


class DevelopmentConfig(Config):

    """Development database."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_db.sqlite'
    # PRAGMA foreign_keys = ON
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):

    """Production database."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_db.sqlite'
    # PRAGMA foreign_keys = ON
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    # If no coniguration specified
    'default': DevelopmentConfig
}
