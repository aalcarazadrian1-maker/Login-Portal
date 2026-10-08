import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT," 
    " Email TEXT NOT NULL UNIQUE, Password_hash TEXT NOT NULL," 
    " Role TEXT NOT NULL DEFAULT 'user')"
      )

connection.commit()
connection.close()

