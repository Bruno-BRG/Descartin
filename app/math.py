import requests
import matplotlib.pyplot as plt
import pandas as pd
import sys

def fetch_graph_data(residue_type, start_date, end_date):
    url = f'http://127.0.0.1:5000/residues/graph_data/?residue_type={residue_type}&start_date={start_date}&end_date={end_date}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def plot_graph(data, residue_type):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['weight'], label=residue_type)
    plt.title(f'Weight Over Time for {residue_type}')
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.legend()
    
    # Format the x-axis to show month-by-month markings
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=12))
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    file_path = f'weight_over_time_{residue_type}.png'
    plt.savefig(file_path)  # Save the plot as an image file
    return file_path

if __name__ == "__main__":
    residue_type = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    
    data = fetch_graph_data(residue_type, start_date, end_date)
    file_path = plot_graph(data, residue_type)
    print(file_path)
