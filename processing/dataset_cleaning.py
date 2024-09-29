import pandas as pd
import numpy as np
from utils.csv_utilities import validate_date_column
from config import DATASET_COLUMNS_TO_SELECT, DATASET_FINAL_COLUMNS

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by performing the following tasks:
    1. Selecting only relevant columns.
    2. Creating an 'Indexer' column based on the 'sheet_name'.
    3. Filtering out rows with invalid 'Indexer' values.
    4. Converting date formats using the existing validate_date_column function.
    5. Ensuring 'PU' and 'Taxa Indicativa' are numeric and removing invalid rows.
    6. Formatting numeric columns to 2 decimal places.

    Args:
        df (pd.DataFrame): The raw dataset that needs cleaning. 
                           It should include at least the following columns: 
                           ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'sheet_name', 'data']

    Returns:
        pd.DataFrame: The cleaned dataset with the following columns: 
                      ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'data', 'Indexer']
                      Rows with invalid or missing values are removed, and numeric fields are rounded to 2 decimals.
    """
    
    # Step 1: Select only the columns of interest
    df_cleaned = df.loc[:, DATASET_COLUMNS_TO_SELECT]

    # Step 2: Create a new 'Indexer' column based on the 'sheet_name'
    df_cleaned['Indexer'] = df_cleaned['sheet_name'].apply(lambda x: (
        'IPCA +' if 'IPCA_SPREAD' in str(x) else
        '% do DI' if 'DI_PERCENTUAL' in str(x) else
        'DI +' if 'DI_SPREAD' in str(x) else 'Other'))

    # Step 3: Filter out rows where 'Indexer' equals 'Other'
    df_filtered = df_cleaned[df_cleaned['Indexer'] != 'Other'].copy()

    # Step 4: Validate and clean the 'data' column using the existing csv_utilities function
    df_filtered = validate_date_column(df_filtered, 'data')
    if df_filtered is None:
        raise ValueError("Data validation failed, unable to proceed with an invalid 'data' column.")

    # Step 5: Ensure 'PU' and 'Taxa Indicativa' are numeric, drop invalid rows
    df_filtered['PU'] = pd.to_numeric(df_filtered['PU'], errors='coerce')
    df_filtered['Taxa Indicativa'] = pd.to_numeric(df_filtered['Taxa Indicativa'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['PU', 'Taxa Indicativa', 'data'])

    # Step 6: Format numeric columns to 2 decimal places
    df_filtered['PU'] = df_filtered['PU'].round(2)
    df_filtered['Taxa Indicativa'] = df_filtered['Taxa Indicativa'].round(2)

    # Step 7: Select final columns for output
    df_filtered = df_filtered.loc[:, DATASET_FINAL_COLUMNS]
    
    return df_filtered
