# Take a PISA and finance dataset and extract all the countries, just to get a list of all countries listed in the dataset.
# The following code only runs if the executing directory is the root directory of the project!!

import os
import sys
from utils.load_finance_data import load_financial_data
from utils.load_PISA_data_fromExcel import load_PISA_data_fromExcel

path_pisa = "data/pisa_data/original_xls_source_combined_tables/IDEExcelExport-Apr222024-0515PM.xls"
path_finance = "data/financial_data/original_tsv_source/educ_expenditure_gdp.tsv"

pisa_data = load_PISA_data_fromExcel(path_pisa)
finance_data = load_financial_data(path_finance)

pisa_df = pisa_data['mathematics']
finance_df = finance_data

pisa_countries = pisa_df['Jurisdiction'].unique()
finance_countries = finance_df['Country'].unique()

print(pisa_countries)
print(finance_countries)


# All keys of the pisa_df data frame
print(pisa_df.keys())


print(sys.path)
# Working dir
print(os.getcwd())
# set working dir of python interpreter to parent folder
os.chdir("..")
