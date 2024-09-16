import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import matplotlib.patches as patches

# Load necessary data
data = pd.read_csv('C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/filtered_pitcher_data.csv')

# Select the relevant columns
selected_columns = ['Pitcher', 'PitchType', 'AvgRelheight', 'AvgRelside', 'AvgYT_Relheight', 'AvgYT_Relside', 'shoulder_pos', 'Adj', 'arm_angle', 'PitcherTeam']
filtered_data = data[selected_columns]

# Function to generate team average report PDF with the graph on the second page
def generate_team_avg_report(team_name, team_data):
    # Create a new PDF for each team
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add the first page with team data
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f'Team Report: {team_name}', ln=True, align='C')
    
    # Column names
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Pitcher', 1)
    pdf.cell(40, 10, 'Avg RelHeight', 1)
    pdf.cell(40, 10, 'Avg RelSide', 1)
    pdf.cell(40, 10, 'Arm Angle', 1)
    pdf.ln()
    
    # Pitcher averages and plotting (without the graph for now)
    pdf.set_font('Arial', '', 12)
    
    for pitcher_name, pitcher_data in team_data.groupby('Pitcher'):
        avg_relheight = pitcher_data['AvgYT_Relheight'].mean()
        avg_relside = pitcher_data['AvgYT_Relside'].mean()
        avg_arm_angle = pitcher_data['arm_angle'].mean()
        
        # Write pitcher averages to the PDF
        pdf.cell(50, 10, pitcher_name, 1)
        pdf.cell(40, 10, f'{avg_relheight:.2f}', 1)
        pdf.cell(40, 10, f'{avg_relside:.2f}', 1)
        pdf.cell(40, 10, f'{avg_arm_angle:.2f}', 1)
        pdf.ln()

    # Create and save the graph
    plot_team_graph(team_name, team_data)

    # Add the second page for the graph
    pdf.add_page()

    # Insert the graph on the second page
    plot_path = f'C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/{team_name}/{team_name}_Pitcher_Averages.png'
    if os.path.exists(plot_path):  # Check if the plot was saved successfully
        pdf.image(plot_path, x=10, y=10, w=190)  # Adjust `x` and `y` for positioning
    else:
        print(f"Error: Plot image for {team_name} not found.")
    
    # Save the PDF for this team
    output_path = f'C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/{team_name}/{team_name}_Pitcher_Averages_Report.pdf'
    pdf.output(output_path)
    print(f'Team average report saved for {team_name} at {output_path}')

# Function to plot a team's graph and save as a PNG
def plot_team_graph(team_name, team_data):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 15)

    # Set team-specific color
    color = get_team_color(team_name)

    # Plot data for each pitcher
    for pitcher_name, pitcher_data in team_data.groupby('Pitcher'):
        avg_relheight = pitcher_data['AvgYT_Relheight'].mean()
        avg_relside = pitcher_data['AvgYT_Relside'].mean()
        plt.scatter(avg_relside, avg_relheight, s=100, color=color, label=pitcher_name)
    
    # Add mound and rubber visuals
    mound = patches.Ellipse((0, 0), width=6, height=1, angle=0, facecolor='brown', edgecolor='black', linewidth=1, zorder=2)
    ax.add_patch(mound)
    rubber = patches.Rectangle((-0.5, 0.5), width=1, height=0.25, angle=0, edgecolor='black', facecolor='white', zorder=3)
    ax.add_patch(rubber)

    plt.title(f'{team_name} Pitcher Averages')
    plt.xlabel('Horizontal Release (ft)')
    plt.ylabel('Vertical Release (ft)')
    plt.legend(title='Pitcher')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the plot
    team_folder = f'C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/{team_name}'
    os.makedirs(team_folder, exist_ok=True)
    plot_path = f'{team_folder}/{team_name}_Pitcher_Averages.png'
    plt.savefig(plot_path)
    plt.close()

# Function to get the color for a specific team
def get_team_color(team_name):
    if team_name == 'Florida southern':
        return 'red'
    elif team_name == 'Rollins':
        return 'blue'
    elif team_name == 'Tampa':
        return 'black'
    elif team_name == 'Barry':
        return 'orange' 
    elif team_name == 'Embry-riddle':
        return 'gold'
    elif team_name == 'Florida tech':
        return 'coral'
    elif team_name == 'Lynn':
        return 'cyan'
    elif team_name == 'Palm beach atlantic':
        return 'fuchsia'  
    elif team_name == 'Saint leo':
        return 'lime'                    
    else:
        return 'gray'  # Default color for other teams

# Create combined graph with all pitchers, but only one pitcher per team in the legend
def create_combined_graph(filtered_data):
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 15)

    # Keep track of teams already added to the legend
    teams_in_legend = set()

    for team_name, team_data in filtered_data.groupby('PitcherTeam'):
        color = get_team_color(team_name)

        # Plot data for all pitchers
        for pitcher_name, pitcher_data in team_data.groupby('Pitcher'):
            avg_relheight = pitcher_data['AvgYT_Relheight'].mean()
            avg_relside = pitcher_data['AvgYT_Relside'].mean()

            # Add to the legend only for the first pitcher of the team
            if team_name not in teams_in_legend:
                plt.scatter(avg_relside, avg_relheight, s=100, color=color, label=f'{team_name}')
                teams_in_legend.add(team_name)
            else:
                plt.scatter(avg_relside, avg_relheight, s=100, color=color)

    # Add mound and rubber visuals
    mound = patches.Ellipse((0, 0), width=6, height=1, angle=0, facecolor='brown', edgecolor='black', linewidth=1, zorder=2)
    ax.add_patch(mound)
    rubber = patches.Rectangle((-0.5, 0.5), width=1, height=0.25, angle=0, edgecolor='black', facecolor='white', zorder=3)
    ax.add_patch(rubber)

    plt.title('Combined Pitcher Averages for All Teams')
    plt.xlabel('Horizontal Release (ft)')
    plt.ylabel('Vertical Release (ft)')
    plt.legend(title='Teams', bbox_to_anchor=(.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the combined graph
    combined_plot_path = 'C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/AllTeams/Combined_Teams_Pitcher_Averages.png'
    os.makedirs('C:/Users/AlfredoCaraballo/OneDrive - DSSports/Desktop/Arm Angle/AllTeams', exist_ok=True)
    plt.savefig(combined_plot_path)
    plt.close()

    return combined_plot_path

# Main script to generate reports for each team and the combined graph
def generate_reports():
    # Generate individual reports for each team
    for team_name, team_data in filtered_data.groupby('PitcherTeam'):
        generate_team_avg_report(team_name, team_data)

    # Create combined graph and save it
    combined_graph_path = create_combined_graph(filtered_data)
    print(f"Combined graph saved at {combined_graph_path}")

# Generate all reports
generate_reports()
