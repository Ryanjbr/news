from bs4 import BeautifulSoup as soup
import requests
import sqlite3
import datetime
from dateutil import parser
from helpers import date_to_int

connection = sqlite3.connect('../news.db')
crsr = connection.cursor()

url = 'https://musicmattersblog.com/'
html = requests.get(url)
bsobj = soup(html.content, 'lxml')
for article in bsobj.find_all("ul"):
    for title in article.find_all("li"):
        titlef = title.text
        for link in title.find_all("a"):
            linkf = link.get('href')
    for date in article.find_all("time", class_="wp-block-latest-posts__post-date"):
        date = parser.parse(date.text)
        dtInt = date_to_int(date)
    print(titlef, linkf, dtInt)


connection.commit()
connection.close