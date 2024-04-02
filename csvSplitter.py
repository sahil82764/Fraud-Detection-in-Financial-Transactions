import os
import pandas as pd

# Path to the original CSV file
input_file = 'Fraud.csv'

# Create the 'Data' folder if it doesn't exist
output_folder = 'Data'
os.makedirs(output_folder, exist_ok=True)

# Number of records per file
records_per_file = 100000

# Read the original CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Get the header row
header = df.columns

# Split the DataFrame into multiple DataFrames based on the number of records per file
dfs = [df[i:i+records_per_file] for i in range(0, len(df), records_per_file)]

# Save each DataFrame to a separate CSV file in the 'Data' folder
for i, df_split in enumerate(dfs):
    output_file = os.path.join(output_folder, f'output_file_{i + 1}.csv')
    df_split.to_csv(output_file, index=False, header=header)

print(f'{len(dfs)} files created in the "Data" folder.')
