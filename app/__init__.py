"""
Hydronium: DuaBaig, AidanWong, QianjunZhou
SoftDev
P01: ArRESTedDevelopment
2024-01-12
Time Spent: 2
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

from customModules import APIModules, DBModules

app = Flask(__name__)

app.secret_key = os.urandom(32)

DBModules.initDB()

@app.route('/', methods = ['GET', 'POST'])
def dashboard():
    gifInformation = APIModules.getGif("Troll")
    if gifInformation == 403:
        return render_template("dashboard.html", logged_in = False, errorMSG="HTTP 402 FORBIDDEN ERROR")
    if gifInformation == 404:
        return render_template("dashboard.html", logged_in = False, errorMSG = "API KEY NOT FOUND")
    if gifInformation == 405:
        return render_template("dashboard.html", logged_in = False, errorMSG="INVALID API NAME")
    
    if 'username' in session:
        return render_template("dashboard.html", logged_in = True, username = session['username'], gif=gifInformation["link"], gifTitle=gifInformation["title"])
    return render_template("dashboard.html", logged_in = False, gif=gifInformation["link"], gifTitle=gifInformation["title"])

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if DBModules.checkUser(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        
        if password == password1:
            if DBModules.registerUser(username, password):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('register'))
    return render_template("register.html")

@app.route('/view', methods = ['GET', 'POST'])
def view():
    return render_template("view.html")

@app.route('/search', methods = ['GET', 'POST'])
def search():

    foodList = APIModules.getRecipes("Chicken")

    if foodList != "RATE-LIMITED" and foodList != 403:
        return render_template("search.html", recipes=foodList)

    return render_template("search.html", errorMSG="HAHA API NO WORKY HAHAHAHAHA")

@app.route('/create', methods = ['GET', 'POST'])
def create():
    return render_template("create.html")

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    return render_template("edit.html")

@app.route('/calendar', methods = ['GET', 'POST'])
def calender():

    holidays = APIModules.getHolidays("2024")

    if holidays == 403:
        return render_template("calendar.html", errorMSG="HTTP 402 FORBIDDEN ERROR")
    if holidays == 404:
        return render_template("calendar.html", errorMSG = "API KEY NOT FOUND")
    if holidays == 405:
        return render_template("calendar.html", errorMSG="INVALID API NAME")

    return render_template("calendar.html", holidays=holidays)

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
