import os
import json

# NOTE: appwrite==4.1.0 is required currently due to broken Queries in 5.0.1!!!
# Query syntax in 5.0.1 is modified for the new server changes but those changes
# have not taken effect yet...

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query

from .utils import get_date_list

# Environment variables
APPWRITE_API_KEY = os.environ['APPWRITE_API_KEY']
PROJECT_ID = os.environ['PROJECT_ID']
DATABASE_ID = os.environ['DATABASE_ID']
COLLECTION_ID_CRYPTO = os.environ['COLLECTION_ID_CRYPTO']
COLLECTION_ID_STOCK = os.environ['COLLECTION_ID_STOCK']

# Adds cors headers to response
def getHeaders():
    return {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type"}

# Queries the database for stock/crypto timeseries price data based on query params
# \param - market_type: either "stocks" or "crypto"
# \param - symbol: stock or coin symbol (UPPERCASE)
# \param - timeseries: resolution of queried data (either "DAILY", "WEEKLY", or "MONTHLY")
# \param - window_offset: number of timeseries units to offset from today
# \param - window_size: number of data points
# \return - tuple: (data, status_code)
def queryTimeSeries(market_type: str, symbol: str, timeseries: str="WEEKLY", window_offset: int=0, window_size: int=52):
    # Set a hard limit of 104 values from query
    window_size = min(window_size, 104)
    
    if timeseries.upper() == "DAILY":
        step = 1
    elif timeseries.upper() == "WEEKLY":
        step = 7
    elif timeseries.upper() == "MONTHLY":
        step = 30
    else:
        return ({"error": "Not a valid timeseries: {}".format(timeseries)}, 400)
        
    # Set collection ID to correct collection (either stock or crypto)
    COLLECTION_ID_PROFILE = COLLECTION_ID_CRYPTO if market_type == "crypto" else COLLECTION_ID_STOCK
    
    dates = get_date_list(window_offset, step, window_size)
    
    client = (
        Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(PROJECT_ID)
            .set_key(os.environ[APPWRITE_API_KEY])
    )
    
    client.set_self_signed(status=True)
    client.set_key(APPWRITE_API_KEY)

    databases = Databases(client)   
    
    try:
        docs = databases.list_documents(
            DATABASE_ID, 
            COLLECTION_ID_PROFILE,
            queries=[
                Query.order_asc('date'),
                Query.equal('symbol', symbol),
                Query.equal('date', dates),
                Query.select(['date', 'symbol', 'price', 'low', 'high'])
            ] 
        )
    except Exception as e:
        return ({"error": "Error during query: {}".format(e)}, 500)
    
    if docs['total'] <= 0:
        return ({"error": "No docs matched query"}, 400)
        
    return (docs, 200)


def main(context):
    # Get the symbol of interest

    context.log(json.dumps(context.req.query)) ##
    context.log(context.req.query_string) ##
    context.log(json.dumps(context.req.body)) ##
    context.log(context.req.body_raw) ##

    if "crypto" in context.req.path.lower():
        market_type = "crypto"
    elif "stock" in context.req.path.lower():
        market_type = "stock"
    else:
        errmsg = "URL path `{}` does not include 'stock' or 'crypto' sub path".format(context.req.path)
        context.error(errmsg)
        return context.res.json({"error": errmsg}, 400, getHeaders())
    
    context.log("market_type = {}".format(market_type))
    
    # Check symbol is provided
    if "symbol" not in context.req.query.keys():
        errmsg = "Query param 'symbol' is required"
        context.error(errmsg)
        return context.res.json({"error": errmsg}, 400, getHeaders())
    
    symbol = context.req.query["symbol"]
    
    context.log(symbol)
    
    # Get non-required params
    length     = int(context.req.query.get("length", 52))
    offset     = int(context.req.query.get("offset", 0))
    timeseries = context.req.query.get("timeseries", "DAILY")
    
    # Returns a tuple of (data, status_code)
    docs = queryTimeSeries(market_type=market_type, symbol=symbol, timeseries=timeseries, window_offset=offset, window_size=length)
    
    context.log("Returning {} docs from db query".format(len(docs[0])))
    
    return context.res.json(docs[0], docs[1], getHeaders())

