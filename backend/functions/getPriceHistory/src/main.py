import os
import json
import requests
from datetime import datetime

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

# Environment variables
ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']
# PROJECT_ID = os.environ['PROJECT_ID']
# DATABASE_ID = os.environ['DATABASE_ID']
# COLLECTION_ID_PROFILE = os.environ['COLLECTION_ID_PROFILE']

### constants
CRYPTO_FUNC_BASE = "DIGITAL_CURRENCY_"
STOCK_FUNC_BASE = "TIME_SERIES_"

# POST - send data to db
# GET  - query from db and send to db
# PUT  - 
# DELETE - 

def parcePriceObjToDocument(symbol, date, values):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    iso_date_str = date_obj.isoformat()
    
    open_value = None
    high_value = None
    low_value  = None
    
    # Make key grabbing more dynamic
    # TODO: worry about currency code to confirm its USD
    for key, value in values.items():
        if "open" in key:
            open_value = float(value)
        elif "high" in key:
            high_value = float(value)
        elif "low" in key:
            low_value = float(value)
    
    transformed_entry = {
        "date": iso_date_str,
        "symbol": symbol,
        "price": open_value,
        "low": low_value,
        "high": high_value
    }
    
    return transformed_entry


def getPriceHistoryAlphaVantage(symbol, outputsize="compact", market_type="stock", timeseries="DAILY", market="USD"):
    headers       = { "Content-Type": "application/json" }
    crypto_market = "" # Only for crypto currency market (must give conversion currency)
    function      = "TIME_SERIES_DAILY"
    
    # Determine API function
    if "crypto" in market_type.lower():
        function = CRYPTO_FUNC_BASE + timeseries
        crypto_market = "&market=" + market
    elif "stock" in market_type.lower():
        function = STOCK_FUNC_BASE + timeseries

    url = 'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}{crypto_market}&apikey={key}'.format(
        function=function,
        outputsize=outputsize,
        symbol=symbol,
        crypto_market=crypto_market,
        key=ALPHAVANTAGE_API_KEY
    )
    
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        errmsg = "Error: {} {}".format(response.status_code, response.text)
        return errmsg

    #convert string to  object
    object = json.loads(response.text)
    
    # Find the key containing the substring "Time Series"
    # Needed for the key being a varaible depending on the time series resolution
    time_series_key = next(key for key in object.keys() if "Time Series" in key)
    
    transformed_data = []
    for date, values in object[time_series_key].items():
        parsedObj = parcePriceObjToDocument(symbol=symbol, date=date, values=values)
        transformed_data.append(parsedObj)
        
    return transformed_data

# Checks input from 
def alphaVantageQuery(market_type, query):

    # Check symbol is provided
    if "symbol" not in query.keys():
        errmsg = "Error: 'symbol' query param is required"
        return errmsg
    
    symbol = query["symbol"]
    
    # Default time series is daily but overwrite if it was provided
    timeseries = "DAILY"
    # Determine series of daily, weekly, or monthly
    if "timeseries" in query.keys():
        timeseries = query["timeseries"].upper()
    
    if timeseries not in ["DAILY", "WEEKLY", "MONTHLY"]:
        errmsg = "Error: timeseries param not containg valid timeseries value"
        return errmsg
    
    # Get non-required params
    outputsize = query.get("outputsize", "compact")
    market = query.get("market", "USD")
        
    documents = getPriceHistoryAlphaVantage(
        symbol, 
        outputsize=outputsize, 
        market_type=market_type, 
        timeseries=timeseries,
        market=market)
    
    return documents
    
def main(context):

    if "crypto" in context.req.path.lower():
        market_type = "crypto"
    elif "stock" in context.req.path.lower():
        market_type = "stock"
    else:
        errmsg = "Error: URL path `{}` does not include 'stock' or 'crypto' sub path".format(context.req.path)
        context.error(errmsg)
        return context.res.send(errmsg)
    
    documents = alphaVantageQuery(market_type, context.req.query)
        
    # Error occured getting documents of API data
    if isinstance(documents, str):
        context.error(documents)
        return context.res.send(documents)
    
    # Check method to either return documents or add to database
    
    return context.res.json(documents)

