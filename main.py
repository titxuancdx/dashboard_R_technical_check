"""
Main Script for Data Retrieval and Dashboard Visualization

This script handles the retrieval of data, updates if 
necessary, and initializes a dashboard for data visualization.
The data retrieval process includes checking if the data needs 
to be updated and downloading the data if required.

The script also defines the main function `main()`, which 
orchestrates the data retrieval and dashboard creation process.

To run this script, execute it from the command line or as 
a standalone Python application.

Author: Titouan Conte-Devolx
Date: 02/11/2023

"""

import dl_file
import traitement

PAGE_DL = "https://data.economie.gouv.fr/explore/dataset/controle_techn/export/?"\
    "disjunctive.cct_code_dept&disjunctive.cat_vehicule_ibelle&"\
    "disjunctive.cat_energie_libelle&sort=cct_code_dept"
PAGE_DATE = "https://data.economie.gouv.fr/explore/dataset/"\
    "controle_techn/information/?disjunctive.cct_code_dept&disjunctive."\
    "cat_vehicule_libelle&disjunctive.cat_energie_libelle&sort=cct_code_dept"
XPATH_DL = "/html/body/div[1]/main/div/div[4]/div[2]/div[2]"\
    "/div[7]/div/div/div/div[1]/ul[1]/li[1]/div/a"
XPATH_DATE = "/html/body/div[1]/main/div/div[4]/div[2]/div[2]"\
    "/div[1]/div/div[2]/div/div[5]/div/div[2]/div"
ATTRS_DL = "href"

def main():
    """
    The main function for the data retrieval and visualization dashboard.

    It checks if the data needs to be updated and initializes the dashboard.

    Returns:
        int: An integer status code, typically 0 for successful execution.
    """
    date_hour_const = dl_file.read_last_value()
    date_hour = dl_file.get_data(url=PAGE_DATE, xpath=XPATH_DATE)

    if date_hour != date_hour_const:
        print("Attendez la fin de la mise à jour de la dataframe (à peu près 2 minutes!)")
        url_dl = dl_file.get_data(url=PAGE_DL, xpath=XPATH_DL, attribute=ATTRS_DL)
        dl_file.download_data(url_dl, r"dataframe\controle_technique.csv")
        dl_file.save_value(date_hour)
    df_data = traitement.read_file(r"dataframe\controle_technique.csv", sep=";")
    df_data = traitement.process_data_column(df_data)

    print("dataframe à jour vous pouvez lancer le programme R 'app.R'")
    return 0

if __name__ == '__main__':
    main()
