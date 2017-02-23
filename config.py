import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='secret!'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAG_MAIL_SUBJECT_PREFIX = '[CAG STATS]'
    CAG_MAIL_SENDER = 'CAG Stats Admin <test@test.com>'
    CAG_ADMIN = os.environ.get('CAG_ADMIN')

    @staticmethod
    def init_app(app):
        pass

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
    SQLALCHEMY_DATABASE_URI=('mysql://root:password1@localhost/cagstats')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=('DATABASE_URL') or \
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
            fromaddr = cls.FLASKY_MAIL_SENDER,
            toaddrs = [cls.FLASKY_MAILSENDER],
            subject = cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials = credentials,
            secure = secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
