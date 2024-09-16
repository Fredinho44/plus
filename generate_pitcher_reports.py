import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load the main dataset
data = pd.read_csv('C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/filtered_pitcher_data.csv')

# Select the relevant columns
selected_columns = ['Pitcher', 'PitchType', 'AvgRelHeight', 'AvgRelSide', 'AvgRelHeight_yt', 'AvgRelSide_yt', 'shoulder_pos', 'Adj', 'arm_angle', 'PitcherTeam']
filtered_data = data[selected_columns]

# Define a color map for each pitch type
pitch_colors = {
    'Fastball': 'blue',
    'Slider': 'red',
    'Curveball': 'green',
    'Changeup': 'orange',
    'Splitter': 'purple',
    'Cutter': 'brown'
}

# Function to plot the arm angle for a pitcher, showing different pitches with different colors
def plot_pitcher_arm_angle(pitcher_name, pitcher_team, pitcher_data):
    print(f"Processing pitcher: {pitcher_name}")
    
    # Filter data for this specific pitcher
    pitcher = pitcher_data[pitcher_data['Pitcher'] == pitcher_name].copy()
    
    # Check if data is available for this pitcher
    if pitcher.empty:
        print(f"No data for {pitcher_name}")
        return

    fig, ax = plt.subplots(figsize=(8, 8))

    # Calculate average shoulder position and min/max for release points
    shoulder_pos_avg = pitcher['shoulder_pos'].mean()

    min_relheight = pitcher['AvgRelHeight_yt'].min()
    max_relheight = pitcher['AvgRelHeight_yt'].max()
    min_relside = pitcher['AvgRelSide_yt'].min()
    max_relside = pitcher['AvgRelSide_yt'].max()

    avg_relheight = pitcher['AvgRelHeight_yt'].mean()
    avg_relside = pitcher['AvgRelSide_yt'].mean()

    # Set axis limits
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 15)

    # Plot average release point (black dot)
    plt.scatter([avg_relside], [avg_relheight], s=200, lw=2, edgecolors='k', color='gray', zorder=0, label='Average Release Point')

    # Shoulder position (black dot at 0 horizontal)
    plt.scatter([0], [shoulder_pos_avg], s=125, lw=1.5, edgecolors='k', color='black', zorder=3, label='Shoulder Pos')

    # Plot each pitch type in its respective color with transparency
    for pitch_type, color in pitch_colors.items():
        pitch_data = pitcher[pitcher['PitchType'] == pitch_type]
        if not pitch_data.empty:
            plt.scatter(pitch_data['AvgRelSide_yt'], pitch_data['AvgRelHeight_yt'], s=150, lw=1.5, edgecolors='k', color=color, alpha=0.7, zorder=3, label=f'{pitch_type} Release Pos')
            # Draw line from shoulder to release point
            for i in range(len(pitch_data)):
                plt.plot([0, pitch_data['AvgRelSide_yt'].iloc[i]], [shoulder_pos_avg, pitch_data['AvgRelHeight_yt'].iloc[i]], '--', color=color, lw=1, alpha=0.5, zorder=1)

    # Add mound and rubber visuals
    mound = patches.Ellipse((0, 0), width=6, height=1, angle=0, facecolor='brown', edgecolor='black', linewidth=1, zorder=2)
    plt.gca().add_patch(mound)
    rubber = patches.Rectangle((-0.5, 0.5), width=1, height=0.25, angle=0, edgecolor='black', facecolor='white', zorder=3)
    plt.gca().add_patch(rubber)

    # Add pitcher information
    arm_angle = int(pitcher['arm_angle'].iloc[0])
    plt.text(0.5, 0.96, f"{pitcher_name} Arm Angle Plot (All Pitches)", transform=plt.gcf().transFigure, fontsize=18, color="black", weight="bold", ha="center")

    # Add a legend with the pitch types and colors
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, loc="upper right", frameon=False, title="Pitch Types")

    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')
    ax.yaxis.label.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.set_ylabel('Vertical Release (ft)')
    ax.set_xlabel('Horizontal Release (ft)')
    ax.grid(True, linestyle='--', alpha=0.25, color='lightgray')

    # Hide the top and right spines
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('black')

    # Create folder for the team if it doesn't exist
    team_folder = f'C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/{pitcher_team}'
    os.makedirs(team_folder, exist_ok=True)

    # Save the plot as a PDF in the team folder
    output_path = f'{team_folder}/{pitcher_name}_ArmAnglePlot_AllPitches.pdf'
    plt.savefig(output_path)
    plt.close()

    print(f"Saved plot for {pitcher_name} at {output_path}")

# Generate a report for each pitcher in the dataset and save in team folders
unique_pitchers = filtered_data['Pitcher'].unique()

for pitcher_name in unique_pitchers:
    # Get the team of the pitcher
    pitcher_team = filtered_data[filtered_data['Pitcher'] == pitcher_name]['PitcherTeam'].iloc[0]
    plot_pitcher_arm_angle(pitcher_name, pitcher_team, filtered_data)