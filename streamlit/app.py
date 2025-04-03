import hmac
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')  # Suppress Prophet warnings

API_URL = "http://localhost:8000"  # Use the service name 'api' instead of 'localhost'
#API_URL = "http://192.81.214.49:8000"  # Use the service name 'api' instead of 'localhost'

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

def prepare_prophet_data(df, residue_type):
    """Prepare data for Prophet forecasting."""
    df_prophet = df[df['residue_type'] == residue_type].copy()
    df_prophet = df_prophet.reset_index()
    df_prophet = df_prophet.rename(columns={'date': 'ds', 'weight': 'y'})
    return df_prophet

def forecast_weights(df_prophet, periods=12):
    """Generate forecasts using Prophet."""
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)
    return forecast

def perform_clustering(df):
    """Perform clustering on monthly weights by residue type."""
    # Prepare data for clustering
    pivot_df = df.reset_index().pivot_table(
        index='residue_type', 
        columns=pd.Grouper(key='date', freq='M'), 
        values='weight',
        aggfunc='sum'
    ).fillna(0)
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(pivot_df)
    
    # Perform K-means clustering
    n_clusters = min(3, len(pivot_df))  # Use at most 3 clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add clusters to the dataframe
    pivot_df['Cluster'] = clusters
    return pivot_df

def detect_anomalies(df, residue_type):
    """Detect anomalies in weight measurements."""
    residue_df = df[df['residue_type'] == residue_type].copy()
    monthly_weights = residue_df['weight'].resample('M').sum().values.reshape(-1, 1)
    
    # Train isolation forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso_forest.fit_predict(monthly_weights)
    
    # Prepare results
    monthly_data = residue_df['weight'].resample('M').sum()
    anomaly_df = pd.DataFrame({
        'date': monthly_data.index,
        'weight': monthly_data.values,
        'is_anomaly': anomalies == -1
    })
    return anomaly_df

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

        # Define common chart settings
        chart_height = 400
        chart_width = None  # This will make it use container width
        common_layout = dict(
            height=chart_height,
            margin=dict(l=50, r=50, t=50, b=50),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.write("## Distribuição de Peso por tipo de resíduo")
                weight_distribution = df.groupby('residue_type')['weight'].sum().reset_index()
                fig = px.bar(weight_distribution.set_index('residue_type'))
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("Ver Tabela de Distribuição de Peso por Tipo de Resíduo"):
                    st.dataframe(weight_distribution, use_container_width=True)

            with col2:
                st.write("## Distribuição de Peso por mês")
                residue_types = df['residue_type'].unique()
                # Create chart with initial data (first residue type)
                initial_residue_type = residue_types[0]
                residue_df = df[df['residue_type'] == initial_residue_type]
                monthly_weight = residue_df['weight'].resample('ME').sum()
                st.line_chart(monthly_weight, use_container_width=True)
                # Move selectbox below the chart
                selected_residue_type = st.selectbox("Selecione o tipo de residuo", residue_types)
                if selected_residue_type != initial_residue_type:
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

                # Create Plotly figure
                fig = go.Figure()
                
                # Add monthly weight line
                fig.add_trace(go.Scatter(
                    x=monthly_weight['date'],
                    y=monthly_weight['weight'],
                    name='Peso Mensal',
                    line=dict(color='#1f77b4')
                ))
                
                # Add trend line
                fig.add_trace(go.Scatter(
                    x=monthly_weight['date'],
                    y=monthly_weight['trend'],
                    name='Tendencia',
                    line=dict(color='red', dash='dash')
                ))
                
                # Update layout
                fig.update_layout(
                    showlegend=True,
                    height=400,
                    margin=dict(l=50, r=50, t=50, b=50),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    xaxis_title='Data',
                    yaxis_title='Peso'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                with st.expander("Ver Tabela de Distribuição de Peso Mensal com Tendência Linear"):
                    st.dataframe(monthly_weight, use_container_width=True)

        # Add new ML visualizations
        st.write("## Análises Avançadas de Machine Learning")
        
        # Second row - ML visualizations
        col4, col5 = st.columns([1, 1])
        
        with col4:
            st.write("### Previsão de Peso Futuro")
            residue_type = st.selectbox(
                "Selecione o tipo de resíduo para previsão",
                df['residue_type'].unique(),
                key='forecast_select'
            )
            
            # Prepare and run forecast
            df_prophet = prepare_prophet_data(df, residue_type)
            with st.spinner('Gerando previsão...'):
                forecast = forecast_weights(df_prophet)
                
                # Create forecast plot
                fig = go.Figure()
                
                # Add actual values
                fig.add_trace(go.Scatter(
                    x=df_prophet['ds'],
                    y=df_prophet['y'],
                    name='Histórico',
                    line=dict(color='blue')
                ))
                
                # Add forecast
                fig.add_trace(go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    name='Previsão',
                    line=dict(color='red')
                ))
                
                # Add uncertainty intervals
                fig.add_trace(go.Scatter(
                    x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
                    y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(0,100,80,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Intervalo de Confiança'
                ))
                
                fig.update_layout(
                    title=f'Previsão de Peso para {residue_type}',
                    xaxis_title='Data',
                    yaxis_title='Peso',
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)

        with col5:
            st.write("### Detecção de Anomalias")
            anomaly_residue = st.selectbox(
                "Selecione o tipo de resíduo para análise de anomalias",
                df['residue_type'].unique(),
                key='anomaly_select'
            )
            
            # Perform anomaly detection
            anomaly_df = detect_anomalies(df, anomaly_residue)
            
            # Create anomaly plot
            fig = go.Figure()
            
            # Add normal points
            normal_points = anomaly_df[~anomaly_df['is_anomaly']]
            fig.add_trace(go.Scatter(
                x=normal_points['date'],
                y=normal_points['weight'],
                mode='markers',
                name='Normal',
                marker=dict(color='blue')
            ))
            
            # Add anomaly points
            anomaly_points = anomaly_df[anomaly_df['is_anomaly']]
            fig.add_trace(go.Scatter(
                x=anomaly_points['date'],
                y=anomaly_points['weight'],
                mode='markers',
                name='Anomalia',
                marker=dict(color='red', size=10)
            ))
            
            fig.update_layout(
                title=f'Detecção de Anomalias para {anomaly_residue}',
                xaxis_title='Data',
                yaxis_title='Peso',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Third row - Clustering visualization
        st.write("### Agrupamento de Tipos de Resíduos")
        cluster_df = perform_clustering(df)
        
        # Create heatmap of clusters
        fig = px.imshow(
            cluster_df.drop('Cluster', axis=1),
            labels=dict(x="Mês", y="Tipo de Resíduo", color="Peso"),
            aspect="auto",
            color_continuous_scale="Viridis"
        )
        
        fig.update_layout(
            title='Padrões de Peso por Tipo de Resíduo',
            xaxis_title='Mês',
            yaxis_title='Tipo de Resíduo'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show cluster information
        st.write("#### Grupos Identificados:")
        for cluster in sorted(cluster_df['Cluster'].unique()):
            residues = cluster_df[cluster_df['Cluster'] == cluster].index.tolist()
            st.write(f"Grupo {cluster + 1}: {', '.join(residues)}")

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
