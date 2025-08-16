import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def load_data_pandas(csv_path):
    """
    Charge les données avec pandas au lieu de PySpark
    """
    try:
        # Charger le CSV avec pandas en gérant les lignes vides et erreurs
        df = pd.read_csv(csv_path, skiprows=0, skip_blank_lines=True)
        
        # Nettoyer les lignes complètement vides
        df = df.dropna(how='all')
        
        # Afficher les colonnes pour debug
        st.write("Colonnes détectées:", df.columns.tolist())
        st.write("Premières lignes brutes:", df.head(2))
        
        # Renommer la colonne pour plus de facilité
        if 'Date - Heure' in df.columns:
            df = df.rename(columns={'Date - Heure': 'Date_Heure'})
        
        # Convertir les colonnes de date avec gestion d'erreurs améliorée
        if 'Date_Heure' in df.columns:
            # Nettoyer d'abord les valeurs vides dans Date_Heure
            df = df.dropna(subset=['Date_Heure'])
            
            # Convertir en datetime avec gestion d'erreurs
            df['Date_Heure'] = pd.to_datetime(df['Date_Heure'], errors='coerce', utc=True)
            
            # Supprimer les lignes où la conversion a échoué
            df = df.dropna(subset=['Date_Heure'])
            
            # Créer les colonnes temporelles seulement si Date_Heure existe et est valide
            if len(df) > 0:
                df['Date'] = df['Date_Heure'].dt.date
                df['Heure'] = df['Date_Heure'].dt.time
                df['Year'] = df['Date_Heure'].dt.year
                df['Month'] = df['Date_Heure'].dt.month
                df['DayOfYear'] = df['Date_Heure'].dt.dayofyear
        
        # Nettoyer les données numériques
        if 'Consommation brute totale (MW)' in df.columns:
            # Convertir en numérique et supprimer les lignes avec valeurs manquantes
            df['Consommation brute totale (MW)'] = pd.to_numeric(df['Consommation brute totale (MW)'], errors='coerce')
            df = df.dropna(subset=['Consommation brute totale (MW)'])
        
        # Remplir les valeurs manquantes pour la consommation de gaz avec la moyenne
        if 'Consommation brute gaz (MW PCS 0°C) - GRTgaz' in df.columns:
            df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'] = pd.to_numeric(
                df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'], errors='coerce'
            )
            mean_value = df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'].mean()
            df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'].fillna(mean_value, inplace=True)
        
        # Gérer la colonne électricité
        if 'Consommation brute électricité (MW) - RTE' in df.columns:
            df['Consommation brute électricité (MW) - RTE'] = pd.to_numeric(
                df['Consommation brute électricité (MW) - RTE'], errors='coerce'
            )
        
        # Créer la variable numérique pour les mouvements sociaux
        if 'mouvement_social' in df.columns:
            # Convertir les booléens/strings en numérique
            df['mouvement_social'] = df['mouvement_social'].astype(str).str.lower()
            df['mouvement_social_num'] = df['mouvement_social'].map({
                'true': 1, 'false': 0, '1': 1, '0': 0, 'yes': 1, 'no': 0
            }).fillna(0).astype(int)
        else:
            df['mouvement_social_num'] = 0
        
        # Vérifier qu'il reste des données après nettoyage
        if len(df) == 0:
            raise ValueError("Aucune donnée valide trouvée après nettoyage")
        
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        import traceback
        st.error(f"Détails de l'erreur: {traceback.format_exc()}")
        return None

def statistical_analysis(df):
    """
    Analyse statistique avec pandas
    """
    if 'mouvement_social_num' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        return None, None, df
    
    group1 = df[df['mouvement_social_num'] == 1]['Consommation brute totale (MW)']
    group2 = df[df['mouvement_social_num'] == 0]['Consommation brute totale (MW)']
    
    if len(group1) > 0 and len(group2) > 0:
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
        return t_stat, p_value, df
    else:
        return None, None, df

def plot_average_consumption_per_year(df):
    """
    Graphique de la consommation moyenne par année
    """
    if 'Year' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    avg_consumption_year = df.groupby('Year')['Consommation brute totale (MW)'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_consumption_year, x='Year', y='Consommation brute totale (MW)')
    plt.title('Moyenne de la Consommation par Année')
    plt.xlabel('Année')
    plt.ylabel('Moyenne de Consommation (MW)')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

