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
    Each DataFrame contains the data for one type of results (mathematics, reading, science).
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
    keywords = ['mathematics', 'reading', 'science']
    # The header of the data is known too and can be used to search for the actual data
    header = ['Year/Study', 'Jurisdiction', 'Average', 'Standard Error']

    data = {}
    for tab in tabs:
        df = pd.read_excel(file_path, sheet_name=tab)

        # In the first few lines of each tab there is always a description if the data is about mathematics, reading, or science
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

        # Store the data in the dictionary with the type of results as the key
        data[resultType] = df_clean

    return data


def load_pisa_data(data_dict):
    """
    Load the PISA data from a dictionary of pandas DataFrames.

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
    pisa_results["countries"] = []

    # I can't just transform the dataframe to JSON since each result type is in a separate dataframe.
    # I need to merge the dataframes first.
    # Additionally, I calculate a additional metric for a average value of mathemathics, reading, and science.
    for resultType, df in data_dict.items():
        pass


        #### EXAMPLE USAGE ####
if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = 'data/pisa_data/original_xls_source_combined_tables'
    file_name = 'IDEExcelExport-Apr222024-0515PM.xls'

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
