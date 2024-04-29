import dataRequest as dr
import pandas as pd
#url of the data, hardcoded, need a dictionary of urls and their corresponding topics
url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/educ_uoe_fine01/1.0/*.*.*.*.*?c[freq]=A&c[unit]=MIO_EUR&c[sector]=S1,S1D,S1D_OTH,S13,INTLORG&c[isced11]=ED0&c[geo]=AT&compress=true&format=csvdata&formatVersion=2.0&c[time]=2020,2019,2018,2017,2016,2015,2014,2013,2012"

def main():
    """
    Main function to execute the script.
    """
    # 1. Fetch the data
    eduData =dr.fetchEUeducationExpansesData(url)
    # 2. Load the data
    eduDataTweeked = pd.read_csv(eduData)
    # 3. Clean the data
    eduDataTweeked = eduDataTweeked.dropna()

    # 4. Analyze the data
    eduDataTweeked
    # 5. Visualize the data
    # 6. Save the data

# 6. Standard boilerplate to run the main function
if __name__ == "__main__":
    main()