from datetime import datetime, timedelta
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

