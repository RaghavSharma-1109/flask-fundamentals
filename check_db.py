import sqlite3
conn= sqlite3.connect('instance/items.db')
result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(result)
conn.close()