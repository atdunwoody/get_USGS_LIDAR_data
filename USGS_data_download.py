
import os
os.environ['GDAL_DATA'] = r'C:\Users\AlexThornton-Dunwood\miniconda3\envs\utils\Library\share\gdal'
os.environ['PROJ_LIB']  = r'C:\Users\AlexThornton-Dunwood\miniconda3\envs\utils\Library\share\proj'

import requests
from bs4 import BeautifulSoup
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
from rasterio.io import MemoryFile
import geopandas as gpd
from shapely.geometry import box, mapping


def list_tif_files(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.tif')]

def download_file(url, out_path):
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'wb') as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"Downloaded: {out_path}")
    else:
        print(f"Failed ({resp.status_code}): {url}")

def download_all_tif_files(base_url, output_dir):
    tif_names = list_tif_files(base_url)
    local_paths = []
    for tif in tif_names:
        url = base_url.rstrip('/') + '/' + tif
        out_path = os.path.join(output_dir, tif)
        # Check if file already exists
        if os.path.exists(out_path):
            print(f"File already exists: {out_path}")
            local_paths.append(out_path)
            continue
        download_file(url, out_path)
        local_paths.append(out_path)
    return local_paths


def stitch_tifs(tif_paths, output_path, mask_gpkg_path):
    # 1. Load basin mask geometry
    mask_gdf = gpd.read_file(mask_gpkg_path)
    mask_geom = mask_gdf.unary_union

    clipped_sources = []
    for p in tif_paths:
        with rasterio.open(p) as src:
            tile_bounds = box(*src.bounds)
            # skip tiles with no intersection
            if not tile_bounds.intersects(mask_geom):
                print(f"Skipping (no overlap): {os.path.basename(p)}")
                continue

            # now safe to mask
            out_image, out_transform = mask(src, [mapping(mask_geom)], crop=True)
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width":  out_image.shape[2],
                "transform": out_transform,
            })
            memfile = MemoryFile()
            dataset = memfile.open(**out_meta)
            dataset.write(out_image)
            clipped_sources.append(dataset)

    if not clipped_sources:
        print("No tiles intersect the mask—nothing to stitch.")
        return

    # 4. Merge clipped arrays
    mosaic, out_trans = merge(clipped_sources)

    # 5. Write out
    out_meta = src.meta.copy()
    out_meta.update({
        "driver":    "GTiff",
        "height":    mosaic.shape[1],
        "width":     mosaic.shape[2],
        "transform": out_trans
    })
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with rasterio.open(output_path, 'w', **out_meta) as dst:
        dst.write(mosaic)

    print(f"Stitched (clipped) mosaic saved to: {output_path}")

def main():
    # ─── CONFIGURATION ────────────────────────────────────────────────────────────────
    project_list = [
        # "OR_DOGAMI_2017",  
        # # "OR_HarneyCounty_2018",
        # # "OR_HarneyCounty_TL_2018",
        # # "OR_HarneySilver_2020_A20",
        # # "OR_Malheur_2016",
        # # "OR_McKenzieRiver_2021_B21",
        # "OR_NRCSUSGS_2019_D19",
        # # "OR_OLCMetro_2019_A19",
        # # "OR_PoleCreek_2013",
        # # "OR_RogueSiskiyouNF_2019_B19",
        # # "OR_SouthCoast_2019_A19",
        # # "OR_SouthwestCentralSycan_2021_B21",
        # "OR_UmatillaUnionMorrow_2021_D21",
        # "OR_UmatillaWallowaWhitman_B22",
        # # "OR_UpperJohnDay_2020_A20"
        
        # Downloaded
        "OR_Wallowa_2015"
    ]
    DOWNLOAD_DIR  = r"C:\Users\AlexThornton-Dunwood\OneDrive - Lichen Land & Water\Lichen Drive\Projects\20240007_Atlas Process (GRMW)\07_GIS\Data\LiDAR"
    MASK_GPKG     = r"C:\Users\AlexThornton-Dunwood\OneDrive - Lichen Land & Water\Lichen Drive\Projects\20240007_Atlas Process (GRMW)\07_GIS\Data\LiDAR\Basin Mask.gpkg"

    for project in project_list:
        print(f"\nProcessing project: {project}")
        BASE_URL = (
            "https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/"
            f"Elevation/1m/Projects/{project}/TIFF/"
        )
        out_dir = os.path.join(DOWNLOAD_DIR, project)
        print("  Listing and downloading .tif files…")
        tif_list = download_all_tif_files(BASE_URL, out_dir)

        if tif_list:
            print("  Stitching downloaded tiles (clipped to basin mask)…")
            stitched_fp = os.path.join(out_dir, f"{project}_mosaic.tif")
            stitch_tifs(tif_list, stitched_fp, MASK_GPKG)
        else:
            print("  No .tif files found at the specified URL.")

if __name__ == "__main__":
    main()
