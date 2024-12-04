import sqlite3

DB_FILE = "TheChemLab"

############################# Build Database #############################

def initDB():
    db = sqlite3.connect(DB_FILE) # Open/Create database file
    c = db.cursor()
    
    c.execute("""
              CREATE TABLE IF NOT EXISTS users (
              username TEXT, 
              password TEXT
              profileImage TEXT,
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
              PRIMARY KEY(username, recipeID)
              FOREIGN KEY (username) REFERENCES users (username)
              FOREIGN KEY (recipeID) REFERENCES recipes (recipeID)
              )
              """) # creates story database
    
    db.commit() #save changes
    db.close()  #close database
