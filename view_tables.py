import sqlite3
conn = sqlite3.connect("ecommerce.db")

tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
for table in tables:
    print(table[0])
