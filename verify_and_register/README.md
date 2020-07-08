## Verify schema and register dataset
This repository houses code to 1) verify a dataset's compliance with the datamart schema and 2) register the dataset with either the NYU or ISI datamart. Below is an overview of the verification and registration processes.

## Contents
1. [Overview](#overview)
2. [Tutorial Video](#tutorial-video)
3. [Verifier Overview](#verifier-overview)
4. [Correcting Errors](#correcting-errors)
5. [Registration Overview](#registration-overview)
6. [Run Instructions](#run-instructions)

### Overview:

#### NOTE: SCHEMA CHANGE AS OF 07 JULY 2020. Changes include:
   - `feature_1_name` is now `feature_value`
   - `feature_1_units` is now `feature_1_unit`
   - `timestamp` is now `time`
   
   For the latest canonical Data-Normalization-Schema, <a href="https://docs.google.com/spreadsheets/d/1BI0hsomtAyuzDTwc-7EgDxx8y1uTpsmeGWaEEPUGCXc/edit#gid=0">Click Here.</a> For further information on the schema and its development, <a href="https://docs.google.com/presentation/d/1n91lkhDc5XYGuYPQDLiodj4vYlR-pZ6d6_dgvnw-400/edit?usp=sharing">Click Here.</a>
 
 
  The following column headers are required:
  1. `time` all lowercase and all times in ISO 8601 format:
  
      - Date Only: `2020-06-30`
      - Date and time in UTC:	`2020-06-30T22:56:54+00:00` or
                              `2020-06-30T22:56:54Z` or
                              `20200630T225654Z`
  2. `country` all lowercase
  3. `feature_value` Feature of interest. This column should contain the value of the feature of interest. For example, if the feature is “crop price” then the column header should be “crop_price_value” (“_value” should be appended). Record values would be the actual price. At least one feature is required. 
  4. `feature_n_description` Description of the feature of interest. For example `crop_price_description` for the feature `crop_price`. Column header must associate to a `_value` feature. This description should be down-filled and will therefore be redundant.
  
   The following column headers are optional:
   1. `feature_n_unit` Units associated with the “_name” feature. For example “crop_price_units” and $/kg as a value. 
   2. `feature_n_qualifier_z` Qualifiers are any additional metadata associated with a feature. There can be n of these, but they must be associated to the feature using the feature’s name. For example “crop_price_category” would be a category modifier for “crop price”
   3. `latitude` Latitude for the record.
   4. `longitude` Longitude for the record.
   5. `polygon` A polygon shape (geoJSON) for the record
   6. `country` Country associated with record using Wikidata as authoritative country list
   7. `admin_1` Admin_1 associated with record using Wikidata as authoritative Admin_1 list
   8. `admin_2` admin_2 associated with record using Wikidata as authoritative Admin_2 list
   9. `admin_3` admin_3 associated with record using Wikidata as authoritative Admin_3 list
   
### Tutorial Video: 
#### Note, tutorial video not updated to reflect schema changes; however, the same processes apply

For a tutorial video that walks through an example of transforming a dataset into a schema-compliant dateset, <a href="https://drive.google.com/file/d/1RqgscMfhTWe2qt8qGm9RncEFvduJH5qq/view">Click Here.</a>

### Verifier Overview
  The script reads your headers and verifies compliance. It checks for: required column headers, dates in ISO 8601 format, and proper qualifier format. Note that the verifier script does account for case; i.e. `Country` will fail verification as it's capitalized.  
  
  The verifier will return the verification results with one of three flags:
  
  - `Passed`: Item of interest passed verification and is valid.
  - `WARNING`: Returns the column header that does not meet the column naming convention. A `WARNING` invalidates a dataset.
  - `FAILED`: Indicates a required column header or time format is invalid (or not present). A `FAILED` invalidates a dataset.
  
  If all checks pass without a `WARNING` or `FAILED` flag, you are notified that the dataset is schema-compliant.

### Correcting Errors
If the verifier returns any `WARNING` or `FAILED` flags, the verifier specifically identifies what needs to be corrected.  Open your dataset, make the changes indicated from the output, and then re-run your dataset through the verifier. Once verfied schema-compliant, your dataset is ready for registration.

### Registration Overview
There are two datamarts available to register your dataset: NYU and ISI.  The schema-verification discussed above is for the NYU datamart; ISI provides its own internal schema check and returns instructions to fix flagged items.

Below is a walk-through of the selections available to you after running the script (see next section: Run Instructions).
 
 1. Verify or Register Selection:
     ```
     WELCOME TO THE DATASET SCHEMA-VERIFICATION AND REGISTATION PORTAL
     Enter 1 to VERIFY your dataset schema compliance
     Enter 2 to REGISTER your dataset (requires schema-compliant dataset)
     ``` 
    
    - Enter 1: If you only want to verify your schema for a `csv` dataset intended for an NYU upload. See the Verifier Overview section above for further discussion.
   
    - Enter 2: This option allows you to A) verify and register a `csv` to NYU datamart, or B) register a dataset, create dataset variables, and upload data to ISI datamart.

2. NYU or ISI:
    ```
    Enter 1 to REGISTER dataset with NYU
    Enter 2 to REGISTER with ISI
    ```
    - Enter 1: Your dataset will automatically be verified for schema compliance. If successful, you can press `ENTER` to upload your dataset. Following a successful upload, both a url and dataset ID are provided: go to the url and verify upload by searching for your dataset ID.
    
    - Enter 2: The schema verification script is not run over your file; ISI will verify compliance. <a href="https://datamart-upload.readthedocs.io/en/latest/download/">Click Here</a> for a detailed schema overview. After entering "2", the following meta data information is requested:
    
        ```
        Enter Dataset Name: Enter the name of your dataset
        Enter Dataset ID: test_id
        Enter Dataset Description: Add your description
        Enter Dataset Source: usually the url that links to your data
        ```
        You may put in an existing `Dataset ID`. You will get the error message below, but if you want to add variables to an existing dataset, you can ignore the error and continue.
        
        ```
        {
        "Error": "Dataset identifier test_id has already been used"
        }
        ```
        
        Next, you will have the option to add variables.  This is NOT where you add data. 
        
        ```
        Do you want to add variables at this time? Enter 'yes' or 'no': yes
        ```
     - Enter `yes` to add your variable as a column header to your dataset. You can add as many variables as you want:
        ```
        Enter Variable Name: test
        Enter Variable ID: test
        ```
        
     - Enter `no` to move you to the next step.
        
     Once all variables are added, you can upload the data to the ISI datamart:
     ```
     Do you want to add your data to your variable now? Enter 'yes' or 'no': 
     ```
     - Enter `no` to exit the program. Your now have a dataset and dataset variables that data can be uploaded to at another time.
     - Enter `yes` to add your data to your dataset. The data are from the `csv` file you include on the command line (see Run Instructions). Entering `yes` gives you the option to override the data currently in the dataset or append the data. It is recommended to append the data unless you are very familiar with the dataset:
     
     ```
     Do you want to append your new data to the dataset or overwrite the existing data. Enter append or overwrite: 
     ```
     
     After selecting to append or overwrite the variables you <i>just</i> added and <i>all</i> the variables for the dataset are displayed.  You can use this as reference to complete the next option below; ensure that you enter the <b>`variable_id`</b>:
     ```
     What dataset variable are you uploading data to? Enter the variable_id: test_variable_id
     ```
     Hit enter and the ISI api will verify compliance. You will be notified if 1) the data is successfully uploaded, or 2) there are errors that need to be corrected.
     
        
### Run Instructions:
The dataset.py script requires Python 3.7 or higher. Non-standard python packages are required and included in the `requirements.txt` file in this repository.

For those using conda environments:
  1. Create a new conda environment: `conda create --name schema` where `schema` is your name of choice.
  2. Install packages: `conda install --yes --file requirements.txt`

If you are not using a virtual environment, you can use `python -m pip install <package>` while referencing the `requirements.txt` file.
  
After installing the required python packages:
  1. Download the `verify_and_register` folder from this repository to `your_folder` on your local machine
  2. Open a Terminal window
  3. Change your working directory to your new folder: `cd /path/to/your_folder`
  4. Run the following CLI: 
  
        `python3 dataset.py csv/file.csv` 
  
        where `file.csv` is your csv file. There are two examples included: `bad.csv`, `good.csv`. You can use these examples to test the functionality or test your own `.csv` file. Note that the csv files are stored in a sub-folder.  It's recommended, but not necessery, to put your csv file in the `csv` folder.
  
  5. Follow the steps as discussed above in the Registration Overview.
