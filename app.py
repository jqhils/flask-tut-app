from flask import Flask, url_for, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import flask_login as login

import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'data.sqlite')
# This should be kept really secret
app.config['SECRET_KEY'] = '123456789'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models import *

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    polls = Poll.query.all()
    return render_template("index.html", polls=polls)


@app.route("/profile/<username>")
def profile(username):
    fetched_user = User.query.filter_by(username=username).first()
    if (fetched_user):
        polls = Poll.query.filter_by(user=fetched_user)
        return render_template("profile.html", user=fetched_user, polls=polls)
    else:
        return render_template("profile.html", user=None)
    return render_template("profile.html", user=user)


@app.route("/poll/<int:poll_id>", methods=['GET', 'POST'])
def show_poll(poll_id):
    fetched_poll = Poll.query.get(poll_id)
    if (fetched_poll):
        if (request.method == 'POST'):
            if (request.form['answer']):
                if (request.form['answer'] == "yes"):
                    fetched_poll.response_yes += 1
                elif (request.form['answer'] == "no"):
                    fetched_poll.response_no += 1
                db.session.add(fetched_poll)
                db.session.commit()
        return render_template("poll.html", poll=fetched_poll)
    else:
        return render_template("poll.html", poll=None)


@app.route("/newpoll", methods=['GET', 'POST'])
@login_required
def new_poll():
    if request.method == 'POST':
        if len(request.form['question']):
            new_poll = Poll(current_user, request.form['question'])
            db.session.add(new_poll)
            db.session.commit()
            return redirect("/poll/"+str(new_poll.id))
    else:
        return render_template("newpoll.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if (user):
            if (user.password == request.form['password']):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/")
        return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run()
