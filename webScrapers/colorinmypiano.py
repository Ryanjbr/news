from bs4 import BeautifulSoup as soup
import requests
import sqlite3
import datetime
from dateutil import parser
from helpers import date_to_int

connection = sqlite3.connect('../news.db')
crsr = connection.cursor()

url = 'https://colorinmypiano.com/'
html = requests.get(url)
bsobj = soup(html.content, 'lxml')
for article in bsobj.find_all("article"):
    for title in article.find_all("h2"):
        titlef = title.text
        for link in title.find_all("a"):
            linkf = link.get('href')
    for date in article.find_all("time", class_="entry-date published updated"):
        date = parser.parse(date.text)
        dtInt = date_to_int(date)
    print(titlef, linkf, dtInt)
    crsr.execute("INSERT or IGNORE INTO blogs(title, link, date) VALUES(?, ?, ?)", (titlef, linkf, dtInt))


connection.commit()
connection.close