"""
dl_file.py

This module provides functions for downloading files 
from URLs and extracting data using Selenium.
Author: Titouan Conte-Devolx
"""

import os
import contextlib
import requests
from huggingface_hub import notebook_login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

VALUE_FILE = "variable\last_value.txt"

def save_value(valeur):
    """
    Save the provided value to the last_value.txt file.
    
    Parameters:
    valeur (int): The value to be saved.
    """
    with open(VALUE_FILE, 'w', encoding='utf-8') as fichier:
        fichier.write(str(valeur))

def read_last_value():
    """
    Read and return the last saved value from the last_value.txt file. 
    If the file doesn't exist, create it with a default value of 0.

    Returns:
    int: The last saved value.
    """
    if not os.path.exists(VALUE_FILE):
        valeur_par_defaut = 0
        save_value(valeur_par_defaut)
        return valeur_par_defaut

    try:
        with open(VALUE_FILE, 'r',encoding="utf-8") as fichier:
            return fichier.read().strip()
    except FileNotFoundError:
        print("FileNotFound Exception: no such file found")
        return None


def get_data(url, xpath, attribute=None, timeout=20):
    """
    Extract data from a web page using Selenium.

    Parameters:
    url (str): The URL of the web page to scrape.
    xpath (str): The XPath expression to locate the 
    element containing the desired data.
    attribute (str, optional): The HTML attribute 
    to extract from the element (default is None).
    timeout (int, optional): Maximum time to wait 
    for the element to be present (default is 20).

    Returns:
    str: Extracted data from the specified element.
    """
    options = Options()
    options.headless = True

    with contextlib.ExitStack() as stack:
        browser = stack.enter_context(webdriver.Firefox(options=options))
        try:
            browser.get(url)
            wait = WebDriverWait(browser, timeout)
            if attribute is None:
                data = wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                data = data.text
            else:
                data = wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                ).get_attribute(attribute)
            return data
        except TimeoutException:
            print("Timeout exception: Element not found "
                  "within the specified timeout.")
            return None
        except NoSuchElementException:
            print("NoSuchElementException: The "
                  "specified element was not found.")
            return None





def download_data(url, file_name):
    """
    Download a file from the specified URL 
    and save it with the provided file name.

    Parameters:
    url (str): The URL of the file to download.
    file_name (str): The desired file name for 
    the downloaded file.
    """
    response = requests.get(url, timeout=10)  # Added timeout for requests.get

    if response.status_code == 200:
        with open(file_name, 'wb') as fichier:
            fichier.write(response.content)
        print('Le fichier', file_name, 'a été téléchargé avec succès.')
    else:
        print('Erreur lors du téléchargement du fichier. Code d\'état :'
              , response.status_code)
