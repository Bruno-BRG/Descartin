import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:5000"

def fetch_data():
    response = requests.get(f"{API_URL}/weight")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from API")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Weight Data Dashboard")

    data = fetch_data()
    if data:
        df = pd.DataFrame(data)
        df['weight'] = df['weight'].str.replace(',', '.').astype(float)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df.set_index('date', inplace=True)
        
        st.write("## Data Overview")
        st.dataframe(df)

        col1, col2 = st.columns(2)

        with col1:
            st.write("## Weight Distribution by Residue Type")
            weight_distribution = df.groupby('residue_type')['weight'].sum().reset_index()
            st.bar_chart(weight_distribution.set_index('residue_type'))

        with col2:
            st.write("## Weight Over Time")
            for residue_type in df['residue_type'].unique():
                st.write(f"### {residue_type}")
                residue_df = df[df['residue_type'] == residue_type]
                monthly_weight = residue_df['weight'].resample('M').sum()
                st.line_chart(monthly_weight)

if __name__ == "__main__":
    main()
