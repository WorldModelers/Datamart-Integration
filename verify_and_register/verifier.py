#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:30:20 2020

@author: travishartman
"""

import csv
import sys
import datetime
from datetime import datetime

# read in the csv file
csv_file = open(sys.argv[1], 'r')
#csv_file=open('/Users/travishartman/Desktop/schema/working_folder/csv/datamart_schema.csv', 'r')
 
#list to hold all the dates
dater=[]
reader = csv.reader(csv_file)
headers_list = next(reader, None)

for a in csv.reader(csv_file, delimiter=','):
    dater.append(a[0])

#### FUNCTIONS ####

#verify that 'country' is in the header
def verify_country(headers_list):

    country = False
    
    if "country" in headers_list:
        country = True
        
    return country    

# Verify that 'time' is in the header
def verify_time(headers_list):
    
    stamp = False
    
    if "time" in headers_list:
        stamp = True
        
    return stamp

# Verify date FORMAT
def verify_time_format(dt_str):
    
    last_one = dt_str[-1]
    
    if last_one == "Z" or last_one == "z":
        dt_str = dt_str[:-1]

    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    
    return True

# get all the features listed in the dataset
def get_features(headers_list):
    
    feature_list=[]
    
    for header in headers_list:
        if "_value" in header:
            feature_list.append(header.split("_value")[0])
    
    return feature_list

#Function to add key,value pairs without overwriting existing info
def set_key(dictionary, key, value):
    
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

# Create dictionary to add k.v of features and any associated atrributes for that feature
def get_feature_attr(feature_list, headers_list):
    
    header_dict ={}
    
    for feature in feature_list:
        for thing in headers_list:
            if feature in thing:
                set_key(header_dict, feature, thing)
                 
    return header_dict

# Check that 'description' is in the dataset for each feature
def verify_description(header_dict):
    
    list_bool=[]
    
    for key in header_dict:
        temp_bool = False
        temp_list = header_dict[key]
        
        for thing in temp_list:
            if 'description' in thing:
                temp_bool = True
        
        list_bool.append([key, temp_bool])
        
    return list_bool 

# Check for and return any differences in the dateset header versus the header columns that are accounted for
# Used to ID any column headers that are non-schema comforming
def the_accounter(headers_list):
    
    not_accounted_for = []
    if verify_time(headers_list) == True:
        not_accounted_for.append("time")
    if verify_country(headers_list) == True:
        not_accounted_for.append("country")
    
    # get all the feautures and attributes
    things = get_feature_attr(get_features(headers_list), headers_list)
    
    for key in things:
        for thing in things[key]:
            not_accounted_for.append(thing)
        
    return (list(set(headers_list) - set(not_accounted_for)))

#Put it all together
def wrapperitup(headers_list, dater):
    
    #populate with function outputs
    country = verify_country(headers_list) 
    time_stamp = verify_time(headers_list)
    features_list = get_features(headers_list)
    header_dict = get_feature_attr(features_list, headers_list)
    descr_list = verify_description(header_dict)
    diff = the_accounter(headers_list)
    
    #features_in_set => [test if any features, number of features, list of features]
    
    holder_of_meta = {'qualifier': header_dict,
                      'country_in': None, 
                      'time_in': None, 
                      'time_format': None, 
                      'features_in_set': [None,0,None], 
                      'desc_for_feature':None,
                      'header_diff': diff}
    
    # COUNTRY CHECK --> Boolean
    holder_of_meta['country_in'] = country   
    
    # TIME CHECK --> Boolean
    holder_of_meta['time_in'] = time_stamp
    
    #  TIME FORMAT--> Boolean
    list_date_bool = []
    for t in dater:
        list_date_bool.append(verify_time_format(t))
    
    holder_of_meta['time_format'] = all(list_date_bool)    
    
    #  CHECK FOR the NAME TAG--> feature_list
    if len(features_list) > 0:
        holder_of_meta['features_in_set'][0] = True
        holder_of_meta['features_in_set'][1] = len(features_list) 
        holder_of_meta['features_in_set'][2] = features_list
    
    #  CHECK FOR DESCRIPTION --> header_dict
    holder_of_meta['desc_for_feature'] = descr_list
    
    
    return holder_of_meta

# Display the results
def displayer(holder_of_meta):

    # Lists to hold the fails/good to gos
    success = []
    fail = []
    warn = []
    verifier_status = False
    
    print("Checking your file for schema compliance..." +  "\n")
    
    # Check if there are any features first!
    temp = holder_of_meta['features_in_set']
    temp_q = holder_of_meta['qualifier']

    if temp[1] == 0:
        fail.append('Failed scan for features --> NO FEATURES FOUND')
        fail.append('Update your feature header to include the "_value" tag')
        fail.append('Example: change crop_price to crop_price_value')
    # Ok, there are features so run the rest of the verification
    else:
        for key in temp_q:
            
            if isinstance(temp_q[key], list):
                print(f"Found Feature: {key} with {len(temp_q[key])-1} qualifier(s)")
                for q in temp_q[key][1:]:
                    print(f"    Qualifier: {q}")
            else:
                print(f"Found Feature: {key} with ZERO qualifiers")
                
        print('\n')
        print(f"Found {temp[1]} total feature(s)") 	
        print(f"If you have more than {temp[1]} feature(s), verify your feature has the '_value' tag" + '\r\n')

        # Stock strings for print out messages	
        yes = 'Passed: '	
        nope = 'FAILED ' 	
        maybe = 'WARNING '	
        v = ' verified'	
 	
        # Allowable headers, if these are in the dataset, the verifier will ignore them since they are optional/allowed
        schema_nulls = ['latitude', 'longitude', 'polygon', 'admin_1', 'admin_2', 'admin_3']
		
        # Pull out data from dictionary for display to user	
        # Any unrecognized headers...
        temp = holder_of_meta['header_diff']
        if temp == True:
            success.append(yes + 'header accounting' + v)
        else:
            for thing in temp:
                if thing not in schema_nulls:
                    warn.append(maybe + "--> Unrecognized column header: '" + thing + "'")  
        
        #COUNTRY
        temp = holder_of_meta['country_in']
        if temp == True:
            success.append(yes + 'country' + v)
        else:
            fail.append(nope + "--> 'country' is a required column header")   

        #TIME
        temp = holder_of_meta['time_in']
        if temp == True:
            success.append(yes + 'time' + v)
        else:
            fail.append(nope + "--> 'time' is a required column header")         

        #TIME FORMAT
        temp = holder_of_meta['time_format']
        if temp == True:
            success.append(yes + 'time format' + v)
        else:
            fail.append(nope  + "-->  Format for 'time' must be ISO 8601")
       
        #FEATURE DESCRIPTION
        temp = holder_of_meta['desc_for_feature']
        for t in temp:
            if t[1] == True:
                success.append(yes +"Description verified for feature: " + t[0])
            else:
                fail.append(nope + '-->  No Description found for feature: ' + t[0])
    
    # Print out the results:  
    if success != []:
        for s in success:
            print(s)
        print('\n')

    if warn != []:
        for w in warn:
            print(w)
        print('* Required column headers: feature_n_value, feature_n_description, time, country')
        print('* Optional column headers: feature_n_value_unit, latitude, longitude, polygon, admin_1, admin_2, admin_3')
        print('* Qualifier column headers: feature_n_<qualifier_here>. Example: feature = crop_price --> qualifier = crop_price_currency') 
        
        # If warnings and no fails
        if fail == []:
            print('\n')
            print("YOUR FILE IS NOT SCHEMA-COMPLIANT. CORRECT THE WARNINGS AND RE-RUN")
            print('\n') 

    if fail != []:
        print('\n') 
        for f in fail:
            print(f)   
        print('\n')
        print("YOUR FILE IS NOT SCHEMA-COMPLIANT. CORRECT THE VERIFICATION FAILURES AND/OR WARNINGS AND RE-RUN")
        print('\n')     

    if fail == [] and warn == []: 
        verifier_status = True
        print("YOUR DATASET IS SCHEMA-COMPLIANT AND READY FOR REGISTRATION")
        
    
    return verifier_status


# call functions and display results
verification_results = wrapperitup(headers_list, dater)
displayer(verification_results)


