from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


@app.route('/')

def home():
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login():
    email = request.form["email"].strip().lower()
    password = request.form["password"].strip().lower()

    if not email or not password:
            return "Email and password are required"
  

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE Email = ?",
        (email,)
    )
    user = cursor.fetchone()

    connection.close()

    if user is None:
        return "Invalid email or password"

    stored_hash = user[2]
    if check_password_hash(stored_hash, password):
        session["user_id"] = user[0]
        session["role"] = user[3]
        
        if session["role"] == "admin":
            return redirect("/admin")
        
        return redirect("/dashboard")
    
    return "Invalid email or password"


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return "Must be logged in first"

    return render_template("dashboard.html")


@app.route("/signup")

def signup():
    return render_template("signup.html")

@app.route("/signup", methods = ["POST"])
def signup_post():
    email = request.form["email"].strip().lower()
    password = request.form["password"].strip()

    if not email or not password:
        return "Email and password are required"

    if len(password) < 8:
        return "Password must be at least 8 characters"
    
    password_hash = generate_password_hash(password)

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    try:
        cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, password_hash)
    )
        connection.commit()


    except sqlite3.IntegrityError:
        connection.close()
        return "An account with that email already exists"

    connection.close()
    return "Account Created"


@app.route("/admin")
def admin():
    if session.get("role") == "admin":  
        return render_template("admin.html")
    
    return("Access Denied")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

