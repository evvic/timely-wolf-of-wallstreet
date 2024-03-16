from datetime import datetime
import finnhub

# Uses FinnHub API to retrieve stock price data
# Error should return error string with it
# Return - Tuple (Boolean of pass/fail, quote dict/error message)
def getStockPriceToday(symbol: str, finnhub_key: str):
    
    finnhub_client = finnhub.Client(api_key=finnhub_key)
    
    try:
        quote = finnhub_client.quote(symbol)
    except finnhub.exceptions.FinnhubAPIException as e:
        errmsg = "Error getting quote: {}".format(e)
        return (False, errmsg)
    else:
        if not quote or "c" not in quote.keys():
            errmsg = "Error getting quote for {}".format(symbol)
            return (False, errmsg)
        
    return (True, quote)


# Format to correct document type
def formatStockDocument(symbol: str, price_data: dict, date = None) -> dict:
    
    date = date if date else datetime.now()
    
    stock_doc = {
        "symbol": symbol,
        "price": price_data["c"],
        "low": price_data["l"],
        "high": price_data["h"],
        "date": date.isoformat() # datetime must be JSON serializable
    }
    
    return stock_doc

