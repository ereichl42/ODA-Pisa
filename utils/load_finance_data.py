import json
import os
import re
import numpy as np
import pandas as pd
import io


def load_financial_data(file_path):
    """
    Load and process the expenditure data from a TSV file.

    Args:
    - file_path (str): The path to the TSV file.

    Returns:
    - pd.DataFrame: Processed expenditure data in long format.
    """
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return None

    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process the lines to replace commas with tabs only in the first few columns
    processed_lines = []
    for line in lines:
        # Replace commas with tabs only in the first few columns (before the year columns)
        processed_line = line.replace(',', '\t', 4)
        processed_lines.append(processed_line)

    # Combine the processed lines into a single string
    processed_content = ''.join(processed_lines)

    # Use StringIO to read the processed content into a pandas DataFrame
    data = pd.read_csv(io.StringIO(processed_content), delimiter='\t')

    # Melt the DataFrame to make it easier to filter
    data_melted = pd.melt(data, id_vars=[
                          "freq", "unit", "isced11", "geo\\TIME_PERIOD"], var_name="Year", value_name="Expenditure")

    # Rename the columns for easier access
    data_melted.columns = ["Frequency", "Unit",
                           "Education_Level", "Country", "Year", "Expenditure"]

    # For easier handling, all country names are converted to country codes
    with open('data/reference/country_codes.json', 'r') as f:
        country_codes = json.load(f)
        country_codes = country_codes['countries']

    # Filter out all countries not listed in the country codes list (which is OECD countries)
    data_melted = data_melted[data_melted['Country'].isin(
        country_codes.values())]

    # Return processed data as a DataFrame
    return data_melted


def transform_financial_data_to_JSON(data):
    """
    Transform the cleaned up financial data to a nested JSON structure according to the defined template.

    Args:
    - data (pd.DataFrame): The cleaned up financial data.

    Returns:
    - dict: The financial data in a nested JSON structure.
    """
    # I take a copy of the JSON template structure
    template_path = "data/templates/financial_dataset_template.json"
    with open(template_path, 'r') as f:
        financial_results = json.load(f)

    # First the data is filtered since we are only interested certain education levels.
    education_levels_of_interest = ["ED01", "ED02", "ED1", "ED2", "ED3"]
    data = data[data["Education_Level"].isin(education_levels_of_interest)]

    # Also, there are lots of non-numeric and mixed values in the Expenditure column.
    # Use function to clean up mixed values and replace all non-numeric values with NaN
    data["Expenditure"] = data["Expenditure"].apply(process_value)
    # Remove rows with NaN values
    data = data.dropna(subset=["Expenditure"])

    # Remove the example data which was included in the template. The metadata is kept.
    financial_results["countries"] = {}

    # Group the data of dataframe by country and year, then iterate over the groups
    grouped = data.groupby(["Country", "Year"])
    for (country, year), group in grouped:
        # Convert year to string for JSON compatibility, with no whitespaces
        year = str(year).strip()

        # Check if the country and year are already in the JSON structure, if not, add them with empty dictionaries
        if country not in financial_results["countries"]:
            financial_results["countries"][country] = {}
        if year not in financial_results["countries"][country]:
            financial_results["countries"][country][year] = {}

        # Iterate over the rows in each group and add the data to the JSON structure
        for _, row in group.iterrows():
            education_level = row["Education_Level"]
            expenditure = row["Expenditure"]
            financial_results["countries"][country][year][education_level] = expenditure

    # Return the JSON data
    return financial_results


def filter_financial_data(data, country=None, education_levels=None, start_year=None, end_year=None):
    """
    Filter the raw expenditure data based on given parameters.

    Args:
    - data (pd.DataFrame): The expenditure data.
    - country (str, optional): The country code.
    - education_levels (list, optional): List of education levels to filter.
    - start_year (int, optional): The start year for the filter. If end_year is None, this will be the only year.
    - end_year (int, optional): The end year for the filter.

    Returns:
    - pd.DataFrame: Filtered expenditure data.
    """
    filtered_data = data.copy()

    if country is not None:
        filtered_data = filtered_data[filtered_data["Country"] == country]

    if education_levels is not None:
        filtered_data = filtered_data[filtered_data["Education_Level"].isin(
            education_levels)]

    if start_year is not None:
        if end_year is None:
            # only filter for that year
            end_year = start_year

        filtered_data = filtered_data[
            (filtered_data["Year"].astype(
                int).between(start_year, end_year))
        ]
    else:
        # All years
        pass

    return filtered_data


