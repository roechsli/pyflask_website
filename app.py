import os
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import hashlib

from dbconnect import connection


file_path = os.path.abspath(os.getcwd())+"\database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(150))
    password = db.Column(db.String(32))
    password_clear = db.Column(db.String(32))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    print("hello")
    try:
        c, conn = connection()

        error = None
        if request.method == 'POST':

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             request.form['uname'])
            print("printing fetchone")
            print(c.fetchone())
            data = c.fetchone()[2]

            if data == hashlib.md5(request.form['password']).hexdigest():
                session['logged_in'] = True
                session['username'] = request.form['username']
                # flash('You are now logged in.'+str(session['username']))
                return redirect(url_for('dashboard'))

            else:
                error = 'Invalid credentials. Try again'
        return render_template('login.html', error=error)
    except Exception as e:
        error = 'Invalid credentials. Try again'
        return render_template('login.html', error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        register = User(username=uname, email=mail, password=hashlib.md5(passw.encode('utf-8')).hexdigest(), password_clear='', firstname=firstname, lastname=lastname)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
