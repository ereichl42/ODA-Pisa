import os
import pandas as pd


# Path to original files, temporarely stored files directly downloaded from OECD webpage as a combined xls file
path_to_folder = 'data\\pisa_data\\original_xls_source_combined_tables'

# File name
file_name = 'IDEExcelExport-Apr222024-0515PM.xls'

# Combine path and file name
file_path = path_to_folder + '\\' + file_name

# Test if path exists
if not os.path.exists(file_path):
    print('File not found:', file_path)
    exit()

# Read the Excel file, figure out how many tabs
xls = pd.ExcelFile(file_path)
tabs = xls.sheet_names

# In the first few lines of each tab there is always a description if the data is about mathematics, reading, or science
# Thus I can search for it and add it as info to the dictionary
# I will use the first tab as a test tab

keywords = ['mathematics', 'reading', 'science']
tab_info = {}
for tab in tabs:
    df = pd.read_excel(file_path, sheet_name=tab)

    resultType = None

    for keyword in keywords:
        for _, row in df[:10].iterrows():
            if row.str.contains(keyword, case=False).any():
                resultType = keyword
                break
        if resultType:
            break

    tab_info[tab] = resultType

# print(tab_info)


# In this part the actual data is read from each tab.
# Again, it is not clear where the data is, the actual table within the excel's tab.
# But it is known how the header looks like, so we search for it and then read the data from there.

# The header is: 'Year/Study', 'Jurisdiction', Average', 'Standard Error'
# Each is in a separate cell.

header = ['Year/Study', 'Jurisdiction', 'Average', 'Standard Error']

# This header can be found in the first 15 rows of the tab
# The data is below it

data = {}

for tab in tabs:
    df = pd.read_excel(file_path, sheet_name=tab)

    # Find the header
    header_row = None
    for i, row in df[:15].iterrows():
        if row.str.contains(header[0], case=False).any() and \
                row.str.contains(header[1], case=False).any() and \
                row.str.contains(header[2], case=False).any() and \
                row.str.contains(header[3], case=False).any():
            header_row = i
            break

    if header_row is None:
        print('Header not found in tab:', tab)
        continue

    # Read the data till a line is empty
    for i, row in df[header_row + 1:].iterrows():
        if row.str.contains('nan', case=False).all():
            data[tab] = df[header_row + 1:i]
            break


# Combine all the above

# The combined excel files with multiple tabs contain the data but with additonal info.
# The data does not start with first cell in each tab. Thus, searching for certain info and the actual data is needed.

# There a types of results which are here defined as keywords.
keywords = ['mathematics', 'reading', 'science']
# The header of the data is known too and can be used to search for the actual data
header = ['Year/Study', 'Jurisdiction', 'Average', 'Standard Error']

data = {}
for tab in tabs:
    df = pd.read_excel(file_path, sheet_name=tab)

    # In the first few lines of each tab there is always a description if the data is about mathematics, reading, or science
    # Search for the type of results
    resultType = None
    info_row = None
    for keyword in keywords:
        for i, row in df[:10].iterrows():
            if row.str.contains(keyword, case=False).any():
                resultType = keyword
                break
        if resultType:
            info_row = i
            break

    # Some safety check, just in case the online source of the file changed its format
    if resultType is None:
        print('ERROR: No info found in tab! Maybe the downloaded files is faulty!')
        exit()

    # The resultType is the key in the data dictionary
    data[resultType] = {}

    # Find the header
    # It should be a few lines below the info
    header_row = None
    for i, row in df[info_row:info_row + 15].iterrows():
        # Assuming that the online source might change the header a bit,
        # I just check that at least two words from the header are in the row
        keywordsFound = 0
        for keyword in header:
            if row.str.contains(keyword, case=False).any():
                keywordsFound += 1
        if keywordsFound >= 2:
            header_row = info_row + i
            break

    # Some safety check, just in case the online source of the file changed its format
    if header_row is None:
        print('ERROR: Header not found in tab! Maybe the downloaded files is faulty!')
        exit()

    # Read the data till a line is empty
    for i, row in df[header_row:].iterrows():
        print(row)
        """ 
        if row.str.contains('nan', case=False).all():
            print('Data found in tab:', tab, 'of type:', resultType,
                  'from row:', header_row + 1, 'to row:', i - 1)
            data[resultType] = df[header_row + 1:header_row+i]
            break """

    # For testing
    exit()

# The data is now in a dictionary with the type of results as the first key.
# The data itself is still in a pandas DataFrame.

# For testing, I print the first few rows of each tab
for resultType, df in data.items():
    print('Result type:', resultType)
    print('First few rows of the data:')
    print(df.head(5))
