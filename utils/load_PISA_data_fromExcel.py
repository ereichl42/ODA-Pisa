import datetime
import os
import pandas as pd
import json


def load_PISA_data_fromExcel(file_path):
    """
    Load and process the PISA data from an Excel file with multiple tabs.

    Args:
    - file_path (str): The path to the Excel file.

    Returns:
    - dict: A dictionary with the type of results as the key and the data as a pandas DataFrame.
    Each DataFrame contains the data for one type of results (math, reading, science).
    The dataframe's columns are: 'Year', 'Country', 'Average', 'Standard Error'.
    """

    # Test if path exists
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return None

    # Read the Excel file, figure out how many tabs
    # Tab names need to be stored to access later
    xls = pd.ExcelFile(file_path)
    tabs = xls.sheet_names

    # The combined excel files with multiple tabs contain the data but with additional info.
    # The data does not start with first cell in each tab. Thus, searching for certain info and the actual data is needed.

    # There are types of results which are here defined as keywords.
    keywords = ['math', 'reading', 'science']
    # The header of the data is known too and can be used to search for the actual data
    header = ['Year/Study', 'Jurisdiction', 'Average', 'Standard Error']

    data = {}
    for tab in tabs:
        df = pd.read_excel(file_path, sheet_name=tab)

        # In the first few lines of each tab there is always a description if the data is about math, reading, or science
        # Search for the type of results
        resultType = None
        header_row = None
        end_row = None

        # I combine everything in one loop, and just check if resultType was already found
        for i, row in df[:].iterrows():
            if resultType == None:
                for keyword in keywords:
                    if row.str.contains(keyword, case=False).any():
                        resultType = keyword
                        break

                # Some safety check, just in case the online source of the file changed its format
                if i > 10:
                    print('ERROR: No info found in tab:', tab,
                          'Maybe the downloaded files is faulty!')
                    return None

            # If the resultType is already found, then search for the header of the data
            elif header_row == None:
                # Check if the header of the actual table is in the row
                # Assuming that the online source might change the header a bit,
                # I just check that at least two words from the header are in the row
                keywordsFound = 0
                for keyword in header:
                    if row.str.contains(keyword, case=False).any():
                        keywordsFound += 1
                if keywordsFound >= 2:
                    header_row = i

                # Some safety check, just in case the online source of the file changed its format
                if i > 15:
                    print('ERROR: Header not found in tab:', tab,
                          'Maybe the downloaded files is faulty!')
                    return None

            # If the header is found, then search for the end of the data - an empty row
            elif row.str.contains('nan', case=False).all():
                end_row = i
                break
        # Some safety check, just in case the online source of the file changed its format
        # It could be that now there is no empty row at the end of the data but instead the data ends at the end of the tab
        if end_row is None:
            end_row = i

        # Extract the actual data with additional cleanup, in the following steps:
        # 1. Extract data from below the header row to the end row.
        df_clean = df[header_row+1:end_row]
        # 2. Drop the columns with NaN values (probably empty columns in the beginning and end of the data)
        df_clean = df_clean.dropna(axis=1, how='all')
        # 3. Reset the index
        df_clean = df_clean.reset_index(drop=True)
        # 4. Define a proper header for the dataframe with clear names
        newNames = ['Year', 'Country', 'Average', 'Standard Error']
        df_clean.columns = newNames

        # This is now a almost clean dataframe, extracted from the Excel file as it was.
        # However, the year is only given once in the beginning of the data till the next year is given.
        # Thus, I fill up the NaN values in the 'Year' column with the previous value.
        df_clean['Year'] = df_clean['Year'].fillna(method='ffill')

        ## Country Names - Country Codes ##
        # Türkiye creates problems, it is replaced with Turkey
        df_clean['Country'] = df_clean['Country'].replace('Türkiye', 'Turkey')

        # For easier handling, all country names are converted to country codes
        country_codes = pd.read_json('data/reference/country_codes.json')
        country_codes = country_codes['countries']
        # The country names in the dataframe are mapped to the country codes
        df_clean['Country'] = df_clean['Country'].map(country_codes)

        # Store the data in the dictionary with the type of results as the key
        data[resultType] = df_clean

    return data


