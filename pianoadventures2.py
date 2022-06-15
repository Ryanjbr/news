from bs4 import BeautifulSoup as soup
import requests
import sqlite3
import datetime
from dateutil import parser
from helpers import date_to_int

connection = sqlite3.connect('news.db')
crsr = connection.cursor()

url = 'https://pianoadventures.com/blog/category/piano-pedagogy/'
html = requests.get(url)
bsobj = soup(html.content, 'lxml')
for article in bsobj.find_all("article"):
    for title in article.find_all("h1"):
        titlef = title.text
        for link in title.find_all("a"):
            linkf = link.get('href')
    for date in article.find_all("span", class_="post-date"):
        date = parser.parse(date.text)
        dtInt = date_to_int(date)
#    print(type(title), type(link), type(dtInt))
    crsr.execute("INSERT or IGNORE INTO blogs(title, link, datetime) VALUES(?, ?, ?)", (titlef, linkf, dtInt))


connection.commit()
connection.close