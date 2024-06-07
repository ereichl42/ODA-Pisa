import os
import pandas as pd
import io


def load_expenditure_data(file_path):
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

    # Return processed data as a DataFrame
    return data_melted


def filter_expenditure_data(data, country=None, education_levels=None, start_year=None, end_year=None):
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


#### EXAMPLE USAGE ####
file_path = "data/expenditure_data/educ_expenditure_gdp.tsv"
expenditure_data = load_expenditure_data(file_path)

if expenditure_data is not None:
    country = "AT"
    education_levels = ["ED0", "ED01"]
    start_year = 2012
    end_year = 2015

    filtered_expenditure_data = filter_expenditure_data(
        expenditure_data, country, education_levels, start_year, end_year)
    print(filtered_expenditure_data)


filter_expenditure_data(expenditure_data, country="AT", start_year=2013)
