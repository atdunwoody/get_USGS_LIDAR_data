import re
from collections import defaultdict
import requests
import os
from bs4 import BeautifulSoup
from USGS_data_download import download_file

def list_tif_files(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tif_files = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.tif'):
            tif_files.append(href)

    return tif_files

# Function to extract x and y coordinates from filenames
def extract_coordinates(filename):
    match = re.search(r'x(\d+)y(\d+)', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None


def get_overlapping_coordinates(base_url, project_list):
    
    #make url_list by adding project_list to base_url
    url_list = []
    for project in project_list:
        url_list.append(base_url + project + "/TIFF/")
    print(url_list)
    
    #create dictionary to store coordinates and files
    coordinate_dict = defaultdict(list)
    
    #loop through url_list
    for url in url_list:
        # List of tif files
        tif_files = list_tif_files(url)
        #print(tif_files)
        
        # Extract coordinates and add to dictionary
        for tif_file in tif_files:
            coords = extract_coordinates(tif_file)
            if coords:
                coordinate_dict[coords].append(tif_file)

    #add 
    # Find overlapping coordinates
    overlapping_files = {coords: files for coords, files in coordinate_dict.items() if len(files) > 1}


    # Create a new dictionary with project names and the corresponding files
    overlapping_files_project = defaultdict(list)
    for coords, files in overlapping_files.items():
        for file in files:
            for project in project_list:
                if project in file:
                    overlapping_files_project[project].append(file)
                    
    return overlapping_files_project

def main():
    # Base URL for the files
    base_url = "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/1m/Projects/"
    base_download_url = f"https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/"
    output_dir = r"C:\ATD\LIDAR 2021-2013"
    project_list = [
                    "CO_CameronPeakWildfire_2021_D21", 
                    #"CO_DRCOG_2020_B20",
                    "CO_SoPlatteRiver_Lot2a_2013",
                    #"CO_SoPlatteRiver_Lot3_2013"
                    ]

    overlapping_files = get_overlapping_coordinates(base_url, project_list)
    for project, files in overlapping_files.items():
        download_url = base_download_url + project + "/TIFF/"
        #search for project in overlapping_files and create a list of coordinates
        for file in files:
            file_download_url = download_url + file
            print(file_download_url)
            print(f"Downloading: {file}")
            download_file(file_download_url, file)

        


if __name__ == "__main__":
    main()