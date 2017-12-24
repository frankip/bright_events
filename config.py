# config.py
import os
# Enable Flask's debugging features. Should be False in production

class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    POSTGRES = {
        'user': 'postgres',
        'pw': 'admin',
        'db': 'postgres',
        'host': 'localhost',
        'port': '5432',
    }

    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