def plot_monthly_average_consumption(df):
    """
    Graphique de la consommation moyenne par mois
    """
    if 'Month' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    avg_consumption_month = df.groupby('Month')['Consommation brute totale (MW)'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_consumption_month, x='Month', y='Consommation brute totale (MW)')
    plt.title('Moyenne de la Consommation par Mois')
    plt.xlabel('Mois')
    plt.ylabel('Moyenne de Consommation (MW)')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

def plot_gas_vs_electricity_consumption(df):
    """
    Graphique de comparaison gaz vs électricité
    """
    required_cols = ['Date', 'Consommation brute gaz (MW PCS 0°C) - GRTgaz', 'Consommation brute électricité (MW) - RTE']
    if not all(col in df.columns for col in required_cols):
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    # Préparation des données
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    df_copy = df_copy.set_index('Date')
    df_weekly = df_copy.resample('W')[required_cols[1:]].mean()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_weekly, x=df_weekly.index, y='Consommation brute gaz (MW PCS 0°C) - GRTgaz', label='Consommation de Gaz')
    sns.lineplot(data=df_weekly, x=df_weekly.index, y='Consommation brute électricité (MW) - RTE', label='Consommation d\'Électricité')
    plt.title('Consommation de Gaz vs Consommation d\'Électricité')
    plt.xlabel('Date')
    plt.ylabel('Consommation (MW)')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)
    plt.close()

def plot_heatmap_daily_hourly_consumption(df):
    """
    Heatmap de la consommation par heure et jour de la semaine
    """
    if 'Date_Heure' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    df_copy = df.copy()
    df_copy['Hour'] = df_copy['Date_Heure'].dt.hour
    df_copy['DayOfWeek'] = df_copy['Date_Heure'].dt.dayofweek
    
    pivot_table = df_copy.pivot_table(values='Consommation brute totale (MW)', 
                                     index='Hour', 
                                     columns='DayOfWeek', 
                                     aggfunc='mean')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap='coolwarm')
    plt.title('Heatmap of Energy Consumption by Hour and Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Hour of Day')
    st.pyplot(plt)
    plt.close()

def plot_smoothed_time_series(df):
    """
    Série temporelle lissée
    """
    if 'Date' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    
    # Supprimer les doublons par date
    df_copy = df_copy.drop_duplicates('Date')
    df_copy = df_copy.set_index('Date').sort_index()
    
    # Appliquer le lissage
    df_copy['Consommation_smoothed'] = df_copy['Consommation brute totale (MW)'].rolling(window=7).mean()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_copy, x=df_copy.index, y='Consommation_smoothed')
    plt.title('Smoothed Time Series of Energy Consumption')
    plt.xlabel('Date')
    plt.ylabel('Smoothed Consumption (MW)')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

def plot_correlation(df):
    """
    Graphique de corrélation
    """
    required_cols = ['Consommation brute gaz (MW PCS 0°C) - GRTgaz', 'Consommation brute électricité (MW) - RTE']
    if not all(col in df.columns for col in required_cols):
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    # Créer les conditions pour les couleurs
    conditions = [
        df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'] > df['Consommation brute électricité (MW) - RTE'],
        df['Consommation brute gaz (MW PCS 0°C) - GRTgaz'] <= df['Consommation brute électricité (MW) - RTE']
    ]
    colors = ['red', 'blue']
    df_copy = df.copy()
    df_copy['colors'] = np.select(conditions, colors)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Consommation brute gaz (MW PCS 0°C) - GRTgaz',
                    y='Consommation brute électricité (MW) - RTE',
                    data=df_copy,
                    palette=colors,
                    hue='colors',
                    legend=None)
    
    plt.title('Correlation between Gas and Electricity Consumption')
    plt.xlabel('Gas Consumption (MW)')
    plt.ylabel('Electricity Consumption (MW)')
    st.pyplot(plt)
    plt.close()

