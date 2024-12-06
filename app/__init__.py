"""
Hydronium: DuaBaig, AidanWong, QianjunZhou
SoftDev
P01: ArRESTedDevelopment
2024-01-12
Time Spent: 2
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os

app = Flask(__name__)

app.secret_key = os.urandom(32)

@app.route('/', methods = ['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html", logged_in = False)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        if password == password1:
            session['username'] = username
    return render_template("register.html")

@app.route('/view', methods = ['GET', 'POST'])
def view():
    return render_template("view.html")

@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template("search.html")

@app.route('/create', methods = ['GET', 'POST'])
def create():
    return render_template("create.html")

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    return render_template("edit.html")

@app.route('/calendar', methods = ['GET', 'POST'])
def calender():
    return render_template("calendar.html")

@app.route('/hrecipes', methods = ['GET', 'POST'])
def hrecipes():
    return render_template("hrecipes.html")

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    return render_template("settings.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.debug = True
    app.run()
