import pandas as pd

# Define the file paths
input_file_path = '/Users/phamthiphuongthuy/Desktop/Intern/server_log/data/parsed_log/kong-logs-acesss.2024-12-15T00_00_00.000Z-2024-12-15T00_15_00.000Z'
output_file_path = '/Users/phamthiphuongthuy/Desktop/Intern/server_log/grouped_logs_20s.csv'

# Read the log data
log_df = pd.read_csv(input_file_path)

# Convert the 'datetime' column to a pandas datetime object
log_df['datetime'] = pd.to_datetime(log_df['datetime'], format='%d/%b/%Y:%H:%M:%S +0000')

# Set the 'datetime' column as the index
log_df.set_index('datetime', inplace=True)

# Resample the data to 20-second intervals and aggregate
grouped_df = log_df.resample('20S').sum()

# Reset the index to make 'datetime' a column again
grouped_df.reset_index(inplace=True)

# Save the grouped data to a new CSV file
grouped_df.to_csv(output_file_path, index=False)

print(f"Grouped logs have been saved to {output_file_path}")