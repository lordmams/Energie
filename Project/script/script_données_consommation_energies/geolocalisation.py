
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# Chargement des données
df = pd.read_csv('donnée concatenées.csv', usecols=['annee', 'region', 'filiere', 'valeur'], encoding='Latin1', sep=';')
df['annee'] = pd.to_datetime(df['annee'], format='%Y')

# Mapping des régions françaises vers leurs coordonnées
region_to_coords={
    'Auvergne-Rhône-Alpes': {'lat': 45.4473, 'lon': 4.3859},
    'Bourgogne-Franche-Comté': {'lat': 47.2805, 'lon': 4.9994},
    'Bretagne': {'lat': 48.2020, 'lon': -2.9326},
    'Centre-Val de Loire': {'lat': 47.7516, 'lon': 1.6751},
    'Corse': {'lat': 42.0396, 'lon': 9.0129},
    'Grand Est': {'lat': 48.6998, 'lon': 6.1878},
    'Hauts-de-France': {'lat': 50.4801, 'lon': 2.7937},
    'Île-de-France': {'lat': 48.8566, 'lon': 2.3522},
    'Normandie': {'lat': 49.1829, 'lon': 0.3707},
    'Nouvelle-Aquitaine': {'lat': 45.7074, 'lon': 0.1532},
    'Occitanie': {'lat': 43.8927, 'lon': 3.2828},
    'Pays de la Loire': {'lat': 47.7633, 'lon': -0.3296},
    'Provence-Alpes-Côte dAzur': {'lat': 43.9352, 'lon': 6.0679}
}

# Remplacer les valeurs nulles dans la colonne 'region' par 'Inconnu'
df['region'].fillna('Inconnu', inplace=True)

# Conversion de la colonne 'filiere' en string
df['filiere'] = df['filiere'].astype(str)

# Fonction pour calculer les totaux de consommation par région et par année
def calculate_consumption_totals(df, year):
    df_year = df[df['annee'].dt.year == year]
    consumption_totals = df_year.groupby('region')['valeur'].sum().reset_index()
    consumption_totals = consumption_totals.merge(
        pd.DataFrame.from_dict(region_to_coords, orient='index').reset_index().rename(columns={'index': 'region'}),
        on='region',
        how='left'
    )
    consumption_totals['weight'] = consumption_totals['valeur'] / consumption_totals['valeur'].max()  # Normaliser pour l'échelle de heatmap
    return consumption_totals

# Titre de la page
st.title('Répartition de la consommation d’énergie par région')

# Sélection de l'année avec un curseur dans la barre latérale
year_to_filter = st.sidebar.slider('Année', int(df['annee'].dt.year.min()), int(df['annee'].dt.year.max()))

# Filtrer les données en fonction de l'année sélectionnée et calculer les totaux
totals = calculate_consumption_totals(df, year_to_filter)

# Création de la visualisation avec pydeck
heatmap_layer = pdk.Layer(
    'HeatmapLayer',
    data=totals,
    opacity=0.9,
    get_position='[lon, lat]',
    get_weight='weight',
    threshold=0.5,
    aggregation='"MEAN"'
)

# Configuration de la vue initiale de la carte
view_state = pdk.ViewState(
    latitude=46.2276,
    longitude=2.2137,
    zoom=5,
    pitch=50,
)

# Affichage de la carte avec pydeck
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[heatmap_layer]
))