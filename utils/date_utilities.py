from datetime import datetime, timedelta

def get_business_days(count: int) -> list:
    """
    Returns a list of dates for the last 'count' business days.
    
    Args:
        count (int): Number of business days to return.
    
    Returns:
        list: A list of strings containing the dates in the format 'yyyymmdd'.
    """
    business_days = []
    current_date = datetime.now() - timedelta(days=1)  # Subtract 1 day to use "yesterday" as the reference
    
    # Loop to get the last 'count' business days
    while len(business_days) < count:
        if current_date.weekday() < 5:  # If it's not Saturday (5) or Sunday (6), it's a business day
            business_days.append(current_date)
        current_date -= timedelta(days=1)

    # Return dates in 'yyyymmdd' format
    return [day.strftime("%Y%m%d") for day in business_days]

