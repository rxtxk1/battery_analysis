import os
import pandas as pd

# Function to consolidate multiple CSV files or process a single CSV file
def consolidate_csv_files(folder_or_file_path, output_file="consolidated_battery_data.csv"):
    # Initialize an empty DataFrame
    consolidated_data = pd.DataFrame()

    # Check if the input is a folder or a single file
    if os.path.isdir(folder_or_file_path):
        # List all CSV files in the folder
        csv_files = [file for file in os.listdir(folder_or_file_path) if file.endswith('.csv')]
        file_paths = [os.path.join(folder_or_file_path, file) for file in csv_files]
    elif os.path.isfile(folder_or_file_path) and folder_or_file_path.endswith('.csv'):
        file_paths = [folder_or_file_path]
    else:
        raise ValueError(f"Invalid path: {folder_or_file_path}. It must be a folder or a CSV file.")

    # Define the required columns
    required_columns = ["Cycle_Number", "Re", "Rct", "Temperature"]

    # Process each file
    for file_path in file_paths:
        try:
            # Load the CSV file
            df = pd.read_csv(file_path)

            # Add missing columns as NaN
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None

            # Filter required columns
            df = df[required_columns]

            # Add source file information
            df["File_Name"] = os.path.basename(file_path)

            # Append to the consolidated DataFrame
            consolidated_data = pd.concat([consolidated_data, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Save the consolidated dataset
    consolidated_data.to_csv(output_file, index=False)
    print(f"Consolidated data saved to {output_file}")
