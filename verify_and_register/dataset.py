#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:04:37 2020
@author: travishartman
"""

import verifier as vlad
import nyu_register as nyu
import isi_register as isi
import spinner as sp
import configparser
import csv
import time
import sys
import os

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
print("WELCOME TO THE DATASET SCHEMA-VERIFICATION AND REGISTATION PORTAL")
print("Enter 1 to VERIFY your dataset schema compliance")
print("Enter 2 to REGISTER your dataset (requires schema-compliant dataset)")
choice = input("Selection: ")

if choice == '1':
    
    #list to hold all the dates
    dater=[]
    reader = csv.reader(csv_file)
    headers_list = next(reader, None)
    
    #build list of all the dates
    for a in csv.reader(csv_file, delimiter=','):
            dater.append(a[0])
    
    print(f"Press ENTER to verify your file: {csv_file.name.split('/')[-1]}")
    input()
    
    # Run the verifier module
    vlad.verification_results = vlad.wrapperitup(headers_list, dater)
    t=vlad.displayer(vlad.verification_results)


# RUN UPLOAD
if choice == '2':
    
    print("\n")
    print("Enter 1 to REGISTER dataset with NYU")
    print("Enter 2 to REGISTER with ISI")
    api = input("Selection: ")
    
    #NYU
    if api == '1':
        
        #list to hold all the dates
        dater=[]
        reader = csv.reader(csv_file)
        headers_list = next(reader, None)
        
        #build list of all the dates
        for a in csv.reader(csv_file, delimiter=','):
                dater.append(a[0])
        print(f"Press ENTER to verify your file: {csv_file.name.split('/')[-1]}")
        input()
        
        # Run the verifier module
        vlad.verification_results = vlad.wrapperitup(headers_list, dater)
        t=vlad.displayer(vlad.verification_results)
        
        if t == True:

            #login to wm auctus
            api_url = f'https://{username_nyu}:{password_nyu}@wm.auctus.vida-nyu.org/api/v1/'
            url_upload = api_url + 'upload' 
            url_meta = api_url + 'metadata/'
            
            # GET META
            dataset_name = input("Enter the Name of your Dataset: ")
            dataset_description = input("Provide a Description of your Dataset: ")
            
            print(f"Press ENTER to UPLOAD your file: {csv_file.name.split('/')[-1]}")
            input()
            
            # Upload to datamart
            dataset_id = nyu.upload_data(url_upload, dataset, dataset_name, dataset_description)
            
            #...wait for good response
            print("Registering your dataset, this may take awhile...")
            with sp.Spinner():
                nyu.get_status(url_meta, dataset_id)

    #ISI
    if api == '2':

        # get meta Data from user
        dataset_meta = isi.get_dataset_meta()
        
        # Post meta data to ISI
        posted_meta = isi.post_meta_to_api(dataset_meta, datamart_api_url)
        
        
        # VARIABLES
        # CONTINUE TO ADD VARIABLES UNTIL USER STOPS
        add_more =input("Do you want to add variables at this time? Enter 'yes' or 'no': " )
        variable_id_list= []
        
        while add_more.lower() == 'yes':
            
            new_variable_with_id = isi.define_new_variable(datamart_api_url, dataset_meta['dataset_id'])
            variable_id_list.append(new_variable_with_id)
            
            add_more = input("Do you want to add another variable? Enter 'yes' or 'no'': ")

        #DATA
        enter_data =  input("Do you want to add your data to your variable now? Enter 'yes' or 'no': ")    
          
        if enter_data.lower()  == 'yes':
            
            # Post DATA TO VARIABLES ISI Datamart: Given option to overwrite or append
            put_or_post = input("Do you want to append your new data to the dataset or overwrite the existing data. Enter append or overwrite: ")    
            
            if put_or_post.lower() == 'append':
                overwrite=False
            if put_or_post.lower() == "overwrite":
                overwrite=True
            
            print("You just created the following dataset variables:")
            for var in variable_id_list:
                print(var)
               
            print("\n Here are the dataset variables available:")    
            isi.print_all_dataset_variables(datamart_api_url, dataset_meta['dataset_id'])    
                
            variable_id = input("What dataset variable are you uploading data to? Enter the variable_id: " )
            
            with sp.Spinner():
                print(f"Uploading data to: {variable_id}")    
                isi.upload_data(datamart_api_url, file_path, dataset_meta['dataset_id'], variable_id, overwrite=put_or_post)
            
            #Display dataframe
            show_it = isi.show_dataset(datamart_api_url, dataset_meta['dataset_id'], variable_id)
        
        #Not adding data at this time...
        else:
            print(f"Your variable {variable_id} is available to be written to later")