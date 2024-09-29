import matplotlib.pyplot as plt
import os
from utils.csv_utilities import load_csv, validate_date_column
from config import CLEANED_DATA_FILE

def plot_indicative_rate_by_indexer(destination_folder: str) -> None:
    """
    Plots the average indicative rate (Taxa Indicativa Média) by date for each indexer.

    Args:
        destination_folder (str): Path to the folder where the CSV file is stored.
    """
    # Construct the file path
    file_path = os.path.join(destination_folder, CLEANED_DATA_FILE)

    # Load the CSV file with error handling
    df = load_csv(file_path)
    if df is None:
        return  # Exit if the file couldn't be loaded

    # Validate the 'data' (date) column
    df = validate_date_column(df, 'data')

    # Group by 'data' and 'Indexer' and calculate the average 'Taxa Indicativa'
    try:
        df_grouped = df.groupby(['data', 'Indexer'])['Taxa Indicativa'].mean().reset_index()
    except KeyError as e:
        print(f"Error: Missing expected column {e} in the dataset.")
        return

    # List of unique indexers
    indexers = df_grouped['Indexer'].unique()

    for indexer in indexers:
        # Filter the dataframe for the current indexer
        df_indexer = df_grouped[df_grouped['Indexer'] == indexer]

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(df_indexer['data'], df_indexer['Taxa Indicativa'], marker='o')

        # Format the x-axis for better readability
        plt.xticks(rotation=45)
        plt.xlabel("Date (DD-MM-YYYY)")
        plt.ylabel("Average Indicative Rate (%)")

        # Set the title
        plt.title(f"Average Indicative Rate by Date - {indexer}")

        # Add gridlines for better visual clarity
        plt.grid(True)

        # Ensure the output file path exists
        output_file = os.path.join(destination_folder, f"indicative_rate_{indexer}.png")
        try:
            plt.savefig(output_file)
            print(f"Plot saved as: {output_file}")
        except Exception as e:
            print(f"Error saving plot for {indexer}: {e}")
        finally:
            plt.close()  # Close the plot to free memory

        # Optionally display the plot
        plt.show()
