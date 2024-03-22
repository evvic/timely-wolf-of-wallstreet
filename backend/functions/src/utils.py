from datetime import date, datetime, timedelta
import finnhub

# String to list
def strtolist(var):
    if isinstance(var, str):
        return [var]
    else:
        return var

# Uses FinnHub API to retrieve stock price data
# Error should return error string with it
# Return - Tuple (Boolean of pass/fail, quote dict/error message)
def getStockPriceToday(symbol: str, finnhub_key: str):
    
    finnhub_client = finnhub.Client(api_key=finnhub_key)
    
    try:
        quote = finnhub_client.quote(symbol)
    except finnhub.exceptions.FinnhubAPIException as e:
        errmsg = "Error getting quote: {}".format(e)
        return {"error": errmsg}
    else:
        if not quote or "c" not in quote.keys():
            errmsg = "Error getting quote for {}".format(symbol)
            return {"error": errmsg}
        
    return quote


# Format to correct document type
def formatStockDocument(symbol: str, price_data: dict, date = None) -> dict:
    
    date = date if date else datetime.now()
    
    # Assuming standard time (not DST) - adjust for DST if needed
    offset = timedelta(hours=4)

    # Subtract 4 hours from the current datetime (estimate NYSE time from UTC)
    now_nyse_approx = date - offset
        
    # Create a new datetime object with year, month, and day only (time set to 00:00:00)
    date = datetime(now_nyse_approx.year, now_nyse_approx.month, now_nyse_approx.day)
    
    stock_doc = {
        "symbol": symbol,
        "price": price_data["c"],
        "low": price_data["l"],
        "high": price_data["h"],
        "date": date.isoformat() # datetime must be JSON serializable
    }
    
    return stock_doc

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

