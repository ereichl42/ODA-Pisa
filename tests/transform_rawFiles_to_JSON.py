import json

# This file contains functions to transform raw data files into JSON formats.
# Another functions stores the JSON as file in the data folder.


def transform_pisa_to_json(pisa_data):
    # TODO: Add the transformation logic. Lookup the defined JSON structure in the templates folder.
    return json.dumps(transformed_data)


def transform_expenditure_to_json(expenditure_data):
    # TODO: Add the transformation logic. Lookup the defined JSON structure in the templates folder.
    return json.dumps(transformed_data)


def save_json_to_file(data, file_path):
    # TODO: Figure out if paths should be defined in this file or somewhere else in the project.

    # Save the JSON data to the specified file path
    with open(file_path, 'w') as file:
        file.write(data)
