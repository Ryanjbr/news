from pygooglenews import GoogleNews
from requests_html import HTMLSession
import re
import datetime
from dateutil import parser
import sqlite3

gn = GoogleNews()

piano  = gn.search('Piano pedagogy')

connection = sqlite3.connect('../news.db')
crsr = connection.cursor()

for entry in piano['entries']:
    d = parser.parse(entry['published'])
    dtInt = d.year*100000000 +\
      d.month * 1000000 +\
      d.day * 10000 +\
      d.hour*100 +\
      d.minute
    crsr.execute("INSERT or IGNORE INTO news(title, link, date) VALUES(?, ?, ?)",
                    (entry['title'], entry['link'], dtInt))

# Must be used to save data in the database
connection.commit()
connection.close

