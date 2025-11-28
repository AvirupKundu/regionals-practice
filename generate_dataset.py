import pandas as pd
import numpy as np
import json
import random
from helper import generate_random_data

# Load the data structure
with open('data.json', 'r') as f:
    data_structure = json.load(f)

data_points = []
for _ in range(2500):
    random_data = generate_random_data(data_structure)

    # Use actual feature names from data.json
    # Create a more meaningful relationship for the target variable
    # High current and high temperature might indicate a higher chance of failure
    if random_data.get('phase_current_IA', 0) > 500 and random_data.get('terminal_temperature_A', 0) > 60:
        random_data['target'] = 1
    else:
        random_data['target'] = 0

    # Introduce some missing values to a specific column
    if random.random() < 0.1:
        random_data['phase_current_IA'] = np.nan

    # Introduce some outliers to a specific column
    if random.random() < 0.05:
        # Ensure the key exists before creating an outlier
        if 'terminal_temperature_A' in random_data:
            random_data['terminal_temperature_A'] = random_data['terminal_temperature_A'] * 10

    data_points.append(random_data)

# Create a DataFrame and save to CSV
df = pd.DataFrame(data_points)
df.to_csv('training_data.csv', index=False)

print("Successfully generated training_data.csv with 2500 data points, including missing values and outliers.")
