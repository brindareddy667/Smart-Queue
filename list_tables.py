import sqlite3

db_path = "/Users/sahithreddy/Downloads/smartqueue/queue.db"
conn = sqlite3.connect(db_path)

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in DB:", [t[0] for t in tables])

