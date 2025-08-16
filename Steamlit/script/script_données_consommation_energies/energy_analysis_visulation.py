import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from Data_Analysis import * 


df = pd.read_csv('eco2mix-national-tr.csv', sep=';')

option = st.sidebar.selectbox(
    'Choisissez le graphique que vous voulez afficher:',
    ('Consommation par source', 'Consommation au fil du temps', 'Relation énergie-CO2', 'Heatmap de corrélation', 'Boxplot de la consommation', 'Consommation par année', 'Violon de la consommation')
)

if option == 'Consommation par source':
    st.subheader("Consommation d'énergie par source")
    plot_energy_consumption_by_source(df)
    st.write("""Ce graphique montre la consommation totale d'énergie par source. Il est utile pour comparer directement quelle source d'énergie contribue le plus à la consommation globale.
             En l'occurance ici, nous voyons le nucléaire est la source d'énérgie la plus utiliée en France. """)

elif option == 'Consommation au fil du temps':
    st.subheader("Évolution de la consommation d'énergie au fil du temps")
    plot_energy_consumption_over_time(df)  
    st.write("""Ce graphique représente l'évolution de la consommation d'énergie au fil du temps. On peut observer deux points importants :
- **Baisse de la consommation en fin d'année 2022 :** En novembre et décembre 2022, la consommation d'électricité a chuté, par rapport à la même période avant la crise sanitaire. Cette baisse a touché tous les secteurs, notamment l'industrie, le tertiaire et le résidentiel.
- **Augmentation des prix de l'électricité :** Le prix de l'électricité a augmenté en février 2024, avec une hausse significative. Cette hausse peut être en partie attribuée au rétablissement d'une taxe sur la consommation finale d'électricité, après que le gouvernement ait réduit cette taxe pendant deux ans pour contrer les effets de la crise énergétique.""")

elif option == 'Heatmap de corrélation':
    st.subheader("Heatmap de corrélation")
    plot_correlation_heatmap(df)  
    st.write("""Cette heatmap montre les corrélations entre les différentes variables du dataset.
            Elle permet de visualiser les relations entre les variables
            Corrélation avec la consommation: La variable "consommation" a divers degrés de corrélation avec d'autres variables, suggérant que certains types de production d'énergie sont plus directement liés à la consommation globale.
            Production d'énergie et échanges commerciaux: Il semble y avoir des corrélations entre les types de production d'énergie (nucléaire, solaire, etc.) et certains échanges commerciaux avec d'autres pays (éch_comm_*), ce qui pourrait indiquer une relation entre la production d'énergie domestique et les flux d'import-export""")
    
elif option == 'Boxplot de la consommation':
    st.subheader("Boxplot de la consommation d'énergie")
    boxplot_energy_consumption(df)
    st.write("""Ce boxplot permet de visualiser la distribution de la consommation d'énergie.
             la consommation d'énergie varie considérablement, avec un certain nombre de valeurs aberrantes qui pourraient indiquer des moments de consommation anormalement élevée ou faible. Cela pourrait être dû à des événements spécifiques qui influencent la consommation d'énergie, comme des périodes de forte chaleur ou de froid extrême, des événements industriels ou d'autres facteurs saisonniers. La médiane semble être autour de 40 000 MW, ce qui suggère que la moitié des valeurs de consommation sont inférieures à ce point et l'autre moitié supérieure.""")

elif option == 'Consommation par année':
    st.subheader("Consommation d'énergie par année")
    max_consumption_year = year_with_highest_consumption(df)
    plot_consumption_by_year(df, max_consumption_year)
    st.write("Ce graphique montre la consommation d'énergie par année, avec une mise en évidence de l'année avec la consommation maximale qui est de Consommation maximale (MW): 1697783206.0 pour l'année 2023.")

elif option == 'Violon de la consommation':
    st.subheader("Violon de la consommation d'énergie")
    violinplot_energy_consumption(df)
    st.write("""Ce diagramme de violon illustre la distribution de la consommation d'énergie. Le diagramme combine des caractéristiques d'une boîte à moustaches et d'un graphique de densité de probabilité.
             La largeur du violon suggère qu'il y a des pics de fréquence à certains niveaux de consommation, ce qui peut indiquer des modes ou des niveaux de consommation typiques Cf : le nucléaire.""")

elif option == 'Relation énergie-CO2':
    st.subheader("Relation énergie-CO2")
    plot_energy_co2_relation(df)
    st.write(""" Le nuage de points présenté illustre la relation entre la consommation d'énergie (en MW) et les émissions de CO2 (en gCO2/kWh). Voici ce qu'oin peut en tirer:
            - **Distribution des données: Les données sont dispersées de façon à indiquer une tendance, à mesure que la consommation d'énergie augmente, les taux d'émissions de CO2 augmentent également.

            - **Concentration des données: La majorité des points sont être concentrés dans une certaine gamme de consommation d'énergie, avec le taux de CO2 qui augmente progressivement. Cela suggère une relation proportionnelle ou linéaire entre ces deux variables sur cette plage de consommation.

            - **Valeurs extrêmes : Il y a quelques valeurs extrêmes, en particulier un point avec un taux de CO2 significativement plus élevé par rapport à la consommation d'énergie, qui pourrait indiquer une inefficacité ou une anomalie à investiguer""")