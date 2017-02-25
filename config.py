import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CAG_MAIL_SUBJECT_PREFIX = '[CAG STATS]'
    CAG_MAIL_SENDER = 'CAG Stats Admin <cagstats@gmail.com>'
    CAG_ADMIN = os.environ.get('CAG_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI=('mysql://root:password1@localhost/cagstats')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI=('mysql://root:password1@localhost/cagstats')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        'mysql://root:password1@localhost/cagstats' + os.path.join(basedir, 'cagstats')

    @classmethod
    def init_add(cls, app):
        Config.init_app(app)

        #email errors to the admin
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr = cls.CAG_MAIL_SENDER,
            toaddrs = [cls.CAG_MAIL_SENDER],
            subject = cls.CAG_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials = credentials,
            secure = secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        #log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

        #handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

config = {
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'stats': HerokuConfig
}