def process_value(value):
    """
    Process the value of the expenditure data to a float. Replaces all non-numeric values with NaN.

    Args:
    - value (str): The value of the expenditure data.

    Returns:
    - float: The processed value.
    """
    try:
        # Most instances are normal values, so this will be checked first
        return float(value)
    except ValueError:
        # For all other cases, which are sometimes mixed values, regex is used
        if isinstance(value, str):
            match = re.search(r'\d+\.\d+', value)
            if match:
                return float(match.group())
            else:
                return np.nan
        else:
            return np.nan


def update_financial_data(file_path, json_path=None, updateDate=None):
    """
    Update the the JSON file of the corresponding raw data file.

    Args:
    - file_path (str): The path to the TSV file.
    - json_path (str, optional): The path to the JSON file. If None, the default path is used with new date.
    - updateDate (DateTime, optional): The date of the update.

    Returns:
    - bool: True if the JSON file was updated successfully, False otherwise.
    """

    # Check if the file exists
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return False

    inputFile_name = os.path.basename(file_path)
    dataset_name = inputFile_name.replace(".tsv", "")
    metadata_name = dataset_name + "_metadata.json"
    metadata_path = "data/financial_data/original_tsv_source/" + metadata_name

    if json_path is None:
        outputFile_name = dataset_name + ".json"
        json_path = "data/financial_data/" + outputFile_name

    if updateDate is None:
        updateDate = pd.Timestamp.now()

    # Load the data
    data = load_financial_data(file_path)
    if data is None:
        return False

    # Transform the data to the JSON structure
    financial_results = transform_financial_data_to_JSON(data)

    # Edit the metadata of the JSON file
    # Get some important metadata out of the metadata files
    with open(metadata_path, 'r') as f:
        metadata_ref = json.load(f)

    # Only if the file does not exist yet.
    if not os.path.exists(json_path):
        financial_results["metadata"]["type"] = "Public Expenditure on Education ??"
        financial_results["metadata"]["description"] = metadata_ref["description"]
        financial_results["metadata"]["unit"] = "???"
    else:
        # Replace the metadata of the new JSON file with the old one
        with open(json_path, 'r') as f:
            oldFile = json.load(f)
        financial_results["metadata"] = oldFile["metadata"]

    financial_results["metadata"]["update"] = updateDate.strftime(
        "%Y-%m-%d")

    # Write the JSON file
    with open(json_path, 'w') as f:
        json.dump(financial_results, f, indent=2)

    return True


def update_all_financial_data():
    """
    Update all the JSON files of the financial data.
    """
    path_original_tsv_files = "data/financial_data/original_tsv_source"
    files_to_update = []
    for file in os.listdir(path_original_tsv_files):
        if file.endswith(".tsv"):
            file_path = os.path.join(path_original_tsv_files, file)
            files_to_update.append(file_path)

    for file_path in files_to_update:
        update_financial_data(file_path)
        print("Updated:", file_path)


#### EXAMPLE USAGE ####
if __name__ == "__main__":
    file_path = "data/financial_data/original_tsv_source/educ_expenditure_gdp.tsv"
    # Check if the file exists
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        exit()
    expenditure_data = load_financial_data(file_path)

    if expenditure_data is not None:
        country = "AT"
        education_levels = ["ED0", "ED01"]
        start_year = 2012
        end_year = 2015

        filtered_expenditure_data = filter_financial_data(
            expenditure_data, country, education_levels, start_year, end_year)
        print(filtered_expenditure_data)

    # Test: Filter all expenditure data for Austria (AT) from year 2013
    filtered2 = filter_financial_data(
        expenditure_data, country="AT", start_year=2013)
    # Show only the column Education_Level and Expenditure, without the index column:
    print(filtered2[["Education_Level", "Expenditure"]].to_string(index=False)
          )

    # Get all possible values for the column Education_Level
    print(expenditure_data["Education_Level"].unique())

    # Transform the filtered data to a nested JSON structure
    financial_results = transform_financial_data_to_JSON(expenditure_data)
    print(json.dumps(financial_results, indent=2))

    # Update the JSON file of the corresponding raw data file
    update_all_financial_data()
