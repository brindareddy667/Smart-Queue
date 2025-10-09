import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Load prepared dataset
df = pd.read_csv("ml_ready_dataset.csv")

# 2. Drop unnecessary text columns that can't be directly used in ML
drop_cols = ["customer_name", "staff_name", "joined_time", "served_time"]
df = df.drop(columns=[col for col in drop_cols if col in df.columns])

# 3. Encode categorical variables into numeric
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 4. Separate features and target
if "wait_time" not in df.columns:
    raise ValueError("Column 'wait_time' not found in dataset.")
X = df.drop(columns=["wait_time"])
y = df["wait_time"]

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error on test set: {mae:.2f} minutes")

# 8. Save model for later use
import joblib
joblib.dump(model, "wait_time_model.pkl")
print("✅ Model saved as wait_time_model.pkl")


