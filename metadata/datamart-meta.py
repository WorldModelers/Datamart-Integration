#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:59:46 2020

@author: brandonrose
"""

import requests
import configparser
import json
from datetime import datetime
import shutil
import os
from glob import glob

config = configparser.ConfigParser()
configFile = 'config.ini'
config.read(configFile)

username_nyu = config['NYU']['username']
password_nyu = config['NYU']['password']

username_isi = config['ISI']['username']
password_isi = config['ISI']['password']

ISI_meta_file = 'ISI_metadata.jsonl'
NYU_meta_file = 'NYU_metadata.jsonl'

# Delete prior metadata files
if os.path.exists(ISI_meta_file):
    os.remove(ISI_meta_file)
if os.path.exists(NYU_meta_file):
    os.remove(NYU_meta_file)

# =============================================================================
# Process ISI Metadata
# =============================================================================
ISI_url= f'https://{username_isi}:{password_isi}@dsbox02.isi.edu:8888/datamart-api-wm'
isi_datasets = requests.get(f'{ISI_url}/metadata/datasets').json()

isi_vars = []
for d in isi_datasets:
    variables = requests.get(f'{ISI_url}/metadata/datasets/{d["dataset_id"]}/variables').json()
    for v in variables:
        var_obj = {'dataset_name': d['name'],
                   'dataset_id': d['dataset_id'],
                   'dataset_description': d['description'],
                   'dataset_url': d['url']}
        var_obj['variable_id'] = v['variable_id']
        var_obj['variable_name'] = v.get('name', '')
        isi_vars.append(var_obj)
        with open(ISI_meta_file,'a') as f:
            f.write(json.dumps(var_obj)+'\n')


# =============================================================================
# Process NYU Metadata
# =============================================================================
date = datetime.today().strftime("%Y%m%d")
NYU_url = f'https://{username_nyu}:{password_nyu}@wm.auctus.vida-nyu.org/snapshot-wm/index.{date}.tar.gz'
r = requests.get(NYU_url, allow_redirects=True)
open('tmp.tar.gz', 'wb').write(r.content)
shutil.unpack_archive('tmp.tar.gz','nyu_files')
os.remove('tmp.tar.gz')

nyu_datasets = []
NYU_files = glob('nyu_files/datamart**')
for f in NYU_files:
    with open(f,'r') as fi:
        d = json.loads(fi.read())
        data_obj = {'dataset_name': d.get('name',''),
                    'dataset_id': d['id'],
                    'dataset_source': d['source']}
        with open(NYU_meta_file,'a') as fo:
            fo.write(json.dumps(data_obj)+'\n')
        nyu_datasets.append(data_obj)

shutil.rmtree('nyu_files')