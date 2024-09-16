import pandas as pd

# Define the file paths for input and output CSV files
input_file_path = r"C:\Users\AlfredoCaraballo\OneDrive - DSSports\Desktop\Arm Angle\collegePlayerKeys 1.csv"
output_file_path = r"C:\Users\AlfredoCaraballo\OneDrive - DSSports\Desktop\Arm Angle\FilteredPlayers.csv"
converted_output_file_path = r"C:\Users\AlfredoCaraballo\OneDrive - DSSports\Desktop\Arm Angle\FilteredPlayers_Converted.csv"
output_file1 = r"C:\Users\AlfredoCaraballo\OneDrive - DSSports\Desktop\Arm Angle\FilteredPlayers_Cleaned.csv"
output_file2 = r"C:\Users\AlfredoCaraballo\OneDrive - DSSports\Desktop\Arm Angle\FilteredPlayers_Converted_Cleaned.csv"

# Function to clean the dataset
def clean_data(df):
    # Ensure 'ht' column is numeric (for height conversion if necessary)
    df['ht'] = pd.to_numeric(df['ht'], errors='coerce')

    # Trim spaces in all string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Remove leading/trailing spaces in 'playerID'
    df['playerID'] = df['playerID'].str.replace(" ", "")

    return df

# Step 1: Import the CSV file
data = pd.read_csv(input_file_path)

# Step 2: Select the correct columns
filtered_data = data[['playerID', 'first', 'last', 'teamID', 'throws', 'ht']]

# Step 3: Export the selected columns to a new CSV file
filtered_data.to_csv(output_file_path, index=False)
print(f"Filtered CSV file has been created at {output_file_path}")

# Step 4: Check if 'ht' column exists and convert to feet (dividing by 12 if it's in inches)
if 'ht' in filtered_data.columns:
    print("ht column found")
    print(filtered_data['ht'].head())
    
    # Convert 'ht' column to numeric and divide by 12 (assuming it's in inches)
    filtered_data['ht'] = pd.to_numeric(filtered_data['ht'], errors='coerce') / 12
    
    # Step 5: Save the modified data to a new CSV file
    try:
        filtered_data.to_csv(converted_output_file_path, index=False)
        print(f"Converted CSV file has been created at {converted_output_file_path}")
    except Exception as e:
        print(f"Error writing the file: {e}")
else:
    print("Error: ht column not found in the dataset")

# Step 6: Load and clean the first CSV (FilteredPlayers.csv)
data1 = pd.read_csv(output_file_path)
data1 = clean_data(data1)

# Step 7: Save the cleaned data to a new CSV file
data1.to_csv(output_file1, index=False)
print(f"Cleaned data saved to {output_file1}")

# Step 8: Load and clean the second CSV (FilteredPlayers_Converted.csv)
data2 = pd.read_csv(converted_output_file_path)
data2 = clean_data(data2)

# Step 9: Save the cleaned data to a new CSV file
data2.to_csv(output_file2, index=False)
print(f"Cleaned data saved to {output_file2}")

print("Both CSV files have been cleaned and saved.")
