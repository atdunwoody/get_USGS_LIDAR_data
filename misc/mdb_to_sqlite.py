import pandas as pd
import pyodbc
import sqlite3

def mdb_to_sqlite(mdb_path, sqlite_path):
    # Connect to the MDB file
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + mdb_path
    mdb_conn = pyodbc.connect(conn_str)
    
    # Fetch all table names
    table_names_query = "SELECT MSysObjects.Name FROM MSysObjects WHERE MSysObjects.Type=1 AND MSysObjects.Flags=0;"
    table_names = pd.read_sql(table_names_query, mdb_conn)['Name'].tolist()
    
    # Connect to the SQLite database
    sqlite_conn = sqlite3.connect(sqlite_path)
    
    # Iterate through each table and transfer the data
    for table_name in table_names:
        # Read the table from MDB
        query = f"SELECT * FROM [{table_name}]"
        df = pd.read_sql(query, mdb_conn)
        
        # Write the table to SQLite
        df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)
    
    # Close the connections
    mdb_conn.close()
    sqlite_conn.close()
    print(f"Conversion from {mdb_path} to {sqlite_path} completed successfully.")

# Example usage
mdb_path = r"Y:\ATD\GIS\Soil Data\soildb_US_2003.mdb"
sqlite_path = r"Y:\ATD\GIS\Soil Data\soildb_US_2003.sqlite"
mdb_to_sqlite(mdb_path, sqlite_path)