def transform_PISA_data_to_JSON(data_dict):
    """
    Transform the PISA data to a nested JSON structure according to the defined template.

    Args:
    - data_dict (dict): A dictionary with the type of results as the key and the data as a pandas DataFrame.

    Returns:
    - dict: The PISA results in a nested JSON structure.
    """

    # I take a deep copy of the JSON template structure.
    template_path = 'data/templates/pisa_dataset_template.json'
    with open(template_path, 'r') as f:
        pisa_results = json.load(f)

    # Remove the example data which was included in the template. The metadata is kept.
    pisa_results["countries"] = {}

    # To comply with the defined JSON template, the data must be transformed to the nested structure, combined for each country and year.
    # Direct transformation of the dataframes to JSON is not possible, since the data is split into multiple dataframes.
    for resultType, df in data_dict.items():
        # Iterate over the rows of the dataframes and add the data line by line to the JSON structure
        for i, row in df.iterrows():
            country = row['Country']
            year = str(int(row['Year']))
            # For the result value it must be checked if it is a number. Otherwise there are multiple symbols showing that data is not available.
            # Check if the average is a number, if not, skip the row.
            average = pd.to_numeric(row['Average'], errors='coerce')
            if pd.isna(average):
                continue

            # Check if the country is already in the JSON structure, if not, add it with emtpy directory
            if country not in pisa_results["countries"]:
                pisa_results["countries"][country] = {}

            # Check if the year is already in the JSON structure, if not, add it with emtpy directory
            if year not in pisa_results["countries"][country]:
                pisa_results["countries"][country][year] = {}

            # Add the data to the JSON structure
            pisa_results["countries"][country][year][resultType] = average

    # Additionally, the combined score is calculated and added to the JSON structure
    for country in pisa_results["countries"]:
        for year in pisa_results["countries"][country]:
            # Check if all three types of results are available, otherwise skip the year
            allExist = True
            for resultType in ['math', 'reading', 'science']:
                if resultType not in pisa_results["countries"][country][year]:
                    allExist = False
                    break

            if allExist:
                math = pisa_results["countries"][country][year]["math"]
                reading = pisa_results["countries"][country][year]["reading"]
                science = pisa_results["countries"][country][year]["science"]

                combined = (math + reading + science) / 3
                pisa_results["countries"][country][year]["combined"] = combined

    return pisa_results


def update_PISA_JSON_byExcel(file_path, json_path=None, updateDate=None):
    """
    Update the PISA JSON file with new data from an Excel file.

    Args:
    - file_path (str): The path to the Excel file.
    - json_path (str, optional): The path to the JSON file. If None, the default path is used with new date.
    - updateDate (DateTime, optional): The date of the update.

    Returns:
    - bool: True if the JSON file was updated successfully, False otherwise.
    """

    # Check if the Excel file exists
    if not os.path.exists(file_path):
        print('File not found:', file_path)
        return False

    default_json_path = 'data/pisa_data/pisa_dataset.json'

    if json_path is None:
        json_path = default_json_path

    if updateDate is None:
        updateDate = datetime.datetime.now()
    else:
        # Check if given in the correct format
        if not isinstance(updateDate, datetime.datetime):
            print('Incorrect date format, should be datetime object')
            return False

        # Check if stored file is newer than the given date
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                pisa_results = json.load(f)
                tmp = pisa_results["metadata"]["update"]
                dateFromFile = datetime.datetime.strptime(tmp, '%Y-%m-%d')
                if dateFromFile > updateDate:
                    print(
                        'The given date of the new sourece is older than the last update of the JSON file')
                    return False

    # So everything is ready to update the JSON file with new data from the Excel file

    # Load the data from the Excel file
    data = load_PISA_data_fromExcel(file_path)

    if data is None:
        print('The Excel file could not be loaded correctly')
        return False

    # Transform the data to the JSON structure
    pisa_results = transform_PISA_data_to_JSON(data)

    # Edit the metadata of the JSON file
    pisa_results["metadata"]["update"] = updateDate.strftime('%Y-%m-%d')

    # Save the JSON file, overwrite the old one
    with open(json_path, 'w') as f:
        json.dump(pisa_results, f, indent=2)

    return True


#### EXAMPLE USAGE ####
if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = 'data/pisa_data/original_xls_source_combined_tables'
    file_name = 'IDEExcelExport-Apr222024-0515PM.xls'
    src_date = '2024-04-22'

    file_path = os.path.join(project_dir, data_dir, file_name)
    data = load_PISA_data_fromExcel(file_path)

    # The data is now in a dictionary with the type of results as the first key.
    # The data itself is still in a pandas DataFrame.

    # For testing, I print the first few rows of each tab
    for resultType, df in data.items():
        print('Result type:', resultType)
        print('First and last few rows of the data:')
        print(df.head(4))
        print('...')
        print(df.tail(4))

    # Print JSON structure
    # pisa_results = transform_PISA_data_to_JSON(data)
    # print(json.dumps(pisa_results, indent=2))

    # Update the JSON file
    # src_date = datetime.datetime.strptime(src_date, '%Y-%m-%d')
    # update_PISA_JSON_byExcel(file_path, updateDate=src_date)
