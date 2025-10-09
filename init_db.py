import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('queue.db')
cursor = conn.cursor()

# Create table for current queue
cursor.execute('''
    CREATE TABLE IF NOT EXISTS queue_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        joined_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create table for exited people
cursor.execute('''
    CREATE TABLE IF NOT EXISTS queue_exited (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        exited_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("✅ Database and tables created successfully!")
