"""
This modules contains the functionalities and classes for the following utilites:
 1. creating a json file for the parameters sets in this repository. This
"""

__author__ = "Moin Ahmed"
__copyright__ = "Copyright 2023 by SPPy. All rights reserved."

import os
import csv
import json

import SPPy

# BASEDIR_CSV = os.path.join('..', '..', 'SPPy', 'parameter_set')
print(__file__)
BASEDIR_CSV: str = os.path.join('..', 'parameter_sets')
DICT_FILENAMES: dict = {'param_battery-cell.csv': 'bc',
                        'param_electrolyte.csv': 'sep',
                        'param_neg-electrode.csv': 'n',
                        'param_pos-electrode.csv': 'p'}  # contains the filenames and their types


def get_dict_params(filepath_to_csv: str, dict_params: dict, filetype: str) -> dict:
    """
    Returns a dict containing the parameters in a csv file. The dictionary key/ value pair are the
    parameter names/values.
    """
    with open(filepath_to_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        for i, row in enumerate(csv_reader):
            if i != 0:
                if len(row[0].split(' [')) >= 2:
                    param_name: str = row[0].split(' [')[0] + f"_{filetype} [" + row[0].split(' [')[-1]  # the string split
                    # is to add the filetype as parameter name_{file type} [units]
                else:
                    param_name: str = row[0] + f"_{filetype}"
                param_value: float = row[1]
                dict_params[param_name] = param_value
    return dict_params


def get_csv_filepath(parameter_name: str, csv_filename: str) -> str:
    """
    Returns the filepath to the csv file given the parameter name and csv file name.
    """
    return os.path.join(BASEDIR_CSV, parameter_name, csv_filename)


def create_dict_parameterset() -> dict:
    """
    Returns a dict containing the information for all the parameter information. The key contains the parameterset name
    and the value is a dict containing the key/value as parameter name (in strings)/parameter value (in strings).
    """
    dict_parameter_set: dict = {}  # creates and empty dict for the json file.
    # iterate over all the filenames in the parameter sets directories
    lst_parameterset_names: list = SPPy.battery_components.parameter_set_manager.ParameterSets.list_parameters_sets()
    dict_final: dict = {}
    for parameterset_name in lst_parameterset_names:
        # in the following, for each file create a dictionary containing parameter values
        dict_params: dict = {}  # intended to store all parameters for the a parameterset
        for filename in DICT_FILENAMES.keys():  # for each above iteration iterate over all files
            filepath: str = os.path.join(BASEDIR_CSV, parameterset_name, filename)
            filetype: str = DICT_FILENAMES[filename]
            try:
                param_dict = get_dict_params(filepath_to_csv=filepath, dict_params=dict_params, filetype=filetype)
            except FileNotFoundError as e:
                print(e)
        dict_final[parameterset_name] = param_dict
    return dict_final


def save_json_file(filepath_to_json: str) -> None:
    with open(filepath_to_json, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(create_dict_parameterset(), indent=4))


save_json_file('static/parameter_sets.json')
