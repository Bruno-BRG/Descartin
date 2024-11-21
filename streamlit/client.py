import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_URL = "http://127.0.0.1:5001/api"

def fetch_residues():
    response = requests.get(f"{API_URL}/residues/")
    response.raise_for_status()
    return response.json()

def fetch_residue_types():
    response = requests.get(f"{API_URL}/residue_types/")
    response.raise_for_status()
    return response.json()

def fetch_graph_data(residue_type, start_date, end_date):
    response = requests.get(f"{API_URL}/residues/graph_data/?residue_type={residue_type}&start_date={start_date}&end_date={end_date}")
    response.raise_for_status()
    return response.json()

def fetch_all_time_weight():
    response = requests.get(f"{API_URL}/all_time_weight")
    response.raise_for_status()
    return response.json()

def plot_graph(data, residue_type):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().any():
        st.error(f"Invalid date format in data: {df[df['date'].isnull()]}")
    
    plt.figure(figsize=(10, 6))
    sns.set_style("darkgrid", {"axes.facecolor": "#3b3b3b", "grid.color": "#555"})
    sns.lineplot(x='date', y='weight', data=df, label=residue_type, color="#4c9ed9")
    
    plt.title(f'Weight Over Time for {residue_type}', color="#e0e0e0", fontsize=20)
    plt.xlabel('Date', color="#e0e0e0", fontsize=16)
    plt.ylabel('Weight', color="#e0e0e0", fontsize=16)
    plt.legend(facecolor="#3b3b3b", edgecolor="#555", labelcolor="#e0e0e0", fontsize=14)
    plt.gca().tick_params(axis='x', colors='#e0e0e0', labelsize=14)
    plt.gca().tick_params(axis='y', colors='#e0e0e0', labelsize=14)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=12))
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()
    plt.gcf().set_facecolor('#2b2b2b')
    plt.gca().set_facecolor('#3b3b3b')
    
    st.pyplot(plt)

def plot_bar_chart(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().any():
        st.error(f"Invalid date format in data: {df[df['date'].isnull()]}")
    
    df = df.groupby('residue_type')['weight'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='residue_type', y='weight', data=df, palette="Blues_d")
    
    plt.title('Total Weight by Residue Type', color="#e0e0e0", fontsize=20)
    plt.xlabel('Residue Type', color="#e0e0e0", fontsize=16)
    plt.ylabel('Total Weight', color="#e0e0e0", fontsize=16)
    plt.legend([],[], frameon=False)
    plt.gca().tick_params(axis='x', colors='#e0e0e0', labelsize=14)
    plt.gca().tick_params(axis='y', colors='#e0e0e0', labelsize=14)
    plt.gcf().set_facecolor('#2b2b2b')
    plt.gca().set_facecolor('#3b3b3b')
    
    st.pyplot(plt)

st.title("Residue Dashboard")

st.sidebar.header("Filters")
residue_types = fetch_residue_types()
selected_residue_type = st.sidebar.selectbox("Select Residue Type", residue_types)
time_range = st.sidebar.selectbox("Select Time Range", ["all_time", "last_year", "last_month"])

if st.sidebar.button("Generate Line Graph"):
    if time_range == "last_year":
        start_date = (pd.to_datetime("today") - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
    elif time_range == "last_month":
        start_date = (pd.to_datetime("today") - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
    else:
        start_date = "1900-01-01"
    end_date = pd.to_datetime("today").strftime('%Y-%m-%d')
    graph_data = fetch_graph_data(selected_residue_type, start_date, end_date)
    plot_graph(graph_data, selected_residue_type)

selected_residue_types = st.sidebar.multiselect("Select Residue Types for Bar Chart", residue_types)
if st.sidebar.button("Generate Bar Chart"):
    if selected_residue_types:
        if time_range == "last_year":
            start_date = (pd.to_datetime("today") - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
        elif time_range == "last_month":
            start_date = (pd.to_datetime("today") - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
        else:
            start_date = "1900-01-01"
        end_date = pd.to_datetime("today").strftime('%Y-%m-%d')
        bar_chart_data = fetch_graph_data(selected_residue_types, start_date, end_date)
        plot_bar_chart(bar_chart_data)

if st.sidebar.button("Generate All Time Weight Graph"):
    all_time_weight_data = fetch_all_time_weight()
    plot_bar_chart(all_time_weight_data)

st.header("Residue Data")
residues = fetch_residues()
df = pd.DataFrame(residues)
st.dataframe(df)
