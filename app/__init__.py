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

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/view')
@app.route('/search')
@app.route('/create')
@app.route('/edit')
@app.route('/calender')
@app.route('/hrecipes')
@app.route('/settings')
@app.route('/logout')


if __name__ == "__main__":
    app.debug = True
    app.run()
