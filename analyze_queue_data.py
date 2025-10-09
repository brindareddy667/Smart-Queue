import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
sns.set(style="whitegrid")
conn = sqlite3.connect("queue.db")

# Load data
df = pd.read_sql_query("SELECT * FROM history_dataset", conn)

# Convert datetime columns
df['joined_time'] = pd.to_datetime(df['joined_time'])
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Derived columns
df['day_name'] = df['joined_time'].dt.day_name()
df['is_lunch_break'] = df['hour_of_day'].apply(lambda h: 1 if h == 13 else 0)

# Sort weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['day_name'] = pd.Categorical(df['day_name'], categories=weekday_order, ordered=True)

# Plot: Average Wait Time per Day
plt.figure(figsize=(8, 5))
sns.barplot(x="day_name", y="wait_time", data=df, estimator='mean')
plt.title("Average Wait Time per Day")
plt.ylabel("Minutes")
plt.xlabel("Day")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot: Average Service Time per Day
plt.figure(figsize=(8, 5))
sns.barplot(x="day_name", y="service_time", data=df, estimator='mean', color='skyblue')
plt.title("Average Service Time per Day")
plt.ylabel("Minutes")
plt.xlabel("Day")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot: Record Count by Hour with 1PM marked as Lunch Break
plt.figure(figsize=(10, 5))
ax = sns.countplot(
    x="hour_of_day", data=df, palette="crest",
    order=list(range(8, 18))  # Ensure all hours 8 to 17 are shown, including 13
)
plt.title("Queue Records by Hour of Day ")
plt.xlabel("Hour")
plt.ylabel("Record Count")

# Rename x-axis label 13 to '13 (Lunch)'
ax.set_xticklabels([
    f"{label.get_text()} (Lunch)" if label.get_text() == "13" else label.get_text()
    for label in ax.get_xticklabels()
])

plt.tight_layout()
plt.show()

# Plot: Status Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x="status", data=df, palette="Set2")
plt.title("Status Distribution")
plt.xlabel("Status")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Plot: Peak Hours Heatmap
pivot = df.pivot_table(index='day_name', columns='hour_of_day', values='id', aggfunc='count').fillna(0)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot.loc[weekday_order], annot=True, fmt='.0f', cmap='YlOrRd')
plt.title(" Queue Volume Heatmap (Day vs Hour)")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.show()

# Print summary stats
print("Average Wait Time by Day:")
print(df.groupby('day_name')['wait_time'].mean().round(2))

print("Average Service Time by Day:")
print(df.groupby('day_name')['service_time'].mean().round(2))

print("Status Counts:")
print(df['status'].value_counts())
