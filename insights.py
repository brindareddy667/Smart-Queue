# insights.py
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("queue.db")

# Load history dataset
df = pd.read_sql_query("SELECT * FROM history_dataset", conn)

# Make sure datetime columns are parsed
datetime_cols = ["joined_time", "start_time", "end_time"]
for col in datetime_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col])

# Extract time features
df["day_of_week"] = df["joined_time"].dt.day_name()
df["hour_of_day"] = df["joined_time"].dt.hour

# Average wait and service times
avg_wait = df["wait_time"].mean().round(1)
avg_service = df["service_time"].mean().round(1)

# Busiest day
busiest_day = (
    df["day_of_week"].value_counts().idxmax()
)
busiest_day_count = df["day_of_week"].value_counts().max()

# Quietest day
quietest_day = (
    df["day_of_week"].value_counts().idxmin()
)
quietest_day_count = df["day_of_week"].value_counts().min()

# Peak hour overall
peak_hour = (
    df["hour_of_day"].value_counts().idxmax()
)
peak_hour_count = df["hour_of_day"].value_counts().max()

# Specific busiest hour per weekday
busiest_by_day = (
    df.groupby(["day_of_week", "hour_of_day"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
    .iloc[0]
)

# Output Insights
print("\n=== Queue Insights (Last 30 Days) ===\n")
print(f"📌 Average wait time: {avg_wait} minutes")
print(f"📌 Average service time: {avg_service} minutes")
print(f"📌 Busiest day overall: {busiest_day} ({busiest_day_count} records)")
print(f"📌 Quietest day overall: {quietest_day} ({quietest_day_count} records)")
print(f"📌 Peak hour overall: {peak_hour}:00 ({peak_hour_count} records)")
print(
    f"📌 Busiest single period: {busiest_by_day['day_of_week']} at {int(busiest_by_day['hour_of_day'])}:00 "
    f"({int(busiest_by_day['count'])} records)"
)

# Status breakdown
status_counts = df["status"].value_counts()
print("\n📊 Status breakdown:")
for status, count in status_counts.items():
    print(f"   - {status}: {count}")

print("\n✅ Insights generated successfully.\n")
