import pandas as pd

# Part 1: Calculating pitcher averages by pitch type and saving it

# Define the path to the input and output CSV files for averages
input_file_path = "C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/combined.csv"
averages_output_file_path = "C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/PitcherAveragesByPitchType_New.csv"

# Function to trim all string columns in a DataFrame
def trim_dataframe_strings(df):
    # Iterate over all columns and trim strings
    for col in df.columns:
        if df[col].dtype == 'object':  # Check if column is of string type
            df[col] = df[col].str.strip()
    return df

# Load CSV file into a DataFrame and trim spaces from all string cells
data = pd.read_csv(input_file_path)
data = trim_dataframe_strings(data)

# Define the required columns with the corrected column names
required_columns = ['Pitcher', 'PitcherId', 'PitcherThrows', 'TaggedPitchType', 'PitcherTeam', 
                    'RelHeight', 'RelSide', 'yt_RelHeight', 'yt_RelSide']

# Verify that the required columns exist
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    print(f"Error: Missing columns in the input CSV: {', '.join(missing_columns)}")
else:
    # Filter the data for relevant pitch types
    valid_pitch_types = ["Fastball", "Slider", "Curveball", "Changeup", "Splitter", "Cutter"]
    filtered_data = data[data['TaggedPitchType'].isin(valid_pitch_types)]
    
    # Group the data by Pitcher, PitcherId, PitcherThrows, TaggedPitchType, and PitcherTeam
    grouped_data = filtered_data.groupby(['Pitcher', 'PitcherId', 'PitcherThrows', 'TaggedPitchType', 'PitcherTeam']).agg(
        AvgRelHeight=('RelHeight', 'mean'),
        AvgRelSide=('RelSide', 'mean'),
        AvgRelHeight_yt=('yt_RelHeight', 'mean'),
        AvgRelSide_yt=('yt_RelSide', 'mean')
    ).reset_index()

    # Check if the grouping resulted in any data
    if grouped_data.empty:
        print("No data found after grouping. Please check your input file and ensure the required fields are present.")
    else:
        # Export the new grouped data to a CSV file
        grouped_data.to_csv(averages_output_file_path, index=False)
        print(f"Pitcher averages by pitch type CSV file with trimmed playerID and PitcherTeam has been created at {averages_output_file_path}")


# Part 2: Adding height information to the calculated averages

# Define the paths to the height file and output file with height
height_file_path = "C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/FilteredPlayers_Converted.csv"
final_output_file_path = "C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/PitcherAveragesWithHeight.csv"

# Import the height data
height_data = pd.read_csv(height_file_path)

# Convert playerID to lowercase and strip spaces for both datasets
grouped_data['PitcherId'] = grouped_data['PitcherId'].str.strip().str.lower()
height_data['playerID'] = height_data['playerID'].str.strip().str.lower()

# Create a dictionary from the height data for quick lookup
height_lookup = pd.Series(height_data['ht'].values, index=height_data['playerID']).to_dict()

# Add the height information to the grouped data by matching on playerID
grouped_data['ht'] = grouped_data['PitcherId'].map(height_lookup)

# Export the updated data with the added ht column to a new CSV file
grouped_data.to_csv(final_output_file_path, index=False)

print(f"Pitcher averages with height CSV file has been created at {final_output_file_path}")
