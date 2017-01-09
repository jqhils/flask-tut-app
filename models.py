from flask_sqlalchemy import SQLAlchemy
import datetime

from app import db

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __init__(self, username, password):
        now = datetime.datetime.now()

        self.username = username
        self.password = password
        self.date_created = now

    def __repr__(self):
        return '<User %r>' % self.username

class Poll(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('users', lazy='dynamic'))
    question = db.Column(db.Text)
    response_yes = db.Column(db.Integer)
    response_no = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)

    def __init__(self, user, question):
        now = datetime.datetime.now()

        self.user = user
        self.question = question
        self.response_yes = 0
        self.response_no = 0
        self.date_created = now

    def __repr__(self):
        return '<Poll %r>' % self.question
