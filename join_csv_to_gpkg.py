import pandas as pd
import geopandas as gpd
from pathlib import Path

# Define file paths
excel_path = r"Y:\ATD\GIS\Soil Data\ETF\Tables\Physical Soil Properties.xlsx"
gpkg_path = r"Y:\ATD\GIS\Soil Data\ETF\Soil_Map.gpkg"
output_gpkg_path = r"Y:\ATD\GIS\Soil Data\ETF\Soil_Map_Physical_Properties.gpkg"


def match_and_merge_excel_to_gpkg(excel_path, gpkg_path, output_gpkg_path):
    # Load the Excel data
    excel_df = pd.read_excel(excel_path)

    # Load the GeoPackage data
    gdf = gpd.read_file(gpkg_path)

    # Ensure the "Map Unit Symbol" and "MUSYM" fields are in the same type
    excel_df['Map Unit Symbol'] = excel_df['Map Unit Symbol'].astype(str)
    gdf['MUSYM'] = gdf['MUSYM'].astype(str)

    # Merge the data
    merged_gdf = gdf.merge(excel_df, left_on='MUSYM', right_on='Map Unit Symbol', how='left')

    # Save the merged data back to a new GeoPackage
    merged_gdf.to_file(output_gpkg_path, driver='GPKG')


# Run the function
match_and_merge_excel_to_gpkg(excel_path, gpkg_path, output_gpkg_path)
