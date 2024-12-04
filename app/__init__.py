"""
Hydronium: DuaBaig, AidanWong, QianjunZhou
SoftDev
P01: ArRESTedDevelopment
2024-01-12
Time Spent: 2
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

@app.route('/')
@app.route('/login')
@app.route('/register')
@app.route('/view')
@app.route('/search')
@app.route('/create')
@app.route('/edit')
@app.route('/calender')
@app.route('/hrecipes')
@app.route('/settings')
