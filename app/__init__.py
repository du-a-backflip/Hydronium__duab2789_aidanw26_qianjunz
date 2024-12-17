"""
Hydronium: DuaBaig, AidanWong, QianjunZhou
SoftDev
P01: ArRESTedDevelopment
2024-01-12
Time Spent: 2
"""

from dataclasses import dataclass
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import calendar
import datetime

calendarDates = {}
for i in range(1,13):
    calendarDates[i]=calendar.monthcalendar(2024,i)
from customModules import APIModules, DBModules

app = Flask(__name__)

app.secret_key = os.urandom(32)

DBModules.initDB()

@app.route('/', methods = ['GET', 'POST'])
def dashboard():
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

@app.route('/search/<queryS>', methods = ['GET', 'POST'])
def search(queryS):

    if not queryS:
        return render_template("search.html", errorMSG="No search query provided.")

    foodList = APIModules.getRecipes(queryS)

    if foodList == "RATE-LIMITED":
        return render_template("search.html", errorMSG="API rate limit reached.")
    if foodList == 403:
        return render_template("search.html", errorMSG="API not accessible. (HTTP 403)")

    if request.method == 'POST':
        query = request.form.get("query")
        if query:
            return redirect(url_for('search', queryS=query))

    return render_template("search.html", recipes=foodList, query=queryS)

@app.route('/search/<queryS>/<recipeID>', methods = ['GET', 'POST'])
def view(queryS, recipeID):

    recipeInformation = APIModules.getRecipeInformation(recipeID)

    recipeGif = APIModules.getGif(recipeInformation[0]["title"])

    if recipeGif == 403:
        return render_template("view.html", errorMSG="HTTP 402 FORBIDDEN ERROR")
    if recipeGif == 404:
        return render_template("view.html", errorMSG = "API KEY NOT FOUND")
    if recipeGif == 405:
        return render_template("view.html",  errorMSG="INVALID API NAME")


    return render_template("view.html", recipeInformation=recipeInformation, recipeGif=recipeGif['link'])

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


currDate = datetime.datetime.now()
month = currDate.month
year = currDate.year

@app.route('/calendar', methods = ['GET', 'POST'])
def Calendar():
    if request.method == 'POST':
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        if month == 0 or year == 0:
            if month == 0:
                month = currDate.month
            if year == 0:
                year = currDate.year
    else:
        month = currDate.month 
        year = currDate.year

    data = APIModules.getHolidays(str(year))
    if data == 403:
        return render_template("calendar.html", errorMSG="HTTP 402 FORBIDDEN ERROR")
    if data == 404:
        return render_template("calendar.html", errorMSG = "API KEY NOT FOUND")
    if data == 405:
        return render_template("calendar.html", errorMSG="INVALID API NAME")

    cal = fullCalendar(year, month, data)
    print(cal)
    return render_template("calendar.html", calen = cal, month = month, year = year)

def fullCalendar(year, month, data):
    cal = calendar.monthcalendar(year, month)
    for i in range(len(cal)):
        for j in range(len(cal[i])):
            cal[i][j] = [cal[i][j]]
            for k in range(len(data)):
                holidate = data[k]['date'].split("-")
                #print(cal[i][j])
                if (int(holidate[1]) == month and int(holidate[2][:2]) == cal[i][j][0]):
                    if (data[k]['name'] not in cal[i][j]):
                        cal[i][j].append(data[k])
                        #print(cal[i][j])
    return cal
    '''
    countneg = -1
    actualDates = {}
    for i in calendarDates:
        actualDates[i] = {}
        for k in range(len(calendarDates[i])):
            actualDates[i][k]={}
            #print(calendarDates[i][k])
            for j in calendarDates[i][k]:
                #print(j)
                if (j == 0):
                    actualDates[i][k][countneg]={}
                    countneg -= 1
                else:
                    actualDates[i][k][j]={}
    #print(actualDates)
    for i in range(len(data)):
        findValue = data[i]['date'][5:10]
        monthOf = findValue[0:2]
        for k in actualDates[int(monthOf)]:
            #print(actualDates[int(monthOf)][k])
            for j in actualDates[int(monthOf)][k]:
                if (j == int(findValue[3:])):
                    actualDates[int(monthOf)][k][j]=data[i]
    
    print(actualDates)
    

    if 'username' in session:
        return render_template("calendar.html", holidays=actualDates, logged_in=True, username = session['username'])

    return render_template("calendar.html", holidays=actualDates, logged_in=False)
    '''

@app.route('/calData/<name>', methods = ['GET', 'POST'])
def calDataName(name):
    print(year)
    data = APIModules.getHolidays(str(year))
    if data == 403:
        return render_template("calData.html", errorMSG="HTTP 402 FORBIDDEN ERROR")
    if data == 404:
        return render_template("calData.html", errorMSG = "API KEY NOT FOUND")
    if data == 405:
        return render_template("calData.html", errorMSG="INVALID API NAME")

    holidayGif = APIModules.getGif(name)

    if holidayGif == 403:
        return render_template("calData.html", errorMSG="HTTP 402 FORBIDDEN ERROR")
    if holidayGif == 404:
        return render_template("calData.html", errorMSG = "API KEY NOT FOUND")
    if holidayGif == 405:
        return render_template("calData.html",  errorMSG="INVALID API NAME")

    if 'username' in session:
        return render_template("calData.html", name = name, data=data, logged_in=True, username = session['username'], holidayGif = holidayGif["link"])


    return render_template("calData.html", name = name, data=data, logged_in=False, holidayGif = holidayGif["link"])

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
