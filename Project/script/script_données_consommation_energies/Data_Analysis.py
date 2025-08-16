import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

file_path = 'eco2mix-national-tr.csv'

def load_data(file_path):
    """Charger les données à partir d'un fichier CSV."""
    return pd.read_csv(file_path, sep=';')

def plot_energy_consumption_by_source(df):
    """Diagramme en barres pour la consommation d'énergie par source."""
    plt.figure(figsize=(10, 6))
    total_consumption_by_source = df[["fioul", "charbon", "gaz", "nucleaire", "eolien", "solaire", "hydraulique",
                                      "pompage", "bioenergies"]].sum()
    total_consumption_by_source.plot(kind="bar", color="skyblue")
    plt.title("Consommation d'énergie par source")
    plt.xlabel("Source d'énergie")
    plt.ylabel("Consommation (MW)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def plot_energy_consumption_over_time(df):
    """Diagramme linéaire pour l'évolution de la consommation d'énergie au fil du temps."""
    plt.figure(figsize=(12, 6))
    df["date"] = pd.to_datetime(df["date"])
    plt.plot(df["date"], df["consommation"], marker='o', linestyle='-')
    plt.title("Évolution de la consommation d'énergie")
    plt.xlabel("Date")
    plt.ylabel("Consommation (MW)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def plot_energy_co2_relation(df):
    """Diagramme de dispersion pour la relation entre la consommation d'énergie et les émissions de CO2."""
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="consommation", y="taux_co2")
    plt.title("Relation entre la consommation d'énergie et les émissions de CO2")
    plt.xlabel("Consommation d'énergie (MW)")
    plt.ylabel("Taux de CO2 (gCO2/kWh)")
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def plot_correlation_heatmap(df):
    """Matrice de corrélation et heatmap."""
    plt.figure(figsize=(12, 10))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm',
                square=True, annot_kws={'size': 8})
    plt.xticks(rotation=45, ha='right', size=10)
    plt.yticks(size=10)
    plt.title('Matrice de Corrélation')
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def forecast_arima(df, order=(5,1,0), steps=30):
    """Prévision de la consommation d'énergie avec ARIMA."""
    model = ARIMA(df['consommation'], order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

def plot_forecast(df, forecast):
    """Tracer les données observées et la prévision."""
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['consommation'], label='Données observées')
    plt.plot(pd.date_range(start=df['date'].iloc[-1], periods=len(forecast), freq='D'), forecast, label='Prévision')
    plt.title('Prévision de la consommation d\'énergie avec ARIMA')
    plt.xlabel('Date')
    plt.ylabel('Consommation (MW)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt.gcf()) 

def boxplot_energy_consumption(df):
    """Boîte à moustaches pour la consommation d'énergie."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[['consommation']])
    plt.title("Boîte à moustaches de la consommation d'énergie")
    plt.ylabel("Consommation (MW)")
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def plot_consumption_by_year(df, max_consumption_year):
    """Tracer la consommation d'énergie par année avec mise en évidence de l'année maximale."""
    plt.figure(figsize=(12, 6))
    
    """ Tracer la consommation d'énergie par année """
    plt.plot(df['year'], df['consommation'], marker='o', linestyle='-', label='Consommation d\'énergie')

    """ Mettre en évidence l'année avec la consommation maximale """
    plt.scatter(max_consumption_year['year'], max_consumption_year['consommation'], color='red', label='Année maximale')

    plt.title('Consommation d\'énergie par année')
    plt.xlabel('Année')
    plt.ylabel('Consommation (MW)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt.gcf())  

def year_with_highest_consumption(df):
    """Trouver l'année avec la consommation maximale."""
    
    df['date'] = pd.to_datetime(df['date'])
    
    
    df['year'] = df['date'].dt.year
    
    df_yearly = df.groupby('year')['consommation'].sum().reset_index()
    
    max_year = df_yearly.loc[df_yearly['consommation'].idxmax()]
    
    return max_year

def violinplot_energy_consumption(df):
    """Diagramme de violon pour explorer la distribution de la consommation d'énergie."""
    plt.figure(figsize=(10, 6))
    sns.violinplot(y=df["consommation"], color="skyblue")
    plt.title("Distribution de la consommation d'énergie")
    plt.ylabel("Consommation (MW)")
    plt.tight_layout()
    st.pyplot(plt.gcf())


df = load_data(file_path)

"""Affichez les graphiques individuels avec Streamlit"""

plot_energy_consumption_by_source(df)
plot_energy_consumption_over_time(df)
plot_energy_co2_relation(df)
plot_correlation_heatmap(df)
forecast = forecast_arima(df)
plot_forecast(df, forecast)
max_consumption_year = year_with_highest_consumption(df)
boxplot_energy_consumption(df)
plot_consumption_by_year(df, max_consumption_year)
violinplot_energy_consumption(df)
