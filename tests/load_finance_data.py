import pandas as pd


# Data source files are in the data/ directory in the root of the project
filepath = 'data/estat_educ_uoe_fina01.tsv'


# Read TSV file
data = pd.read_csv(filepath, sep='\t', encoding='utf-8')
