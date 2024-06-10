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


# Compare pisa countries with country code list
# Load the country code list
path_country_codes = "data/reference/country_codes.json"
with open(path_country_codes, "r") as file:
    country_codes = json.load(file)
    country_codes = country_codes["countries"].values()

missingInPisa = []
missingInCountryList = []
for country in countries_pisa:
    if country not in country_codes:
        missingInCountryList.append(country)
for country in country_codes:
    if country not in countries_pisa:
        missingInPisa.append(country)

print("Missing in PISA dataset:")
print(missingInCountryList)
print("Missing in country code list:")
print(missingInPisa)
