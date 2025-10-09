import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite
conn = sqlite3.connect('queue.db')
cursor = conn.cursor()

# Drop old table
cursor.execute("DROP TABLE IF EXISTS history_dataset")
print("🗑️ Dropped old 'history_dataset' table.")

# Create new table (no user_id)
cursor.execute("""
CREATE TABLE history_dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    joined_time TEXT,
    start_time TEXT,
    end_time TEXT,
    status TEXT,
    wait_time INTEGER,
    service_time INTEGER,
    day_of_week INTEGER,
    hour_of_day INTEGER
)
""")
print("🆕 Created new 'history_dataset' table without user_id.")

# Name generation
first_names = ['Alex', 'Jordan', 'Taylor', 'Riley', 'Casey', 'Morgan', 'Sam', 'Jamie', 'Drew', 'Chris']
last_names = ['Smith', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Clark', 'Lewis', 'Hall']

# Insert mock records
total_days = 30
records_per_day = 15
statuses = ['completed', 'cancelled', 'missed']

for day in range(total_days):
    date = datetime.now() - timedelta(days=day)

    for _ in range(records_per_day):
        joined = date.replace(
            hour=random.choice([8, 9, 10, 11, 12, 14, 15, 16, 17]),  # skips 13 (1 PM)
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        start = joined + timedelta(minutes=random.randint(1, 10))
        end = start + timedelta(minutes=random.randint(2, 15))

        wait_time = int((start - joined).total_seconds() / 60)
        service_time = int((end - start).total_seconds() / 60)
        day_of_week = joined.weekday()
        hour_of_day = joined.hour
        status = random.choice(statuses)
        user_name = f"{random.choice(first_names)} {random.choice(last_names)}"

        joined_str = joined.strftime('%Y-%m-%d %H:%M:%S')
        start_str = start.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO history_dataset (
                user_name, joined_time, start_time, end_time, status,
                wait_time, service_time, day_of_week, hour_of_day
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_name, joined_str, start_str, end_str, status,
            wait_time, service_time, day_of_week, hour_of_day
        ))

# Save & close
conn.commit()
conn.close()
print(f"✅ Inserted {total_days * records_per_day} records with user names (no user_id).")
