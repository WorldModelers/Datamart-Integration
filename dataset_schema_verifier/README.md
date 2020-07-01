## Schema Verifier
This repository houses code to verify a dataset's compliance with the datamart schema. There is a discussion on the schema, a tutorial video, and instructions on how to deploy the verifier script.

## Contents
1. [Overview](#overview)
2. [Tutorial Video](#tutorial-video)
3. [Verifier Overview](#verifier-overview)
4. [Correcting Errors](#correcting-errors)
5. [Run Instructions](#run-instructions)

### Overview:
 The information below identifies and explains the required and optional column headers, to include the proper naming convention per the datamart schema. For further information on the schema, <a href="https://docs.google.com/presentation/d/1n91lkhDc5XYGuYPQDLiodj4vYlR-pZ6d6_dgvnw-400/edit?usp=sharing">Click Here.</a>
  
  The following column headers are required:
  1. `timestamp` all lowercase and all timestamps in ISO 8601 format:
  
      - Date Only: `2020-06-30`
      - Date and time in UTC:	`2020-06-30T22:56:54+00:00` or
                              `2020-06-30T22:56:54Z` or
                              `20200630T225654Z`
  2. `country` all lowercase
  3. `feature_n_name` Feature of interest. This column should contain the value of the feature of interest. For example, if the feature is “crop price” then the column header should be “crop_price_name” (“_name” should be appended). Record values would be the actual price. At least one feature is required. 
  4. `feature_n_description` Description of the feature of interest. For example `crop_price_description` for the feature `crop_price`. Column header must associate to a `_name` feature. This description should be down-filled and will therefore be redundant.
  
   The following column headers are optional:
   1. `feature_n_units` Units associated with the “_name” feature. For example “crop_price_units” and $/kg as a value. 
   2. `feature_n_qualifier_z` Qualifiers are any additional metadata associated with a feature. There can be n of these, but they must be associated to the feature using the feature’s name. For example “crop_price_category” would be a category modifier for “crop price”
   3. `latitude` Latitude for the record.
   4. `longitude` Longitude for the record.
   5. `polygon` A polygon shape (geoJSON) for the record
   6. `country` Country associated with record using Wikidata as authoritative country list
   7. `admin_1` Admin_1 associated with record using Wikidata as authoritative Admin_1 list
   8. `admin_2` admin_2 associated with record using Wikidata as authoritative Admin_2 list
   9. `admin_3` admin_3 associated with record using Wikidata as authoritative Admin_3 list
   
### Tutorial Video
For a tutorial video that walks through an example of transforming a dataset into a schema-compliant dateset, <a href="https://drive.google.com/file/d/1RqgscMfhTWe2qt8qGm9RncEFvduJH5qq/view">Click Here.</a>

### Verifier Overview
  The script reads your headers and verifies compliance. It checks for: required column headers, dates in ISO 8601 format, and proper qualifier format. Note that the verifier script does account for case; i.e. `Country` will fail verification as it's capitalized.  
  
  The verifier will return the verification results with one of three flags:
  
  - `Passed`: Item of interest passed verification and is valid.
  - `WARNING`: Returns the column header that does not meet the column naming convention. A `WARNING` invalidates a dataset.
  - `FAILED`: Indicates a required column header or timestamp format is invalid (or not present). A `FAILED` invalidates a dataset.
  
  If all checks pass without a `WARNING` or `FAILED` flag, you are notified that the dataset is schema-compliant.

### Correcting Errors
If the verifier returns any `WARNING` or `FAILED` flags, the verifier specifically identifies what needs to be corrected.  Open your dataset, make the changes indicated from the output, and then re-run your dataset through the verifier. Once verfied schema-compliant, your dataset is ready for registration.

### Run Instructions:
The verifier.py script requires Python 3.7 or higher. No additional packages are needed. 

  1. Download `verifier.py`, `bad.csv`, and `good.csv` to `your_folder` on your local machine
  2. Open a Terminal window
  3. Change your working directory to your new folder: `cd /path/to/your_folder`
  4. Run the following CLI: 
  
        `python3 verifier.py file.csv` 
  
        where `file.csv` is your csv file. There are two examples included: `bad.csv` and `good.csv`. You can use these examples to test the functionality or test your own `.csv` file.
  
  5. The verification results are printed out to the terminal window. If you'd like to write them to a file, run: 
  
        `python3 verifier.py file.csv >> results.txt`  
