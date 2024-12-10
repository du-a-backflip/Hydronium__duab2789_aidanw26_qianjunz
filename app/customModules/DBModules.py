import sqlite3

DB_FILE = "TheChemLab"

############################# Build Database #############################

def initDB():
    db = sqlite3.connect(DB_FILE) # Open/Create database file
    c = db.cursor()
    
    c.execute("""
              CREATE TABLE IF NOT EXISTS users (
              username TEXT, 
              password TEXT,
              profileImage TEXT
              )
              """) # creates login database
    c.execute("""
              CREATE TABLE IF NOT EXISTS recipes (
              recipeID INTEGER, 
              recipeName TEXT, 
              recipeData TEXT,
              userStatus INTEGER, 
              PRIMARY KEY(recipeID, recipeName)
              )
              """) # creates story database
    c.execute("""
              CREATE TABLE IF NOT EXISTS favRecipes (
              username TEXT, 
              recipeID INTEGER,
              PRIMARY KEY(username, recipeID),
              FOREIGN KEY (username) REFERENCES users (username),
              FOREIGN KEY (recipeID) REFERENCES recipes (recipeID)
              )
              """) # creates story database
    
    db.commit() #save changes
    db.close()  #close database

############################# User Database Interations #############################

def addUser(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    c.execute(query, (username, password))
    db.commit()
    db.close()

def checkUser(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username, )) # Passing username as a single element tuple
    user = c.fetchone() # Checks to see if any rows were returned
    if user is not None:
        if password == user[1]:
            return True
    return False

def registerUser(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username, )) # Passing username as a single element tuple
    user = c.fetchone() # Checks to see if any rows were returned
    if user is None:
        addUser(username, password)
        return True
    return False