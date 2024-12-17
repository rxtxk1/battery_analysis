# import os
# import pandas as pd
# from consolidate_data import consolidate_csv_files
# from visualize_data import plot_re_vs_cycle, plot_rct_vs_cycle
# from handle_missing_data import handle_missing_values

# def main():
#     # Define paths
#     input_path = r"C:\Users\ritik\OneDrive\Desktop\battery_analysis\data.csv"  # Update with folder or single file path
#     consolidated_file = r"C:\Users\ritik\OneDrive\Desktop\battery_analysis\consolidated_battery_data.csv"
    
#     # Step 1: Consolidate data
#     try:
#         print("Consolidating CSV files...")
#         consolidate_csv_files(input_path, consolidated_file)
#     except ValueError as e:
#         print(f"Error: {e}")
#         return

#     # Step 2: Load consolidated data
#     print("Loading consolidated data...")
#     try:
#         data = pd.read_csv(consolidated_file)
#     except FileNotFoundError:
#         print(f"Error: Consolidated file '{consolidated_file}' was not found.")
#         return

#     # Step 3: Handle missing data
#     print("Handling missing data...")
#     data = handle_missing_values(data)

#     # Step 4: Visualize data
#     print("Generating plots...")
#     plot_re_vs_cycle(data)
#     plot_rct_vs_cycle(data)
#     print("Plots generated successfully.")

# if __name__ == "__main__":
#     main()


import os
import pandas as pd
import plotly.graph_objects as go

# Define the directory containing your CSV files
data_folder = r'C:\Users\ritik\Downloads\archive\cleaned_dataset\data'

# Initialize lists to store the extracted data
impedance_data = []

# Loop through all CSV files in the directory
for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(data_folder, file)
        
        try:
            # Read the CSV file
            data = pd.read_csv(file_path)
            
            # Extract and process Battery_impedance column
            if "Battery_impedance" in data.columns:
                # Convert strings to complex numbers safely
                data["Battery_impedance"] = data["Battery_impedance"].apply(lambda x: complex(x) if isinstance(x, str) else x)
                
                # Compute real and imaginary parts separately
                mean_real = data["Battery_impedance"].apply(lambda x: x.real).mean()
                mean_imag = data["Battery_impedance"].apply(lambda x: x.imag).mean()
            else:
                mean_real, mean_imag = None, None  # Set defaults if column is missing
            
            # Extract Re and Rct (fallback to 0 if the columns are missing)
            Re_mean = data.get("Re", pd.Series([0])).mean()
            Rct_mean = data.get("Rct", pd.Series([0])).mean()
            
            # Extract Cycle or Time column if it exists, else use the file index
            cycle_number = data["Cycle"].iloc[0] if "Cycle" in data.columns else len(impedance_data) + 1  # Use file index if no cycle number
            
            # Append processed data to the list
            impedance_data.append({
                "filename": file,
                "Cycle": cycle_number,
                "Battery_impedance_real": mean_real,
                "Battery_impedance_imag": mean_imag,
                "Re": Re_mean,
                "Rct": Rct_mean
            })

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Convert collected data into a DataFrame
summary_df = pd.DataFrame(impedance_data)

# Drop rows with missing or invalid values for plotting
summary_df = summary_df.dropna()

# Plot Battery Impedance Real and Imaginary parts over Aging (Cycle)
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=summary_df['Cycle'], y=summary_df['Battery_impedance_real'],
                          mode='lines+markers', name='Real Part of Impedance'))
fig1.add_trace(go.Scatter(x=summary_df['Cycle'], y=summary_df['Battery_impedance_imag'],
                          mode='lines+markers', name='Imaginary Part of Impedance'))

fig1.update_layout(title="Battery Impedance (Real and Imaginary) Over Charge/Discharge Cycles",
                   xaxis_title="Cycle Number",
                   yaxis_title="Impedance (Ohms)",
                   legend_title="Components")
fig1.show()

# Plot Re (Electrolyte Resistance) and Rct (Charge Transfer Resistance) over Aging (Cycle)
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=summary_df['Cycle'], y=summary_df['Re'],
                          mode='lines+markers', name='Re: Electrolyte Resistance'))
fig2.add_trace(go.Scatter(x=summary_df['Cycle'], y=summary_df['Rct'],
                          mode='lines+markers', name='Rct: Charge Transfer Resistance'))

fig2.update_layout(title="Re and Rct Resistance Over Charge/Discharge Cycles",
                   xaxis_title="Cycle Number",
                   yaxis_title="Resistance (Ohms)",
                   legend_title="Parameters")
fig2.show()


