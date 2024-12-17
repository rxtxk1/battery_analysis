import pandas as pd

# Function to handle missing values in the dataset
def handle_missing_values(data):
    # Replace missing values with appropriate defaults or drop them
    # Example: Fill missing numeric values with 0 or column mean
    numeric_columns = ["Cycle_Number", "Re", "Rct", "Temperature"]
    for col in numeric_columns:
        if col in data.columns:
            data[col].fillna(0, inplace=True)

    # Return the cleaned DataFrame
    print("Missing values handled.")
    return data
