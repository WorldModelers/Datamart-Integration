#!/usr/bin/env python3
import nyu_register as nyu
import isi_register as isi
import spinner as sp
import configparser
import csv
import time
import sys
import os
from openpyxl import load_workbook
from requests import get, post
import pandas as pd
from io import StringIO
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


# Get input data
wrkDir = os.getcwd()
wrkDir = wrkDir + '/'

config = configparser.ConfigParser()
configFile = wrkDir + 'config.ini'
config.read(configFile)

################### set up logger event handling
username_nyu = config['NYU']['username']
password_nyu = config['NYU']['password']
url_nyu = config['NYU']['url']

username_isi = config['ISI']['username']
password_isi = config['ISI']['password']
url_isi = config['ISI']['url']

#open dataset and get info:
csv_file = open(sys.argv[1], 'r')
dataset = open(sys.argv[1], 'rb')
file_path = sys.argv[1]

datamart_api_url = f'https://{username_isi}:{password_isi}@{url_isi}'

# NYU TBD

###############  WELCOME MESSAGE
print("\n")
print("WELCOME TO THE T2WML ANNOTATER AND DATASET REGISTRATION TOOL")

# get meta Data from user
dataset_meta = isi.get_dataset_meta()

# Post meta data to ISI
posted_meta = isi.post_meta_to_api(dataset_meta, datamart_api_url)

# Update Excel Workbook to have correct dataset_id
logging.debug(f'Updating dataset ID in Excel Workbook: {file_path}')
workbook = load_workbook(filename=file_path)
sheet = workbook.active
sheet["B1"].value = dataset_meta["dataset_id"]
workbook.save(filename="csv/tmp.xlsx")
logging.debug(f'Completed update of Excel workbook: {file_path}')

# Upload dataset to T2WML
logging.debug(f'Uploading dataset to ISI')
url = f'{datamart_api_url}/datasets/{dataset_meta["dataset_id"]}/annotated'
file_path = 'csv/tmp.xlsx'
isi.upload_data_post(file_path, url)
logging.debug(f'ISI upload complete')

# Get variable(s)
logging.debug(f'Obtaining variables from ISI')
response = get(f'{datamart_api_url}/metadata/datasets/{dataset_meta["dataset_id"]}/variables')
variable_ids = [i.get('variable_id') for i in response.json()]

# Download data in canonical form
df_all_variables = pd.DataFrame()
for v in variable_ids:
    response = get(f'{datamart_api_url}/datasets/{dataset_meta["dataset_id"]}/variables/{v}')
    df = pd.read_csv(StringIO(response.text))
    if df_all_variables.shape[0] == 0:
        df_all_variables = df
    else:
        df_all_variables = df_all_variables.append(df)
df_all_variables = df_all_variables.reset_index().drop(columns=['index'])        

logging.debug(f'Saving data in canonical format to csv/tmp.csv')
df_all_variables.reset_index().to_csv('csv/tmp.csv')

# Upload to NYU
#login to wm auctus
api_url = f'https://{username_nyu}:{password_nyu}@{url_nyu}'
url_upload = api_url + 'upload' 
url_meta = api_url + 'metadata/'

# Upload to datamar
logging.debug(f'Uploading canonical data to NYU Datamart')
dataset = open('csv/tmp.csv', 'rb')
dataset_id = nyu.upload_data(url_upload, dataset, dataset_meta["name"], dataset_meta["description"], dataset_meta["url"])

#...wait for good response
print("Registering your dataset, this may take awhile...")
with sp.Spinner():
    nyu.get_status(url_meta, dataset_id)
