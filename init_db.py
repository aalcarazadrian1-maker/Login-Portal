import sqlite3

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT," 
    " Email TEXT NOT NULL UNIQUE, Password_hash TEXT NOT NULL," 
    " Role TEXT NOT NULL DEFAULT 'user')"
      )

cursor.execute(
    "CREATE TABLE IF NOT EXISTS private_data"
    " (ID INTEGER PRIMARY KEY AUTOINCREMENT," 
    "user_id INTEGER NOT NULL, private_text TEXT)"
)


connection.commit()
connection.close()

