import pandas as pd
import os
from config import RAW_DATA_FILE

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file into a pandas DataFrame with error handling.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    except pd.errors.ParserError:
        print(f"Error: Failed to parse the file {file_path}.")
    
    return None

def validate_date_column(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Validates and converts the date column. If the date is in 'YYYYMMDD', it converts to 'DD/MM/YYYY'.
    If the date is already in 'DD/MM/YYYY' format, no change is made. Invalid dates are removed.

    Args:
        df (pd.DataFrame): The DataFrame to validate.
        date_column (str): The name of the column to validate.

    Returns:
        pd.DataFrame: DataFrame with the date column formatted as 'DD/MM/YYYY', and invalid date rows removed.
    """
    try:
        # First, attempt to convert from 'YYYYMMDD' to datetime
        try:
            df[date_column] = pd.to_datetime(df[date_column], format='%Y%m%d', errors='raise')
        except (ValueError, TypeError):
            # If it fails, try to parse the date as 'DD/MM/YYYY'
            df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y', errors='coerce')

        # Drop rows with invalid dates (NaT)
        if df[date_column].isnull().any():
            print("Warning: Some dates could not be converted and will be removed.")
            df = df.dropna(subset=[date_column])

        # Convert to 'DD/MM/YYYY' format
        df[date_column] = df[date_column].dt.strftime('%d/%m/%Y')

        return df
    except KeyError:
        print(f"Error: Column '{date_column}' not found in the DataFrame.")
        return df
    except Exception as e:
        print(f"Error validating date column: {e}")
        return df

def combine_and_save_csvs(source_folder: str, business_days: list, output_folder: str) -> pd.DataFrame:
    """
    Combines CSV files corresponding to the business days from the source folder and saves the result as a CSV.
    
    Args:
        source_folder (str): Path to the folder containing the source CSV files.
        business_days (list): List of business days to look for CSVs.
        output_folder (str): Path to the folder where the combined CSV will be saved.

    Returns:
        pd.DataFrame: Combined DataFrame from all the CSV files.
    """
    combined_data = []

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for date_str in business_days:
        # Look for all CSV files corresponding to the business days
        for file_name in os.listdir(source_folder):
            if date_str in file_name and file_name.endswith('.csv'):
                file_path = os.path.join(source_folder, file_name)
                
                try:
                    # Read the CSV file into a DataFrame and append it to the list
                    df = pd.read_csv(file_path)
                    df['sheet_name'] = file_name.split('-')[1].split('.')[0]  # Add sheet name from file name
                    df['data'] = date_str  # Add the date based on the file name
                    combined_data.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Combine all DataFrames into one
    if combined_data:
        combined_df = pd.concat(combined_data, ignore_index=True)

        # Save the combined DataFrame to the output folder
        combined_file_path = os.path.join(output_folder, RAW_DATA_FILE)
        combined_df.to_csv(combined_file_path, index=False)
        print(f"Combined CSV saved to: {combined_file_path}")
        return combined_df
    else:
        print("No CSV files were combined.")
        return pd.DataFrame()  # Return an empty DataFrame if no files were combined