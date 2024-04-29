#import requests library
import requests
#url of the data, hardcoded, need a dictionary of urls and their corresponding topics
url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/educ_uoe_fine01/1.0/*.*.*.*.*?c[freq]=A&c[unit]=MIO_EUR&c[sector]=S1,S1D,S1D_OTH,S13,INTLORG&c[isced11]=ED0&c[geo]=AT&compress=true&format=csvdata&formatVersion=2.0&c[time]=2020,2019,2018,2017,2016,2015,2014,2013,2012"

def fetchEUeducationExpansesData(url):
    #GET request 
    try:
        response = requests.get(url)

        #error handling; if the request is successful, the status code will be 200
        if response.status_code == 200:
            print('data retrieved successfully')
        else:
            print('error in retrieving data Code:', response.status_code)
    except Exception as e:
        print('An error occurred:', str(e))
