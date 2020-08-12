# T2WML Processing and Datamart Registration

This document outlines how to use the [T2WML registration script](https://github.com/WorldModelers/Datamart-Integration/blob/master/verify_and_register/t2wml_register.py). This script is designed to take in an annotated spreadsheet, run it through T2WML, and ensure that the output is registered to both the ISI and NYU Datamarts.

## Requirements

Install the requirements with `pip3 install -r requirements.txt`

## Configuration

You should ensure that `config.ini` has the appropriate usernames/passwords for each Datamart.

## Usage

To use the script, point it at an annotated spreadsheet with:

```
python3 t2wml_register.py path_to_spreadsheet.xlsx
```

You will be asked to provide metadata about the dataset, such as a description and source (url).



