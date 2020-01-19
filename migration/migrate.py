import sqlite3

conn = sqlite3.connect('./database.sqlite')
conn.row_factory = lambda c, r: dict(sqlite3.Row(c, r))
cur = conn.cursor()

cur.execute('SELECT username, first_name, last_name, email, points FROM User;')
users = cur.fetchall()
cur.close()
conn.close()

print(users[:5])
