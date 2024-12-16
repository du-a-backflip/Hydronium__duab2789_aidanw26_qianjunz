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
    """
    gifInformation = APIModules.getGif("Troll")
    if gifInformation == 403:
        return render_template("dashboard.html", logged_in = False, errorMSG="HTTP 402 FORBIDDEN ERROR")
    if gifInformation == 404:
        return render_template("dashboard.html", logged_in = False, errorMSG = "API KEY NOT FOUND")
    if gifInformation == 405:
        return render_template("dashboard.html", logged_in = False, errorMSG="INVALID API NAME")
    """

    if request.method == 'POST':
        query = request.form.get("query")
        if query:
            return redirect(url_for('search', queryS=query))

    if 'username' in session:
        return render_template("dashboard.html", logged_in = True, username = session['username'])
    return render_template("dashboard.html", logged_in = False)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if DBModules.checkUser(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('dashboard'))
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

@app.route('/search/<queryS>', methods = ['GET', 'POST'])
def search(queryS):

    if not queryS:
        return render_template("search.html", errorMSG="No search query provided.")
    
    foodList = APIModules.getRecipes(queryS)

    if foodList == "RATE-LIMITED":
        return render_template("search.html", errorMSG="API rate limit reached.")
    if foodList == 403:
        return render_template("search.html", errorMSG="API not accessible. (HTTP 403)")

    return render_template("search.html", recipes=foodList, query=queryS)

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if 'username' in session:
        return render_template("create.html")
    return redirect(url_for('dashboard'))

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    if 'username' in session:
        return render_template("edit.html")
    return redirect(url_for('dashboard'))

@app.route('/calendar', methods = ['GET', 'POST'])
def calendar():

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
    if 'username' not in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = session['username']
        new_username = request.form.get('username')
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        errormsgs = []

        if new_username:
            if not DBModules.changeUser(username, new_username, current_password):
                errormsgs.append("Username Change Failed: Current Password Incorrect/Not Provided")
            else:
                flash("Username changed to " + new_username)
                session['username'] = new_username
                username = session['username']

        print(current_password)
        
        if new_password:
            if new_password != confirm_password:
                errormsgs.append("New passwords do not match")
            if not DBModules.changePassword(username, current_password, new_password):
                errormsgs.append("Password update failed: Current password incorrect or not provided")
            else:
                flash("Password sucessfully changed")

        if errormsgs:
            return render_template("settings.html", logged_in=True, username=session['username'], errorMsg = "; ".join(errormsgs))
    
    return render_template("settings.html", logged_in=True, username=session['username'])



    

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('dashboard'))

@app.route("/holiday_redirect")
def holidayRedirect():
    query = request.args.get('query')

    return redirect(APIModules.getFirstLink(query))


if __name__ == "__main__":
    app.debug = True
    app.run()
