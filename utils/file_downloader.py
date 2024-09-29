import requests
import time
from datetime import datetime
from config import BASE_URL, MONTHS_PT_BR  # Static values from config.py

def build_url(date: datetime) -> str:
    """
    Constructs the URL based on the given date. The expected format in the URL is something like 'd24set19', (19/09/2024).

    Args:
        date (datetime): Date used to build the URL.

    Returns:
        str: Formatted URL.
    """
    day = date.strftime("%d")
    month_abbr = date.strftime("%b").upper()  # Get the abbreviated month in uppercase
    month_abbr_pt = MONTHS_PT_BR.get(month_abbr, '').lower()  # Convert to the Portuguese month in lowercase
    year_abbr = date.strftime("%y")  # Abbreviated year with two digits
    
    if not month_abbr_pt:
        raise ValueError(f"Month '{month_abbr}' not found in the mapping.")

    # URL structure with formatted date, using the BASE_URL from config.py
    return f"{BASE_URL}d{year_abbr}{month_abbr_pt}{day}.xls"


def download_file(url: str, max_retries: int = 3, delay: int = 5) -> bytes:
    """
    Downloads a file from a URL with retry logic.

    Args:
        url (str): The URL of the file to be downloaded.
        max_retries (int): Maximum number of retry attempts before failing. Default is 3.
        delay (int): Wait time (in seconds) between retries. Default is 5 seconds.

    Returns:
        bytes: The content of the file, or None if the download fails after all attempts.
    """
    for attempt in range(max_retries):
        try:
            print(f"Attempting to download file (Attempt {attempt + 1}/{max_retries}): {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check for HTTP errors
            print(f"File successfully downloaded: {url}")
            return response.content  # Return the file content
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as error:
            print(f"Error downloading file from {url}: {error}")
            if attempt < max_retries - 1:  # If it's not the last attempt
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                print(f"Failed to download the file after {max_retries} attempts.")
    
    return None  # Return None if all attempts fail
