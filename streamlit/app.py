import hmac
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

API_URL = "http://192.81.214.49:8000"  # Use the service name 'api' instead of 'localhost'

# Main Streamlit app starts here
def fetch_data():
    try:
        response = requests.get(f"{API_URL}/weight")
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        if data:
            return data
        else:
            st.error("No data received from API")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from API: {e}")
        return []

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%Y-%m-%d')
    except ValueError:
        return pd.to_datetime(date_str, format('%d/%m/%Y'))

def add_entry_form():
    """Form to add a new entry to the database."""
    data = fetch_data()
    if data:
        df = pd.DataFrame(data)
        residue_types = df['residue_type'].unique()

        with st.form("Adicionar novo dado"):
            weight = st.number_input("Peso", min_value=0.0, format="%.2f")
            residue_type = st.selectbox("Tipo do residuo", residue_types)
            date = st.date_input("Data")
            submitted = st.form_submit_button("Adicionar Dado")
            if submitted:
                response = requests.post(f"{API_URL}/weight", json={
                    "weight": f"{weight:.2f}".replace('.', ','),  # Ensure weight is formatted correctly
                    "residue_type": residue_type,
                    "date": date.strftime('%Y-%m-%d')
                })
                if response.status_code == 200:
                    st.success("Dado inserido com sucesso!")
                else:
                    st.error(f"Falha ao inserir dado: {response.text}")

def add_entry_page():
    """Page to add a new entry to the database."""
    st.title("Adicionar Dado")
    add_entry_form()

def main_page():
    """Main dashboard page."""
    st.title("Dashboard Descartin")
    st.markdown("Dados providos por [Cascais Data](https://data.cascais.pt/)")

    data = fetch_data()
    if data:
        df = pd.DataFrame(data)
        df['weight'] = df['weight'].str.replace(',', '.').astype(float)
        df['date'] = df['date'].apply(parse_date)
        df.set_index('date', inplace=True)

        # Ensure the date range covers from 2014 to the most recent date
        df = df[(df.index >= '2014-01-01') & (df.index <= '2024-12-31')]

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write("## Distribuição de Peso por tipo de resíduo")
                weight_distribution = df.groupby('residue_type')['weight'].sum().reset_index()
                st.bar_chart(weight_distribution.set_index('residue_type'), use_container_width=True)
                with st.expander("Ver Tabela de Distribuição de Peso por Tipo de Resíduo"):
                    st.dataframe(weight_distribution, use_container_width=True)

            with col2:
                st.write("## Distribuição de Peso por mês")
                residue_types = df['residue_type'].unique()
                selected_residue_type = st.selectbox("Selecione o tipo de residuo", residue_types)
                residue_df = df[df['residue_type'] == selected_residue_type]
                monthly_weight = residue_df['weight'].resample('ME').sum()
                st.line_chart(monthly_weight, use_container_width=True)
                with st.expander(f"Ver Tabela de Distribuição de Peso por Mês para {selected_residue_type}"):
                    st.dataframe(monthly_weight.reset_index(), use_container_width=True)

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
                fig.patch.set_facecolor('black')
                ax.set_facecolor('black')
                ax.plot(monthly_weight['date'], monthly_weight['weight'], label='Peso Mensal', color='white')
                ax.plot(monthly_weight['date'], monthly_weight['trend'], label='Tendencia', linestyle='--', color='red')
                ax.legend(facecolor='black', framealpha=1, edgecolor='white', labelcolor='white')
                ax.xaxis.label.set_color('white')
                ax.yaxis.label.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.title.set_color('white')
                for label in ax.get_xticklabels() + ax.get_yticklabels():
                    label.set_color('white')
                for spine in ax.spines.values():
                    spine.set_edgecolor('white')
                st.pyplot(fig)
                with st.expander("Ver Tabela de Distribuição de Peso Mensal com Tendência Linear"):
                    st.dataframe(monthly_weight, use_container_width=True)

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Ir para", ["Dashboard", "Adicionar Dado"])

    if page == "Dashboard":
        main_page()
    elif page == "Adicionar Dado":
        add_entry_page()

if __name__ == "__main__":
    main()
