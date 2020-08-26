#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:37:16 2020

@author: travishartman
"""

import os
import json
import pandas as pd
from io import StringIO
from requests import get,post,put,delete
import requests
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


# Define a new dataset
# get the metadata to start process of addinga new dataset
def get_dataset_meta():
    
    name = input('Enter Dataset Name: ')
    dataset_id = input('Enter Dataset ID: ')
    description = input('Enter Dataset Description: ')
    url= input("Enter Dataset Source: ")
    
    dataset_meta = {"name": name,
                    "dataset_id": dataset_id,
                    "description": description,
                    "url": url
                    }
        
    return dataset_meta

# Post the dataset meta to the ISI datamart...repeated dataset Identifiers Raise an error
def post_meta_to_api(dataset_meta, datamart_api_url):
    
    td_response = post(f'{datamart_api_url}/metadata/datasets', json = dataset_meta)
    logging.debug("ISI posting metadata to API")
    try:
        output = json.dumps(td_response.json(), indent=2)
        return print(json.dumps(td_response.json(), indent=2))
    except:
        logging.error(f"ERROR: {td_response.text}")    
        sys.exit(f"Process failed: {td_response.text}")


# DEFINE a new variable to be added to the dataset
# return the dataset_id to feed into the next function...    
def define_new_variable(datamart_api_url, dataset_id):
    
    name = input('Enter Variable Name: ')
    variable_id = input('Enter Variable ID: ')
    
    variable = {"name": name,
                "variable_id": variable_id,
                }
    
    tv_response = post(f'{datamart_api_url}/metadata/datasets/{dataset_id}/variables', json=variable)

    # Print out the post results
    logging.info(json.dumps(tv_response.json(), indent=2))
    
    return variable['variable_id']

#Retrieve all variables for the dataset
def print_all_dataset_variables(datamart_api_url, dataset_id):
    
    response = get(f'{datamart_api_url}/metadata/datasets/{dataset_id}/variables')
    
    return print(json.dumps(response.json(), indent=2))


#Upload data to the dataset and assign data to a variable 
def upload_data(datamart_api_url, file_path, dataset_id, dataset_variable, overwrite=False):
    
    url = f'{datamart_api_url}/datasets/{dataset_id}/variables/{dataset_variable}'
    
    file_name = os.path.basename(file_path)
    files = {
        'file': (file_name, open(file_path, mode='rb'), 'application/octet-stream')
    }
    
    # post APPENDS the new data to the variable shell
    # put OVERWRITES the existing data in the variable sell with the new data
    # Repeated row data will not be added
    
    if overwrite:
        response = put(url, files=files)
    else:
        response = post(url, files=files)
    
    if response.status_code == 400:
        logging.info(json.dumps(response.json(), indent=2))
    else:
        logging.info(response.json())

# Print out the dataset to user
def show_dataset(datamart_api_url, dataset_id, variable_id):
    
    response = get(f'{datamart_api_url}/datasets/{dataset_id}/variables/{variable_id}')

    df = pd.read_csv(StringIO(response.text))

    return print(df)

# Login into the ISI datamart with creds from config.ini
# Return T/F and brak from execution if False/not connected
def login_isi(url, user, pwd):
    
    logon = False

    session = requests.Session()
    session.auth = (user, pwd)

    response = session.get(url)
    
    if response.status_code == 200:
        return print("Successfully logged into ISI Datamart")
        logon = True
    
    else:
        logging.error(f'Error: {response.status_code}. Update the config.ini file with the proper logon credentials.')
    
    return logon


def upload_data_post(file_path, url):
    file_name = os.path.basename(file_path)
    files = {
        'file': (file_name, open(file_path, mode='rb'), 'application/octet-stream')
    }
    response = post(url, files=files)
    if response.status_code == 400:
        try:
            out = json.dumps(response.json(), indent=2)
            logging.info(out)
        except:
            logging.error(f"ERROR: {response.text}")
    else:
        try:
            out = json.dumps(response.json(), indent=2)
            logging.info(out)
        except:
            logging.error(f"ERROR: {response.text}")
            sys.exit("Process failed.")