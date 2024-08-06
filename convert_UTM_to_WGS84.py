import pandas as pd
from pyproj import Transformer, CRS

# Load the CSV file
input_csv = r"Y:\ATD\Drone Data Processing\Metashape_Processing\BlueLake_JoeWright\240723 Joe Wright\240723 joewright_corr_WGS84.csv"  # Replace with the path to your CSV file
output_csv = r"Y:\ATD\Drone Data Processing\Metashape_Processing\BlueLake_JoeWright\240723 Joe Wright\240723 joewright_corr_WGS84_convert.csv"  # Replace with the desired output file path

# Read the CSV file
df = pd.read_csv(input_csv)

# Define the source CRS (NAD83 UTM Zone 13N with GEOID18)
source_crs = CRS.from_proj4("+proj=utm +zone=13 +datum=NAD83 +geoidgrids=us_noaa_g2018u0.tif +units=m +vunits=m +no_defs")

# Define the target CRS (WGS84 with ellipsoidal height)
target_crs = CRS.from_epsg(4326)

# Initialize the transformer with vertical transformation
transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

# Perform the coordinate transformation
def transform_coordinates(row):
    lon, lat, elev = transformer.transform(row['E_corr'], row['N_corr'], row['Z_corr'])
    return pd.Series([lat, lon, elev], index=['Latitude', 'Longitude', 'Elevation'])

# Apply the transformation
df[['Latitude', 'Longitude', 'Elevation']] = df.apply(transform_coordinates, axis=1)

# Save the transformed coordinates to a new CSV file
df.to_csv(output_csv, index=False)

print(f'Transformed coordinates saved to {output_csv}')
