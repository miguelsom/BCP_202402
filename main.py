from processing.dataset_preparation import download_and_save_files, prepare_and_clean_dataset
from utils.csv_utilities import combine_and_save_csvs
from utils.date_utilities import get_business_days
from utils.plot_indicative_rate import plot_indicative_rate_by_indexer
from config import SOURCE_FOLDER, DATASET_FOLDER, PLOT_FOLDER, BUSINESS_DAYS_COUNT

def main():
    """
    Main function that orchestrates the process of data extraction, 
    CSV combination, dataset preparation, and plotting.
    """
    print("Step 1: Getting the list of recent business days.")
    # Get the list of recent business days
    business_days = get_business_days(BUSINESS_DAYS_COUNT)
    print(f"Business days: {business_days}")

    print("Step 2: Data extraction - Downloading and saving files for the business days.")
    # 1. Data extraction - Downloads and saves the files for the business days
    download_and_save_files(SOURCE_FOLDER, business_days)
    print("Files downloaded and saved successfully.")

    print("Step 3: CSV combination - Combining the CSV files for the business days.")
    # 2. CSV combination - Combines the CSV files for the business days
    # Adds the 'sheet_name' and 'date' columns to the combined DataFrame
    combined_dataframe = combine_and_save_csvs(SOURCE_FOLDER, business_days, DATASET_FOLDER)
    print("CSV files combined successfully.")

    print("Step 4: Dataset preparation - Cleaning and preparing the dataset for further analysis.")
    # 3. Dataset preparation - Cleans and prepares the dataset for further analysis
    prepare_and_clean_dataset(DATASET_FOLDER)
    print("Dataset prepared and cleaned successfully.")

    print("Step 5: Plotting - Generating plots based on the indicative rate by indexer.")
    # 4. Plotting - Generates plots based on the indicative rate by indexer
    plot_indicative_rate_by_indexer(DATASET_FOLDER)
    print("Plots generated successfully.")

if __name__ == "__main__":
    main()
