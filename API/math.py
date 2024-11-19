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
    sns.lineplot(x='date', y='weight', data=df, label=residue_type)
    
    plt.title(f'Weight Over Time for {residue_type}')
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.legend()
    
    # Format the x-axis to show month-by-month markings
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=12))
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    # Ensure the images directory exists
    os.makedirs('images', exist_ok=True)
    file_path = os.path.join('images', f'weight_over_time_{residue_type}.png')
    plt.savefig(file_path)  # Save the plot as an image file
    return file_path

if __name__ == "__main__":
    try:
        residue_type = sys.argv[1]
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        
        data = fetch_graph_data(residue_type, start_date, end_date)
        file_path = plot_graph(data, residue_type)
        print(file_path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
