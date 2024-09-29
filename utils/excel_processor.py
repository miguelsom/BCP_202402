import pandas as pd
from io import BytesIO
from config import *

def process_sheets(file_data: bytes, date_str: str) -> dict:
    """
    Processes each sheet of the Excel file and returns a dictionary with the sheet name as the key and the processed DataFrame as the value.

    Args:
        file_data (bytes): Excel file in bytes format.
        date_str (str): Date in the format 'yyyymmdd', used as a reference for processing.

    Returns:
        dict: A dictionary where the key is the sheet name and the value is the processed DataFrame.
    """
    try:
        # Wrap file_data in BytesIO to read it correctly
        file_like_object = BytesIO(file_data)
        
        # Read all sheets from the Excel file
        sheets = pd.read_excel(file_like_object, sheet_name=None)  
        processed_sheets = {}

        for sheet_name, df in sheets.items():
            # Skip the first 8 rows and adjust the headers
            df = df.iloc[8:].reset_index(drop=True)
            
            # Set the new column names
            df.columns = COLUMNS
            
            # Remove rows where 'Nome' is NaN and rows where all columns are NaN
            df = df.dropna(subset=['Nome']).dropna(how='all').reset_index(drop=True)

            # Add the processed sheet to the dictionary
            processed_sheets[sheet_name] = df

        return processed_sheets

    except Exception as error:
        print(f"Error processing the spreadsheet: {error}")
        return {}
