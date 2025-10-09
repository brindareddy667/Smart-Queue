import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Connect and load data
conn = sqlite3.connect("queue.db")
df = pd.read_sql_query("SELECT * FROM history_dataset", conn)

# Preprocess
df['joined_time'] = pd.to_datetime(df['joined_time'])
df['day_of_week'] = df['joined_time'].dt.weekday  # Monday = 0, Sunday = 6

# Features and label
X = df[['hour_of_day', 'day_of_week', 'service_time']]  # You can add more features here
y = df['wait_time']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_test, y_test)
print(f"Model R² Score: {score:.2f}")

# Save model
with open("wait_time_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved to wait_time_model.pkl")
