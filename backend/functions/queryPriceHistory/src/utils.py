from datetime import date, timedelta, datetime

def get_date_list(num_offset, step_days, window_size):
    """
    Generates a list of datetime objects for a window based on offset and step.

    Args:
        offset_days (int): Number of days offset from today (0 for today).
        step_days (int): Step size between dates (e.g., 6 for every Monday).
        window_size (int): Number of dates to include in the window.

    Returns:
        list: List of datetime objects for the specified window.
    """
  
    adjusted_offset = num_offset * step_days

    # Get today's date
    today = date.today()

    # Calculate start date based on offset
    start_date = today - timedelta(days=adjusted_offset)

    # List to store datetime objects
    date_list = []

    # Iterate for the window size
    for _ in range(window_size):

        # Skip weekends by shifting to the closest weekday
        while start_date.weekday() == 5:  # 5 and 6 represent Saturday and Sunday
            start_date -= timedelta(days=1)
        
        # Combine date with zero time
        date_list.append(start_date.strftime("%Y-%m-%d"))

        # Update start date for the next iteration
        start_date -= timedelta(days=step_days)

    return date_list
