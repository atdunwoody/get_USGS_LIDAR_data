import os
import requests
from collections import defaultdict

def get_download_links(url):
    """Download a file from a URL and return its contents as a list of lines."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text.splitlines()

def extract_coordinates(link):
    """Extract 'x#y#' pattern from a link."""
    parts = link.split('_')
    for part in parts:
        if 'x' in part and 'y' in part:
            return part
    return None

def download_file(url, path):
    """Download a file from a URL to a specified path."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {url} to {path}")

def main(output_folder):
    base_url = "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/1m/Projects/"
    project_list = [
        "CO_CameronPeakWildfire_2021_D21", 
        #"CO_SoPlatte_Lot3_2013",
        "CO_SoPlatteRiver_Lot2a_2013",
    ]
    link_list_txt = "0_file_download_links.txt"
    link_dict = {}
    coordinate_dict = defaultdict(list)

    # Collect all links and group them by coordinates
    for project_name in project_list:
        try:
            link_url = base_url + project_name + "/" + link_list_txt
            links = get_download_links(link_url)
            for link in links:
                coord = extract_coordinates(link)
                if coord:
                    coordinate_dict[coord].append((project_name, link))
        except requests.RequestException as e:
            print(f"An error occurred while downloading the file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Filter coordinates that appear in more than one project
    matching_links = {coord: links for coord, links in coordinate_dict.items() if len(links) > 1}

    # Download and organize files
    for coord, items in matching_links.items():
        print(f"Processing files for coordinate {coord}:")
        for project_name, link in items:
            project_folder = os.path.join(output_folder, project_name)
            os.makedirs(project_folder, exist_ok=True)
            file_name = link.split('/')[-1]
            file_path = os.path.join(project_folder, file_name)
            download_file(link, file_path)

if __name__ == "__main__":
    output_folder = r"Y:\ATD\LIDAR 2021-2013"  # Specify your output directory here
    main(output_folder)
