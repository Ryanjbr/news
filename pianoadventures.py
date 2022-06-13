from requests_html import HTMLSession
import datetime
from dateutil import parser
import sqlite3

connection = sqlite3.connect('news.db')
crsr = connection.cursor()

session = HTMLSession()
url = 'https://pianoadventures.com/blog/category/piano-pedagogy/'
r = session.get(url)
r.html.render(sleep=1, scrolldown=5)
articles = r.html.find('article')
for item in articles:
    try:
        newsitem = item.find('h1', first=True)
        date = item.find('.post-date', first=True)
#        blurb = item.find('.entry', first=True)
        date = parser.parse(date.text)
        dtInt = d.year*100000000 +\
          d.month * 1000000 +\
          d.day * 10000 +\
          d.hour*100 +\
          d.minute
        print(newsitem.text, newsitem.absolute_links, dtInt)
        crsr.execute("INSERT or IGNORE INTO articles(title, link, datetime) VALUES(?, ?, ?)",
                        (newsitem.text, newsitem.absolute_links, dtInt))
#        'title' : newsitem.text,
#        'link' : newsitem.absolute_links,
#        'blurb' : blurb.text
    except:
        pass

connection.commit()
connection.close
