import pandas as pd
import numpy as np

def clean_excel_RUSLE(file_path, output_path):
    df = pd.read_excel(file_path)

    #drop rows with all NaN values
    df = df.dropna(how='all')
    # Fill down values for 'Map Unit Symbol', 'Component Name - Local Phase', 'T Factor', 'Wind Erodibility Group', 'Wind Erodibility Index'
    columns_to_fill = ['Map Unit Symbol']
    df[columns_to_fill] = df[columns_to_fill].fillna(method='ffill')

    # Drop rows where all values are NaN
    df = df.dropna(how='all')

    #remove : from 'Map Unit Symbol'
    df['Map Unit Symbol'] = df['Map Unit Symbol'].str.replace(':', '')
    
    # # Remove rows that have NaN values in the essential columns
    # essential_columns = ['Horizon Depth Range', 'Total Sand Range', 'Total Silt Range', 'Total Clay Range', 'Moist Bulk Density Range', 'Ksat Range', 'AWC Range', 'Linear Extensibility Range', 'Organic Matter Range', 'Kw Factor', 'Kf Factor']
    # df = df.dropna(subset=essential_columns, how='all')

    # Remove repeating headers
    # Assuming the repeating headers are identical to the first row
    # repeating_header = df.iloc[0]
    # df = df[~(df == repeating_header).all(axis=1)]
    def replace_dash_with_null(df):
        df.replace('---', np.nan, inplace=True)

    # Apply the function to replace "---" with NaN
    replace_dash_with_null(df)
    # Reset index after cleaning
    df = df.reset_index(drop=True)

    # Save the cleaned DataFrame to a new Excel file
    df.to_excel(output_path, index=False)

    print(f"Cleaned data has been saved to {output_path}")
 
def clean_excel(file_path, output_path):

    # Load the Excel file
    df = pd.read_excel(file_path)

    # Fill down values for 'Map Unit Symbol', 'Component Name - Local Phase', 'T Factor', 'Wind Erodibility Group', 'Wind Erodibility Index'
    columns_to_fill = ['Map Unit Symbol', 'Component Name - Local Phase', 'T Factor', 'Wind Erodibility Group', 'Wind Erodibility Index']
    df[columns_to_fill] = df[columns_to_fill].fillna(method='ffill')

    # Drop rows where all values are NaN
    df = df.dropna(how='all')

    # Remove rows that have NaN values in the essential columns
    essential_columns = ['Horizon Depth Range', 'Total Sand Range', 'Total Silt Range', 'Total Clay Range', 'Moist Bulk Density Range', 'Ksat Range', 'AWC Range', 'Linear Extensibility Range', 'Organic Matter Range', 'Kw Factor', 'Kf Factor']
    df = df.dropna(subset=essential_columns, how='all')

    # Remove repeating headers
    # Assuming the repeating headers are identical to the first row
    repeating_header = df.iloc[0]
    df = df[~(df == repeating_header).all(axis=1)]

    # Reset index after cleaning
    df = df.reset_index(drop=True)

    df.to_excel(output_path, index=False)

    print(f"Cleaned data has been saved to {output_path}")   

def split_columns(input_file, output_file):
    df = pd.read_excel(input_file)

    # Define the columns to split
    columns_to_split = [
        'Horizon Depth Range', 'Total Sand Range', 'Total Silt Range',
        'Total Clay Range', 'Moist Bulk Density Range', 'Ksat Range',
        'AWC Range', 'Linear Extensibility Range', 'Organic Matter Range'
    ]

    # Function to split a column and create two new columns
    def split_column(df, column):
        # Split the column into two new columns
        new_columns = df[column].str.split('-', expand=True)
        df[column + ' Min'] = new_columns[0]
        df[column + ' Max'] = new_columns[1]
        # Drop the original column
        df.drop(columns=[column], inplace=True)

    # Apply the function to each column that needs to be split
    for column in columns_to_split:
        split_column(df, column)


    def replace_dash_with_null(df):
        df.replace('---', np.nan, inplace=True)

    # Apply the function to replace "---" with NaN
    replace_dash_with_null(df)

    # Save the modified dataframe back to an Excel file
    df.to_excel(output_file, index=False)

def join_list_of_df_on_column(list_of_df, column):
    # Join a list of DataFrames on a common column
    # list_of_df: List of DataFrames to join
    # column: Column name to join on
    # Returns: DataFrame containing the joined data
    if len(list_of_df) == 0:
        raise ValueError("List of DataFrames is empty")

    # Initialize the DataFrame with the first DataFrame in the list
    joined_df = list_of_df[0]

    # Iterate over the remaining DataFrames and merge them
    for df in list_of_df[1:]:
        joined_df = joined_df.merge(df, on=column)

    return joined_df

def open_excel_in_folder_to_df(folder_path):
    # Open all Excel files in a folder and read them into a list of DataFrames
    # folder_path: Path to the folder containing Excel files
    # Returns: List of DataFrames
    import os

    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter out only Excel files
    excel_files = [f for f in files if f.endswith('.xlsx')]

    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate over each Excel file and read it into a DataFrame
    for file in excel_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)
        dfs.append(df)

    return dfs

def main():
    # Load the Excel file
    input_path = r"Y:\ATD\GIS\Soil Data\ETF\Tables\Physical Soil Properties Clean.xlsx"
    output_path = r"Y:\ATD\GIS\Soil Data\ETF\Tables\Physical Soil Properties Clean v1.xlsx"

    split_columns(input_path, output_path)
if __name__ == "__main__":
    main()