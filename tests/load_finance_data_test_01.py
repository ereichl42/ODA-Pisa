import os
import pandas as pd
import io


# Read file and standarize delimiters in memory

file_path = "data/expenditure_data/educ_expenditure_gdp.tsv"

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

# Melt the DataFrame to make it easier to filter.
# This will convert the DataFrame from wide format to long format, that means each row will represent a single observation.
data_melted = pd.melt(data, id_vars=[
                      "freq", "unit", "isced11", "geo\\TIME_PERIOD"], var_name="Year", value_name="Expenditure")

# Rename the columns for easier access
data_melted.columns = ["Frequency", "Unit",
                       "Education_Level", "Country", "Year", "Expenditure"]


# Function to get expenditure data for a specific country, education levels, and year range
def get_expenditure(country, education_levels, start_year, end_year):
    # Filter the data based on the given parameters
    filtered_data = data_melted[
        (data_melted["Country"] == country) &
        (data_melted["Education_Level"].isin(education_levels)) &
        (data_melted["Year"].astype(int).between(start_year, end_year))
    ]
    return filtered_data


# Example usage of the function
country = "AT"
education_levels = ["ED0", "ED01"]
start_year = 2012
end_year = 2015

expenditure_data = get_expenditure(
    country, education_levels, start_year, end_year)
print(expenditure_data)
