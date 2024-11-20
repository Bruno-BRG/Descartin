import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import os

def fetch_graph_data(residue_type, start_date, end_date):
    url = f'http://127.0.0.1:5001/api/residues/graph_data/?residue_type={residue_type}&start_date={start_date}&end_date={end_date}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def plot_graph(data, residue_type):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().any():
        print(f"Invalid date format in data: {df[df['date'].isnull()]}", file=sys.stderr)
    
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"axes.facecolor": "#3b3b3b", "grid.color": "#555"})
    sns.lineplot(x='date', y='weight', data=df, label=residue_type, color="#4c9ed9")
    
    # Increased font sizes
    plt.title(f'Weight Over Time for {residue_type}', color="#e0e0e0", fontsize=20)
    plt.xlabel('Date', color="#e0e0e0", fontsize=16)
    plt.ylabel('Weight', color="#e0e0e0", fontsize=16)
    plt.legend(facecolor="#3b3b3b", edgecolor="#555", labelcolor="#e0e0e0", fontsize=14)
    
    # Increased tick label sizes
    plt.gca().tick_params(axis='x', colors='#e0e0e0', labelsize=14)
    plt.gca().tick_params(axis='y', colors='#e0e0e0', labelsize=14)
    
    # Format the x-axis to show month-by-month markings
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=12))
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    # Set the color of the tick labels
    plt.gca().tick_params(axis='x', colors='#e0e0e0')
    plt.gca().tick_params(axis='y', colors='#e0e0e0')
    
    # Set the background color of the figure and axes
    plt.gcf().set_facecolor('#2b2b2b')
    plt.gca().set_facecolor('#3b3b3b')
    
    # Ensure the images directory exists
    os.makedirs('images', exist_ok=True)
    file_path = os.path.join('images', f'weight_over_time_{residue_type}.png')
    plt.savefig(file_path, facecolor=plt.gcf().get_facecolor())  # Save the plot as an image file
    return file_path

def plot_bar_chart(csv_path):
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().any():
        print(f"Invalid date format in data: {df[df['date'].isnull()]}", file=sys.stderr)
    
    df = df.groupby('residue_type')['weight'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='residue_type', y='weight', data=df, palette="Blues_d")
    
    # Increased font sizes
    plt.title('Total Weight by Residue Type', color="#e0e0e0", fontsize=20)
    plt.xlabel('Residue Type', color="#e0e0e0", fontsize=16)
    plt.ylabel('Total Weight', color="#e0e0e0", fontsize=16)
    plt.legend([],[], frameon=False)  # Remove legend if not needed
    
    # Increased tick label sizes
    plt.gca().tick_params(axis='x', colors='#e0e0e0', labelsize=14)
    plt.gca().tick_params(axis='y', colors='#e0e0e0', labelsize=14)
    
    # Set the color of the tick labels
    plt.gca().tick_params(axis='x', colors='#e0e0e0')
    plt.gca().tick_params(axis='y', colors='#e0e0e0')
    
    # Set the background color of the figure and axes
    plt.gcf().set_facecolor('#2b2b2b')
    plt.gca().set_facecolor('#3b3b3b')
    
    # Ensure the images directory exists
    os.makedirs('images', exist_ok=True)
    file_path = os.path.join('images', 'total_weight_by_residue_type.png')
    plt.savefig(file_path, facecolor=plt.gcf().get_facecolor())  # Save the plot as an image file
    return file_path

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'plot_bar_chart':
            csv_path = sys.argv[2]
            file_path = plot_bar_chart(csv_path)
        else:
            residue_type = sys.argv[1]
            start_date = sys.argv[2]
            end_date = sys.argv[3]
            data = fetch_graph_data(residue_type, start_date, end_date)
            file_path = plot_graph(data, residue_type)
        print(file_path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
