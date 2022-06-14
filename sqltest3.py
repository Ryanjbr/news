import sqlite3

db.execute("INSERT into users(username, hash) VALUES(?, ?)", (username, hash))