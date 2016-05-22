import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG=True
SECRET_KEY='secret!'
PROPAGATE_EXCEPTION=True
SQLALCHEMY_DATABASE_URI=('mysql://root:password1@localhost/cagstats')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'cagstats')

port = 5000
localhost = "127.0.0.1"
