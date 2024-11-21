import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

API_URL = "http://localhost:5000"

def fetch_data():
    response = requests.get(f"{API_URL}/weight")
    if response.status_code == 200:
        data = response.json()
        # Verify the data fetched from the API
        if data:
            return data
        else:
            st.error("No data received from API")
            return []
    else:
        st.error("Failed to fetch data from API")
        return []

def main():
    st.set_page_config(layout="wide")
    st.title("Dashboard Descartin")

    data = fetch_data()
    if data:
        df = pd.DataFrame(data)
        df['weight'] = df['weight'].str.replace(',', '.').astype(float)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df.set_index('date', inplace=True)

        # Ensure the date range covers from 2014 to the most recent date
        df = df[(df.index >= '2014-01-01') & (df.index <= '2024-12-31')]

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.write("## Distribuição de Peso por tupo de resíduo")
            weight_distribution = df.groupby('residue_type')['weight'].sum().reset_index()
            st.bar_chart(weight_distribution.set_index('residue_type'), use_container_width=True)

        with col2:
            st.write("## Distribuição de Peso por mês")
            residue_types = df['residue_type'].unique()
            selected_residue_type = st.selectbox("Selecione o tipo de residuo", residue_types)
            residue_df = df[df['residue_type'] == selected_residue_type]
            monthly_weight = residue_df['weight'].resample('ME').sum()
            st.line_chart(monthly_weight, use_container_width=True)

        with col3:
            st.write("## Distribuição de Peso por mês com Tendência Linear")
            # Prepare data for linear regression
            monthly_weight = monthly_weight.reset_index()
            monthly_weight['date_ordinal'] = monthly_weight['date'].map(pd.Timestamp.toordinal)
            X = monthly_weight['date_ordinal'].values.reshape(-1, 1)
            y = monthly_weight['weight'].values

            # Fit linear regression model
            model = LinearRegression()
            model.fit(X, y)
            monthly_weight['trend'] = model.predict(X)

            # Plot the line chart with trend line
            fig, ax = plt.subplots()
            ax.plot(monthly_weight['date'], monthly_weight['weight'], label='Monthly Weight')
            ax.plot(monthly_weight['date'], monthly_weight['trend'], label='Trend', linestyle='--')
            ax.legend()
            st.pyplot(fig)

if __name__ == "__main__":
    main()
