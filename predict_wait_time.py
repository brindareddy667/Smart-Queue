import pickle
import pandas as pd

# Load model
with open("wait_time_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define input in same order used during training
input_data = pd.DataFrame([{
    'hour_of_day': 14,
    'day_of_week': 2,
    'service_time': 5
}])

# Predict
predicted_wait = model.predict(input_data)[0]
print(f"Estimated Wait Time: {predicted_wait:.2f} minutes")

