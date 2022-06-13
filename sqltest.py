import sqlite3

connection = sqlite3.connect('news.db')
crsr = connection.cursor()

sql = """CREATE TABLE articles (
    	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	    title TEXT,
	    link TEXT,
	    year SMALLINT,
	    month TINYINT,
	    day TINYINT,
        hour TINYINT,
        minute TINYINT,
        second TINYINT
        );"""
        
crsr.execute(f'INSERT INTO emp VALUES ({pk[i]}, "{f_name[i]}", "{l_name[i]}", "{gender[i]}", "{date[i]}")')
crsr.execute(sql)

# Must be used to save data in the database
connection.commit()
connection.close

#https://www.geeksforgeeks.org/sql-using-python/