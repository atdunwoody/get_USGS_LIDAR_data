import requests


# Function to download a file
def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename} (Status code: {response.status_code})")

def download_file_from_coords(base_url, project_name, coordinates):
    # Download each file based on the coordinates
    for x, y in coordinates:
        filename = f"USGS_1M_13_x{x}y{y}_{project_name}.tif"
        url = base_url + filename
        print(f"Downloading: {url}")
        download_file(url, filename)

def main():
    # Base URL for the files
    project_name = "CO_CameronPeakWildfire_2021_D21"
    #project_name = "CO_DRCOG_2020_B20"
    base_url = f"https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1m/Projects/{project_name}/TIFF/"


    # List of coordinates
    coordinates = [
        (44, 447), 
        # (44, 448), (44, 449), (44, 450), (44, 451),
        # (45, 446), (45, 447), (45, 448), (45, 449), (45, 450), (45, 451), (45, 452),
        # (46, 445), (46, 446),
        # (47, 445), (47, 446),
        # (48, 446),
        # (49, 446)
    ]
if __name__ == "__main__":
    main()