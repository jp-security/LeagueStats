#Program to display stats for the CAG Season 55

from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, send_file
from flask.ext.sqlalchemy import SQLAlchemy
#from wtforms import Form, BooleanField, TextField, validators, SelectField, TextAreaField, HiddenField
import flask.views

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True
  , SECRET_KEY='secret!'
  , PROPAGATE_EXCEPTION=True
))
db = SQLAlchemy(app)

port = 5000
localhost = "127.0.0.1"

@app.route('/stats')
def stats():
    return render_template('stats.html', host="localhost", port=port)


if __name__ == "__main__":
    app.run(port=port)
