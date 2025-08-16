import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import os

file = 'eco2mix-national-tr.csv'
df = pd.read_csv(file, sep=';',low_memory=False,skiprows=1, encoding='Latin1')
print(df.columns)

# """ Suppression colonnes jugées peu pertinentes pour la suite des analyses   """
# def drop_columns(df, columns_to_drop):
#     """
#     Supprime les colonnes spécifiées d'un DataFrame.
    
#     Args:
#     - df : DataFrame : Le DataFrame à modifier.
#     - columns_to_drop : list : Liste des noms des colonnes à supprimer.
    
#     Returns:
#     - df : DataFrame : Le DataFrame avec les colonnes supprimées.
#     """
#     return df.drop(columns_to_drop, axis=1)

# # """ Liste des colonnes à supprimer """
# columns_to_drop = ["stockage_batterie", "destockage_batterie", "gaz_autres", "eolien_offshore",
#                    "eolien_terrestre", "date_heure" , "ech_comm_angleterre", "ech_comm_espagne",
#                    "ech_comm_italie" ,"ech_comm_suisse" , "ech_comm_allemagne_belgique"]

# # """ Appel de la fonction pour supprimer les colonnes """
# df = drop_columns(df, columns_to_drop)

# """ Affichage du DataFrame résultant """


pd.set_option('display.max_columns', None)



def check_missing_values(df):
    """
    Vérifie et affiche le nombre de valeurs manquantes par colonne dans un DataFrame.

    Args:
    data (DataFrame): DataFrame contenant les données à vérifier.
    """
    # Calcul des valeurs manquantes par colonne
    missing_values = df.isna().sum()

    # Affichage
    print("Nombre de valeurs manquantes par colonne :")
    print(missing_values)
    
check_missing_values(df)


def fillna_with_mean(df, columns):
    """
    Remplace les valeurs manquantes dans les colonnes spécifiées par la moyenne de chaque colonne.

    Args:
    - df : DataFrame : Le DataFrame à modifier.
    - columns : list : Liste des noms des colonnes à traiter.

    Returns:
    - df : DataFrame : Le DataFrame avec les valeurs manquantes remplacées par la moyenne.
    """
    for column in columns:
        df[column] = df[column].fillna(df[column].mean())
    return df

columns_to_fill = ["consommation","prevision_j1","prevision_j","fioul","charbon", "gaz","nucleaire", "eolien","solaire","hydraulique","pompage","bioenergies","ech_physiques",
                   "taux_co2","fioul_tac","fioul_cogen","fioul_autres","gaz_tac","gaz_cogen","gaz_ccg","hydraulique_fil_eau_eclusee","hydraulique_lacs","hydraulique_step_turbinage",
                   "bioenergies_dechets","bioenergies_biomasse","bioenergies_biogaz"]                                                                                     

# """Appel de la fonction pour remplacer les valeurs manquantes par la moyenne"""
fillna_with_mean(df, columns_to_fill)





df.describe()
## Matrice de correlation 
correlation_matrix = df.corr()
print(correlation_matrix)
plt.figure(figsize=(12, 10))


sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', 
            square=True, annot_kws={'size':8}) 


plt.xticks(rotation=45, ha='right', size=15) 
plt.yticks(size=15)
# Titre et affichage
plt.title('Matrice de Corrélation')
plt.tight_layout()
plt.show()

