import os
import pandas as pd
from utils.data_validation import DatasetValidator
from utils.csv_utilities import load_csv
from utils.file_utilities import save_dataframe_to_csv
from processing.dataset_cleaning import clean_dataset
from utils.excel_processor import process_sheets
from utils.file_downloader import build_url, download_file
from config import RAW_DATA_FILE, CLEANED_DATA_FILE

def download_and_save_files(destination_folder: str, business_days: list) -> None:
    """
    Downloads and saves files for the given business days. Processes each sheet and saves it as
    'sheet_name-yyyymmdd.csv'.

    Args:
        destination_folder (str): Path to the folder where the files will be saved.
        business_days (list): List of business days to process.
    """
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created directory: {destination_folder}")

    for date_str in business_days:
        try:
            # Convert date string to datetime
            date = pd.to_datetime(date_str, format="%Y%m%d")
            
            # Generate URL and download the file
            url = build_url(date)
            file_data = download_file(url)

            if file_data:
                # Process the data from the sheet
                sheets_dict = process_sheets(file_data, date_str)

                # Save each processed sheet individually as a CSV
                for sheet_name, df in sheets_dict.items():
                    if not df.empty:
                        file_path = os.path.join(destination_folder, f"{date_str}-{sheet_name}.csv")
                        save_dataframe_to_csv(df, file_path)
                        print(f"File saved: {file_path}")
            else:
                print(f"Failed to download the file for {date_str}.")
        
        except Exception as e:
            print(f"Error processing file for date {date_str}: {e}")

def prepare_and_clean_dataset(destination_folder: str) -> None:
    """
    Prepares and cleans the dataset by applying multiple processing steps and saving the final cleaned dataset.

    Args:
        destination_folder (str): Path to the folder where the files are stored.
    """
    # Load the combined dataset
    input_file_path = os.path.join(destination_folder, RAW_DATA_FILE)
    
    try:
        df = load_csv(input_file_path)
        if df is None:
            print(f"Failed to load the dataset from {input_file_path}.")
            return

        # Clean the dataset
        df_cleaned = clean_dataset(df)

        # Save the cleaned dataset
        output_file_path = os.path.join(destination_folder, CLEANED_DATA_FILE)
        save_dataframe_to_csv(df_cleaned, output_file_path)
        print(f"Cleaned dataset saved to: {output_file_path}")

        # Validate the cleaned dataset
        DatasetValidator.validate_dataset(df_cleaned)
        print("Dataset validation passed.")
    
    except Exception as e:
        print(f"Error in preparing or cleaning the dataset: {e}")



