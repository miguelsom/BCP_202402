import os
import pandas as pd

def ensure_folder_exists(folder_path: str) -> None:
    """
    Ensures that the given folder path exists. If not, it creates the folder.
    
    Args:
        folder_path (str): The path to the folder to check or create.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

def save_dataframe_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Saves a DataFrame to a CSV file.
    
    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The path to the file to save the DataFrame in.
    """
    try:
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"File saved: {file_path}")
    except Exception as e:
        print(f"Failed to save file {file_path}: {e}")
