"""
Data processing module.

This module contains functions to read a CSV file and process its columns
by performing various filtering and merging operations.

Author: Titouan Conte-Devolx
"""

import pandas as pd

def read_file(filename, sep):
    """
    Read a CSV file.

    Parameters:
    filename (str): The path to the CSV file.
    sep (str): The separator used in the CSV file.

    Returns:
    pandas.DataFrame: The DataFrame containing the data from the CSV file.
    """
     
    if sep == ";":
        df = pd.read_csv(filename, sep=';', low_memory=False)
    elif sep == ",":
        df = pd.read_csv(filename, sep=',', low_memory=False)
    else:
        return "Erreur : mauvais séparateur"
    return df

def process_data_column(df):
    """
    Process DataFrame columns.

    This function removes certain columns from the DataFrame and performs 
    merging and filtering operations
    Parameters:
    df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    pandas.DataFrame: The resulting DataFrame after processing.
    """
    df.dropna()
    df.drop(columns=["Adresse", "Raison sociale", "Téléphone",
                     "SIRET", "site web","coordgeo", 
                     "statut", "date_application_contre_visite", 
                     "date_application_visite"], inplace=True)
    
    df = df.rename(columns={'num_dep': 'Code_Departement',
                            'prix de la visite': 'price',
                            'Type de véhicule' : 'type_vehicule'})

    df_region = read_file("dataframe\departements-region.csv", sep=",")

    df_region = df_region.rename(columns={'dep_name': 'Departement',
                                          'region_name': 'region', 
                                          'num_dep': 'Code_Departement',})

    df_finale = pd.merge(df, df_region, on='Departement', how='left')

    df_extrm = df_finale[df_finale['price'] >= 200 ].index
    df_finale.drop(df_extrm, inplace=True)

    chemin_fichier_csv = "dataframe\df_finale.csv"
    df_finale.to_csv(chemin_fichier_csv, index=False)

    return df_finale

if __name__ == '__main__':
    df_data = read_file(r"dataframe\controle_technique.csv", sep=";")
    df_data = process_data_column(df_data)
