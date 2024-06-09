# ODA-Pisa
The goal is to examine the relationship between educational investments and student performance across various countries and years.

API Call
THis section explains how the download for data from the OECD PISA study and educational funding datasets is implemented. 

PISA Dataset
The OECD provides access to PISA data through a RESTful API. Below is an example of how to generate a link and make an API call using Python:
The problem regarding the datasets of interest, like students reading competences, with identifier PVREAD, or PVMEATH for mathematical competences:

So there was no end node found, which is an internal error of the OECD site because the implementation works for other datasets like QNA.

Example API Call
python

import requests

# Define the base URL and parameters
base_url = "http://stats.oecd.org/sdmx-json/data/"
dataset = "QNA" #PVREAD is the dataset of interest
filter_exp = "USA+CAN+MEX.PVREAD.TOTAL"
start_period = "2000"
end_period = "2022"

# Generate the API link
link = f"{base_url}{dataset}/{filter_exp}/all?startTime={start_period}&endTime={end_period}"

# Make the API call
response = requests.get(link)
data = response.json()

# Print the response data
print(data)

Eurostat Educational Funding Dataset
The Eurostat API provides access to educational funding data. Below is an example of how to fetch the data:
The call works fine for single and multiple countries, but most easy readible JSON is provided for single countries
The used dataset contains following information: "Financial aid to students by education level - as % of total public expenditure"

Example API Call for OECD Dataset 
python

import requests

# Define the URL for Eurostat dataset
url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/educ_uoe_finf01?format=TSV&compressed=true"

# Make the API call
response = requests.get(url)
data = response.text

# Print the response data
print(data)
Frontend


Backend


Getting Started
Clone the repository.
Install the required Python libraries.
Run the provided scripts to fetch and analyze the data.
Requirements
Python 3.x
pandas
numpy
requests
tkinter
