#!/usr/bin/env python3
import verifier as vlad
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

# Get input data
wrkDir = os.getcwd()
wrkDir = wrkDir + '/'

config = configparser.ConfigParser()
configFile = wrkDir + 'config.ini'
config.read(configFile)

################### set up logger event handling
username_nyu = config['NYU']['username']
password_nyu = config['NYU']['password']

username_isi = config['ISI']['username']
password_isi = config['ISI']['password']

#open dataset and get info:
csv_file = open(sys.argv[1], 'r')
dataset = open(sys.argv[1], 'rb')
file_path = sys.argv[1]
post_type = sys.argv[2]

#### ENDPOINTS
# ISI
if post_type == 'local':
    datamart_api_url = 'http://localhost:14080'   

else:
    datamart_api_url = f'https://{username_isi}:{password_isi}@dsbox02.isi.edu:8888/datamart-api-wm'

# NYU TBD

###############  WELCOME MESSAGE
print("\n")
print("WELCOME TO THE T2WML ANNOTATER AND DATASET REGISTRATION TOOL")

# get meta Data from user
dataset_meta = isi.get_dataset_meta()

# Post meta data to ISI
posted_meta = isi.post_meta_to_api(dataset_meta, datamart_api_url)

# Update Excel Workbook to have correct dataset_id
workbook = load_workbook(filename=file_path)
sheet = workbook.active
sheet["B1"].value = dataset_meta["dataset_id"]
workbook.save(filename="csv/tmp.xlsx")

# Upload dataset to T2WML
url = f'{datamart_api_url}/datasets/{dataset_meta["dataset_id"]}/annotated'
file_path = 'csv/tmp.xlsx'
upload_data_post(file_path, url)

# Get variable(s)
response = get(f'{datamart_api_url}/metadata/datasets/{dataset_meta["dataset_id"]}/variables')
variable_ids = [i.get('variable_id') for i in response.json()]

# Download data in canonical form
df_all_variables = None
for v in variable_ids:
    response = get(f'{datamart_api_url}/datasets/{dataset_meta["dataset_id"]}/variables/{v}')
    df = pd.read_csv(StringIO(response.text)).set_index('time')
    if df_all_variables == None:
        df_all_variables = df
    else:
        cols_to_use = df.columns.difference(df_all_variables.columns)
        df_all_variables = merge(df_all_variables, df[cols_to_use], left_index=True, right_index=True, how='outer')

df_all_variables.reset_index().to_csv('csv/tmp.csv')

# Upload to NYU
#login to wm auctus
api_url = f'https://{username_nyu}:{password_nyu}@wm.auctus.vida-nyu.org/api/v1/'
url_upload = api_url + 'upload' 
url_meta = api_url + 'metadata/'

# Upload to datamar
dataset = open('csv/tmp.csv', 'rb')
dataset_id = nyu.upload_data(url_upload, dataset, dataset_meta["name"], dataset_meta["description"])

#...wait for good response
print("Registering your dataset, this may take awhile...")
with sp.Spinner():
    nyu.get_status(url_meta, dataset_id)