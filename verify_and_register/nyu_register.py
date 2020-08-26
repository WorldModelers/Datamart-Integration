#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:37:54 2020

@author: travishartman
"""

import requests
import time
import csv
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

### FUNCTIONS ###

# POSTs the dataset to the NYU datamart
def upload_data(url, dataset, dataset_name, dataset_description, source):
    
    dataset.seek(0,0)
    response = requests.post(
               url,
               data={ "name": dataset_name,
                      "description": dataset_description,
                      "source": source
                    },
                files={'file': dataset}
                )
    try:
        dataset_id = response.json()['id']
    except: 
        logging.error("Error decoding response from NYU")
        logging.error(response.text)
    
    return dataset_id

# Check out the response's json fil to see when the dataset has been profiled
# and registered with the NYU datamart
def get_status(url_meta, dataset_id):
    
    response = requests.get(url_meta + dataset_id)
    response.raise_for_status()
    status_q = response.json()['status']
    
    if status_q == 'indexed':
        logging.debug(f"REGISTRATION COMPLETE")
        logging.debug(f"DATASET ID: {dataset_id}")
        return print("Your registered dataset is available at: https://wm.auctus.vida-nyu.org/")
    
    else:
        time.sleep(5)
        return get_status(url_meta, dataset_id)
    
# Login to NYU World Modelers Datamart    
def login_nyu(url, user, pwd):
    
    logon = False

    session = requests.Session()
    session.auth = (user, pwd)

    response = session.get(url)
    
    if response.status_code == 200:
        logging.debug("Successfully logged into Auctus World Modelers")
        logon = True
    
    else:
        logging.debug(f'Error: {response.status_code}. Update the config.ini file with the proper logon credentials.')
    
    return logon