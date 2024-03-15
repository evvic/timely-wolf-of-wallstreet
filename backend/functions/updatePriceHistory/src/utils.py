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
        if not quote:
            errmsg = "Error getting quote for {}".format(symbol)
            return (False, errmsg)
        
    return (True, quote)
