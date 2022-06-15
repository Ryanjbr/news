import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import null
from werkzeug.security import check_password_hash, generate_password_hash
from requests_html import HTMLSession
from pygooglenews import GoogleNews
from helpers import login_required, sql_to_dict
import sqlite3



# TODO: separate news posts and blog posts
# TODO: Customize style and css
# TODO: implement favorites functionality and create favorites page
# TODO: implement field errors for login page

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = "SELECT title, link, datetime FROM news ORDER BY datetime DESC"
        articles = sql_to_dict('news.db', QUERY)

        return render_template("index.html", articles=articles)

@app.route("/blogs")
def blogs():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = "SELECT title, link, datetime FROM blogs ORDER BY datetime DESC"
        articles = sql_to_dict('news.db', QUERY)

        return render_template("blogs.html", articles=articles)

@app.route("/favorites")
def index():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = "SELECT title, link, datetime FROM favorites ORDER BY datetime DESC"
        articles = sql_to_dict('news.db', QUERY)

        return render_template("favorites.html", articles=articles)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change password"""
    if request.method == "GET":
        # TODO: Implement HTML page
        return render_template("changepassword.html")

    else:
        # Get username from current user
        rows = db.execute("SELECT * FROM users WHERE username = ?", session["user_id"])

        # confirm current password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return apology("invalid password", 403)

        #enter new password
        if not newpassword:
            return apology("You must enter a password")
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("You must confirm your password")
    # check that password and confirmation match
        if password != confirmation:
            return apology("Passwords do not match")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # TODO: Only insert password in row of current user id
        db.execute("INSERT into users(hash) ?", hash)
        return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if get
    if request.method == "GET":
        return render_template("register.html")

    # if post (form submitted)
    else:
        connection = sqlite3.connect('news.db')
        db = connection.cursor()
        # check for errors
        # check for field left blank
        username = request.form.get("username")
        if not username:
            return render_template("register.html", usernameInput = "False")
        password = request.form.get("password")
        if not password:
            # TODO: abstract the prompt_user function to work for all of the inputs without needing to change
            return render_template("register.html", passwordInput = "False")
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return render_template("register.html", confirmationInput = "False")
    # check that password and confirmation match
        if password != confirmation:
            return render_template("register.html", passwordsMatch = "False")
    # check that username is not already taken (return apologies for all)
        if db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall():
            return render_template("register.html", uniqueUsername = "False")
        # use generate_password_hash
            # Hash the user password
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        # use db.execute to insert user, using ? to insert yet unknown values
        # TODO: not working
        db.execute("INSERT into users(username, hash) VALUES(?, ?)", (username, hash))
        connection.commit()
        QUERY = "SELECT * FROM users WHERE username=" + "'" + request.form.get("username") + "'"
        rows = sql_to_dict('news.db', QUERY)
        print(rows)
        session["user_id"] = rows[0]["id"]
        connection.close()
        return redirect("/")

