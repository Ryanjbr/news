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


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = "SELECT id, title, link, date FROM news ORDER BY date DESC"
        articles = sql_to_dict('news.db', QUERY)

        return render_template("index.html", articles=articles)
    
    if request.method == "POST":
        connection = sqlite3.connect('news.db')
        db = connection.cursor()
        newsId = request.form['favorite']
        date = db.execute("SELECT date FROM news WHERE id = ?", (newsId,)).fetchone()[0]
        print(newsId, date, session["user_id"])
        db.execute("INSERT INTO favorites(newsid, date, userid) VALUES(?, ?, ?)", (newsId, date, session["user_id"]))
        connection.commit()
        connection.close
        return redirect("/")

@app.route("/blogs")
def blogs():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = "SELECT id, title, link, date FROM blogs ORDER BY date DESC"
        articles = sql_to_dict('news.db', QUERY)

        return render_template("blogs.html", articles=articles)
    
    if request.method == "POST":
        connection = sqlite3.connect('news.db')
        db = connection.cursor()
        blogsId = request.form['favorite']
        date = db.execute("SELECT date FROM blogs WHERE id = ?", (newsId,)).fetchone()[0]
        db.execute("INSERT INTO favorites(blogsid, date, userid) VALUES(?, ?, ?)", (newsId, date, session["user_id"]))
        connection.commit()
        connection.close
        return redirect("/blogs")

@app.route("/favorites")
def favorites():
    if request.method == "GET":
        # populates a dict with articles title, link and date from DB
        QUERY = ("SELECT newsid, blogsid, date FROM favorites WHERE userid="+'"'+str(session["user_id"])+'"')
        print(QUERY)
        ids = sql_to_dict('news.db', QUERY)
        print(ids)
        articles = []
        for id in ids:
            if id["newsid"]:
                QUERY = ("SELECT title, link, date FROM news WHERE id="+'"'+str(id["newsid"])+'"')
                articles.append(sql_to_dict('news.db', QUERY)[0])
            if id["blogsid"]:
                QUERY = ("SELECT title, link, date FROM blogs WHERE id="+'"'+str(id["blogsid"])+'"')
                articles.append(sql_to_dict('news.db', QUERY)[0])
            else:
                pass
        print(articles)

        return render_template("favorites.html", articles=articles)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return render_template("login.html", usernameInput = "False")

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return render_template("login.html", passwordInput = "False")

        # Query database for username
        QUERY = "SELECT * FROM users WHERE username=" + "'" + request.form.get("username") + "'"
        rows = sql_to_dict('news.db', QUERY)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", inputCorrect = "False")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change password"""
    if request.method == "GET":
        # displays form
        return render_template("changepassword.html")

    else:
        # enter old password
        connection = sqlite3.connect('news.db')
        db = connection.cursor()
        oldPassword = request.form.get("oldPassword")
        if not oldPassword:
            return render_template("changepassword.html", oldPasswordInput = "False")
        # Get username from current user
        QUERY = "SELECT * FROM users WHERE id=" + "'" + str(session["user_id"]) + "'"
        rows = sql_to_dict('news.db', QUERY)
        # Check current password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], oldPassword):
            return render_template("changepassword.html", inputCorrect = "False")
        # enter new password
        newPassword = request.form.get("newPassword")
        if not newPassword:
            return render_template("changepassword.html", newPasswordInput = "False")
        # confirm password
        confirmation = request.form.get("confirmation")
        if not confirmation:
            return render_template("changepassword.html", confirmationInput = "False")
        # check that password and confirmation match
        if newPassword != confirmation:
            return render_template("changepassword.html", passwordsMatch = "False")
        hash = generate_password_hash(newPassword, method='pbkdf2:sha256', salt_length=8)
        # update hash with new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", (hash, session["user_id"]))
        connection.commit()
        connection.close
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
        db.execute("INSERT into users(username, hash) VALUES(?, ?)", (username, hash))
        connection.commit()
        QUERY = "SELECT * FROM users WHERE username=" + "'" + request.form.get("username") + "'"
        rows = sql_to_dict('news.db', QUERY)
        session["user_id"] = rows[0]["id"]
        connection.close()
        return redirect("/")

