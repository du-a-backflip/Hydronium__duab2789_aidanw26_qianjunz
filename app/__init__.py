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
def home():
    return "Welcome to the home page"

"""
@app.route('/login')
@app.route('/register')
@app.route('/view')
@app.route('/search')
@app.route('/create')
@app.route('/edit')
@app.route('/calender')
@app.route('/hrecipes')
@app.route('/settings')
"""

if __name__ == "__main__":
    app.debug = True
    app.run()