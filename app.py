from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return redirect("/login")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Hash password
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            flash("Registration Successful!")
            return redirect("/login")

        except:
            flash("Username already exists!")

    return render_template("register.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        # Check password
        if user and check_password_hash(user[2], password):

            session["user"] = username
            return redirect("/dashboard")

        else:
            flash("Invalid Username or Password")

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" in session:
        return render_template("dashboard.html", user=session["user"])

    return redirect("/login")

# Logout
@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/login")

# Run app
if __name__ == "__main__":
    app.run(debug=True)