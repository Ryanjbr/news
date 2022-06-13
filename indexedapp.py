import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from requests_html import HTMLSession


# TODO: Watch videos on asyncio and try to implement
# TODO: figure out how to order articles by date order
# TODO: create registration and login forms
# TODO: Customize style and css
# TODO: Go back to finance and get login required from helpers

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
        session = HTMLSession()
        url = 'https://pianoadventures.com/blog/category/piano-pedagogy/'
        r = session.get(url)
        r.html.render(sleep=1, scrolldown=5)
        articles = r.html.find('article')
        newslist = []
        for item in articles:
            try:
                newsitem = item.find('h1', first=True)
                date = item.find('.post-date', first=True)
                blurb = item.find('.entry', first=True)
                newsarticle = {
                'title' : newsitem.text,
                'link' : newsitem.absolute_links,
                'date' : date.text,
                'blurb' : blurb.text
                }
                newslist.append(newsarticle)
            except:
                pass
        render_template("index.html", newslist=newslist)