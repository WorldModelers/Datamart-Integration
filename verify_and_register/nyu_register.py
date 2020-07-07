#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 19:37:54 2020

@author: travishartman
"""

import requests
import time
import csv

### FUNCTIONS ###

# POSTs the dataset to the NYU datamart
def upload_data(url, dataset, dataset_name, dataset_description):
    
    dataset.seek(0,0)
    response = requests.post(
               url,
               data={ "name": dataset_name,
                      "description": dataset_description,
                    },
                files={'file': dataset}
                )
    dataset_id = response.json()['id']
    
    return dataset_id

# Check out the response's json fil to see when the dataset has been profiled
# and registered with the NYU datamart
def get_status(url_meta, dataset_id):
    
    response = requests.get(url_meta + dataset_id)
    response.raise_for_status()
    status_q = response.json()['status']
    
    if status_q == 'indexed':
        print("\n")
        print(f"REGISTRATION COMPLETE")
        print(f"DATASET ID: {dataset_id}")
        return print("Your registered dataset is available at: https://wm.auctus.vida-nyu.org/")
    
    else:
        time.sleep(5)
        return get_status(url_meta, dataset_id)
    
# Login to NYU World Modelers Datamart    
def login_nyu(url, user, pwd):
    
    session = requests.Session()
    session.auth = (user, pwd)

    response = session.get(url)
    
    if response.status_code == 200:
        return print("Successfully logged into Auctus World Modelers")
    
    else:
        return print(f'Error: {response.status_code}. Update the config.ini file with the proper logon credentials.')    