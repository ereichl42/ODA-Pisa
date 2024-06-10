# Take a PISA and finance dataset and extract all the countries, just to get a list of all countries listed in the dataset.
# The following code only runs if the executing directory is the root directory of the project!!

import json
import os
import sys

# Load the JSON files to get a unique list of all countries
path_pisa = "data/pisa_data/pisa_dataset.json"
path_finance_1 = "data/financial_data/educ_expenditure_gdp.json"
path_finance_2 = "data/financial_data/educ_expenditure_level_source.json"

# Load the JSON files
with open(path_pisa, "r") as file:
    pisa_data = json.load(file)

with open(path_finance_1, "r") as file:
    finance_data_1 = json.load(file)

with open(path_finance_2, "r") as file:
    finance_data_2 = json.load(file)

# Get the countries from the PISA dataset
# It is all the keys within "countries" in the JSON file
countries_pisa = []
for country in pisa_data["countries"]:
    countries_pisa.append(country)

# Get the countries from the financial dataset
# It is all the keys within "countries" in the JSON file
countries_finance_1 = []
for country in finance_data_1["countries"]:
    countries_finance_1.append(country)

# Get the countries from the financial dataset
# It is all the keys within "countries" in the JSON file
countries_finance_2 = []
for country in finance_data_2["countries"]:
    countries_finance_2.append(country)

# Write the countries to a file
path_countries = "tests/countries.txt"
with open(path_countries, "w") as file:
    file.write("Countries in PISA dataset:\n")
    for country in countries_pisa:
        file.write(country + "\n")

# Use country code list to figure out which countries are missing in the financial dataset
path_country_codes = "data/reference/country_codes.json"
with open(path_country_codes, "r") as file:
    country_codes = json.load(file)
    country_codes = country_codes["countries"]

# Transform pisa countries to country codes
countries_pisa_codes = []
for country in countries_pisa:
    # The country codes are given as values in the dictionary, where the key is the country name
    countries_pisa_codes.append(country_codes[country])

# The financial data are already in country codes, so no need to transform them

# Find the countries that are in the PISA dataset, but not in the financial dataset
missing_countries_1 = []
for country in countries_pisa_codes:
    if country not in countries_finance_1 or country not in countries_finance_2:
        missing_countries_1.append(country)

missing_countries_2 = []
for country in countries_finance_1:
    if country not in countries_pisa_codes:
        missing_countries_2.append(country)

print("Countries in PISA dataset, but not in financial dataset:")
print(missing_countries_1)
print("Countries in financial dataset, but not in PISA dataset:")
print(missing_countries_2)
