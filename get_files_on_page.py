import requests
from bs4 import BeautifulSoup

def list_tif_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tif_files = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.tif'):
            tif_files.append(href)

    return tif_files

# URL to scrape
url = "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/1m/Projects/CO_SoPlatteRiver_Lot2a_2013/TIFF/"
tif_files = list_tif_files(url)
print(tif_files)
