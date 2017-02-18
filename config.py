import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='secret!'
    PROPAGATE_EXCEPTION=True
    CAG_MAIL_SUBJECT_PREFIX = '[CAG STATS]'
    CAG_MAIL_SENDER = 'CAG Stats Admin <test@test.com>'
    CAG_ADMIN = os.environ.get('CAG_ADMIN')

    @staticmethod
    def init_app(app):
        pass

    #port = 5000
    #localhost = "127.0.0.1"

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI=('mysql://root:password1@localhost/cagstats')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI=('TEST_DATABASE_URL') or \
        'mysql://root:password1@localhost/cagstats' + os.path.join(basedir, 'cagstats')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=('DATABASE_URL') or \
        'mysql://root:password1@localhost/cagstats' + os.path.join(basedir, 'cagstats')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
