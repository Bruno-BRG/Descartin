import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_data_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    query = "SELECT date, residue_type, weight FROM residues"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def plot_weight_over_time(data, residue_type, start_date, end_date):
    # Filter data based on user input
    filtered_data = data[(data['residue_type'] == residue_type) & 
                         (data['date'] >= start_date) & 
                         (data['date'] <= end_date)]
    
    # Convert weight to float
    filtered_data['weight'] = filtered_data['weight'].astype(float)
    
    # Convert date to datetime
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    # Aggregate data by month
    filtered_data = filtered_data.resample('M', on='date').sum().reset_index()
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['date'], filtered_data['weight'], label=residue_type)
    plt.title(f'Weight Over Time for {residue_type}')
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.legend()
    
    # Format the x-axis to show month-by-month markings
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    plt.savefig(f'weight_over_time_{residue_type}.png')  # Save the plot as an image file
    plt.show()

if __name__ == "__main__":
    # Get data from the database
    data = get_data_from_db()
    
    # Get user input
    residue_type = input("Enter the residue type: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    # Plot the data
    plot_weight_over_time(data, residue_type, start_date, end_date)