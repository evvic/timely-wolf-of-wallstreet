import os
import json
import requests
from datetime import datetime

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

# Environment variables
ALPHAVANTAGE_API_KEY = os.environ['ALPHAVANTAGE_API_KEY']
PROJECT_ID = os.environ['PROJECT_ID']
DATABASE_ID = os.environ['DATABASE_ID']
COLLECTION_ID_CRYPTO = os.environ['COLLECTION_ID_CRYPTO']
COLLECTION_ID_STOCK = os.environ['COLLECTION_ID_STOCK']

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
def alphaVantageQuery(market_type, context):
    
    query = context.req.query ## temp?

    # Check symbol is provided
    if "symbol" not in query.keys():
        errmsg = "Error: 'symbol' query param is required"
        return errmsg
    
    symbol = query["symbol"]
    
    context.log(symbol)
    
    # Get non-required params
    outputsize = query.get("outputsize", "compact")
    market     = query.get("market", "USD")
    timeseries = query.get("timeseries", "DAILY")
    
    context.log("{} {} {}".format(outputsize, market, timeseries))
    
    # Determine series of daily, weekly, or monthly
    if timeseries not in ["DAILY", "WEEKLY", "MONTHLY"]:
        errmsg = "Error: timeseries param not containg valid timeseries value"
        return errmsg
    
    try:
        documents = getPriceHistoryAlphaVantage(
            symbol, 
            outputsize=outputsize, 
            market_type=market_type, 
            timeseries=timeseries,
            market=market)
    except Exception as e:
        context.log(e)
    
    return documents
    
def main(context):
    
    # Get the symbol of interest
    query_params = context.req.query
    
    context.log(json.dumps(query_params)) ##
    context.log(context.req.query_string) ##
    context.log(json.dumps(context.req.body)) ##
    context.log(context.req.body_raw) ##

    if "crypto" in context.req.path.lower():
        market_type = "crypto"
    elif "stock" in context.req.path.lower():
        market_type = "stock"
    else:
        errmsg = "Error: URL path `{}` does not include 'stock' or 'crypto' sub path".format(context.req.path)
        context.error(errmsg)
        return context.res.send(errmsg)
    
    context.log("market_type = {}".format(market_type))
    
    documents = alphaVantageQuery(market_type, context)
        
    # Error occured getting documents of API data
    if isinstance(documents, str):
        context.error(documents)
        return context.res.send(documents)
    
    # Check method to either return documents or add to database
    # The `ctx.req` object contains the request data
    # POST stock price data to database (create documents)
    if context.req.method == "POST":
        context.log("Adding data to database")
        
        # Set collection ID to correct collection (either stock or crypto)
        COLLECTION_ID_PROFILE = COLLECTION_ID_CRYPTO if market_type == "crypto" else COLLECTION_ID_STOCK
        
        # Init client for posting
        client = (
            Client()
                .set_endpoint("https://cloud.appwrite.io/v1")
                .set_project(os.environ["PROJECT_ID"])
                #.set_key(os.environ["APPWRITE_API_KEY"])
        )

        databases = Databases(client)
        
        responses = []
        for index, doc in enumerate(documents):
            
            resp = databases.create_document(
                database_id=DATABASE_ID, 
                collection_id=COLLECTION_ID_PROFILE,
                document_id=ID.unique(),
                data=doc
            )
            
            #responses.append(resp)
            
        #context.log("Added {} documents to {} collection".format(len(responses), COLLECTION_ID_PROFILE))
        
        #documents = responses
    
    return context.res.json(documents)