def plot_monthly_boxplot(df):
    """
    Boxplot mensuel
    """
    if 'Month' not in df.columns or 'Consommation brute totale (MW)' not in df.columns:
        st.error("Colonnes nécessaires manquantes pour ce graphique")
        return
    
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Month', y='Consommation brute totale (MW)', data=df)
    plt.title('Monthly Boxplot of Energy Consumption')
    plt.xlabel('Month')
    plt.ylabel('Energy Consumption (MW)')
    st.pyplot(plt)
    plt.close()

def main():
    st.title('Analyse de Consommation Énergétique (Version Pandas)')
    st.info("Cette version utilise pandas au lieu de PySpark pour éviter les problèmes de configuration Java.")

    tabs = st.sidebar.radio("Navigation", ["Visualisation", "Analyse"])
    
    # Chemin vers le fichier CSV
    csv_path = './Consomation&Mouvement.csv'
    
    # Vérifier si le fichier existe
    import os
    if not os.path.exists(csv_path):
        st.error(f"Le fichier {csv_path} n'existe pas. Veuillez vérifier le chemin.")
        return
    
    # Charger les données avec pandas
    with st.spinner("Chargement des données..."):
        df = load_data_pandas(csv_path)
    
    if df is None:
        st.error("Impossible de charger les données.")
        return
    
    st.success(f"Données chargées avec succès ! {len(df)} lignes.")
    
    # Afficher un aperçu des données
    with st.expander("Aperçu des données"):
        st.write("Premières lignes :")
        st.dataframe(df.head())
        st.write("Colonnes disponibles :")
        st.write(df.columns.tolist())
        st.write("Informations sur les données :")
        st.write(f"- Nombre de lignes: {len(df)}")
        st.write(f"- Nombre de colonnes: {len(df.columns)}")

    if tabs == "Visualisation":
        st.subheader("Visualisation des Données")

        visualization_options = {
            "Moyenne de la Consommation par Année": plot_average_consumption_per_year,
            "Moyenne de la Consommation par Mois": plot_monthly_average_consumption,
            "Consommation de Gaz vs Consommation d'Électricité": plot_gas_vs_electricity_consumption,
            "Heatmap de la Consommation Énergétique par Heure et Jour de la Semaine": plot_heatmap_daily_hourly_consumption,
            "Consommation énergétique au fil du temps": plot_smoothed_time_series,
            "Corrélation entre la Consommation de Gaz et d'Électricité": plot_correlation,
            "Distribution Mensuelle de la Consommation Énergétique": plot_monthly_boxplot
        }

        selected_visualization = st.selectbox("Sélectionnez une visualisation prédéfinie", 
                                            list(visualization_options.keys()))

        if st.button("Générer la visualisation"):
            with st.spinner("Génération du graphique..."):
                try:
                    visualization_options[selected_visualization](df)
                except Exception as e:
                    st.error(f"Erreur lors de la génération du graphique: {e}")

    elif tabs == "Analyse":
        st.subheader("Analyse Statistique")

        try:
            t_stat, p_value, _ = statistical_analysis(df)
            
            if t_stat is not None and p_value is not None:
                st.write("**Résultats du test t de Student:**")
                st.write(f"T-statistic: {t_stat:.4f}")
                st.write(f"P-value: {p_value:.4f}")
                
                if p_value < 0.05:
                    st.write("✅ p est inférieure au seuil prédéfini (0.05), on rejette l'hypothèse nulle.")
                    st.write("Les différences entre les moyennes des groupes sont statistiquement significatives.")
                else:
                    st.write("❌ p est supérieure au seuil prédéfini (0.05), on ne peut pas rejeter l'hypothèse nulle.")
                
                # Boxplot
                if 'mouvement_social_num' in df.columns and 'Consommation brute totale (MW)' in df.columns:
                    plt.figure(figsize=(10, 6))
                    sns.boxplot(x='mouvement_social_num', y='Consommation brute totale (MW)', data=df)
                    plt.title('Distribution de la Consommation Énergétique par Statut de Mouvement Social')
                    plt.xlabel('Mouvement Social (0=Non, 1=Oui)')
                    plt.ylabel('Consommation brute totale (MW)')
                    st.pyplot(plt)
                    plt.close()
            else:
                st.warning("Impossible de réaliser l'analyse statistique avec les données disponibles.")
                
        except Exception as e:
            st.error(f"Erreur lors de l'analyse statistique: {e}")

if __name__ == "__main__":
    main() 