import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect("queue.db")   # <-- change if your DB file name differs
df = pd.read_sql_query("SELECT * FROM history_dataset", conn)
conn.close()

# --- Compute insights ---
insights = {}

# 1 & 2: Busiest / Quietest day by avg wait
day_waits = df.groupby("day_of_week")["wait_time"].mean()
insights["busiest_day"] = int(day_waits.idxmax())
insights["quietest_day"] = int(day_waits.idxmin())

# 3: Peak wait hour
hour_waits = df.groupby("hour_of_day")["wait_time"].mean()
insights["peak_hour"] = int(hour_waits.idxmax())

# 4: Average wait
insights["avg_wait_time"] = round(df["wait_time"].mean(), 2)

# 5: Longest wait
insights["longest_wait"] = int(df["wait_time"].max())

# 6: Shortest wait
insights["shortest_wait"] = int(df["wait_time"].min())

# 7: % waiting > 15 min
insights["pct_over_15"] = round((df[df["wait_time"] > 15].shape[0] / len(df)) * 100, 2)

# 8: Day with most customers
insights["most_customers_day"] = int(df["day_of_week"].value_counts().idxmax())

# --- Print results ---
print("\n📊 KEY INSIGHTS 📊\n")
print(f"1️⃣ Busiest day (highest avg wait): {insights['busiest_day']}")
print(f"2️⃣ Quietest day (lowest avg wait): {insights['quietest_day']}")
print(f"3️⃣ Peak wait hour: {insights['peak_hour']}:00")
print(f"4️⃣ Average wait time: {insights['avg_wait_time']} minutes")
print(f"5️⃣ Longest recorded wait: {insights['longest_wait']} minutes")
print(f"6️⃣ Shortest recorded wait: {insights['shortest_wait']} minutes")
print(f"7️⃣ % of customers waiting >15 min: {insights['pct_over_15']}%")
print(f"8️⃣ Day with most customers: {insights['most_customers_day']}")

