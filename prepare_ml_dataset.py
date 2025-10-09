import sqlite3
import pandas as pd

# Connect to your existing database
conn = sqlite3.connect("queue.db")

# Load data from history_dataset
df = pd.read_sql_query("SELECT * FROM history_dataset", conn)
conn.close()

# Convert datetime columns (adjust names to your table)
df['joined_time'] = pd.to_datetime(df['joined_time'])
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Feature engineering
df['day_of_week'] = df['joined_time'].dt.day_name()
df['hour_of_day'] = df['joined_time'].dt.hour
df['wait_time_minutes'] = (df['start_time'] - df['joined_time']).dt.total_seconds() / 60
df['service_time_minutes'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60

# Weekend flag (1 if Saturday or Sunday)
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)

# Peak hour flag (define your own busy hours, here 11am-2pm and 5pm-7pm)
df['is_peak_hour'] = df['hour_of_day'].isin([11, 12, 13, 17, 18, 19]).astype(int)

# Optional: drop any rows with missing values
df = df.dropna()

# Save to CSV for ML
df.to_csv("ml_ready_dataset.csv", index=False)

# Preview first 5 rows
print("ML-ready dataset saved as ml_ready_dataset.csv")
print(df.head())


