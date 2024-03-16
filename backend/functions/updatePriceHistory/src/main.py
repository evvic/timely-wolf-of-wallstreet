import os
import json
import requests

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

from .utils import getStockPriceToday
from .utils import formatStockDocument

# Environment variables
FINNHUB_API_KEY = os.environ['FINNHUB_API_KEY']
PROJECT_ID = os.environ['PROJECT_ID']
DATABASE_ID = os.environ['DATABASE_ID']
COLLECTION_ID_PROFILE = os.environ['COLLECTION_ID_PROFILE']



# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    
    # Get the symbol of interest
    query_params = context.req.query
    
    context.log(json.dumps(query_params)) ##
    context.log(context.req.query_string) ##
    
    symbol = "AAPL" ## temp init
    if "symbol" in query_params.keys():
        symbol = query_params["symbol"]
    else:
        context.error("Error: no symbol provided! Must include i.e. ?symbol=AAPl")
        return context.res.send("Error: no symbol provided! Must include i.e. ?symbol=AAPl")
        
    log = "\nsymbol == {}\n".format(symbol)
    
    context.log(log)
    
    #data = databases.list_documents(database_id=DATABASE_ID, collection_id=COLLECTION_ID_PROFILE)
    
    #context.log(data)
    #context.log(FINNHUB_API_KEY)
    
    resp = getStockPriceToday(symbol=symbol, finnhub_key=FINNHUB_API_KEY)
    
    context.log(resp)
    
    # Return error if it could not get symbol
    if resp[0] == False:
        # If something goes wrong, log an error
        context.error(resp[1])
        return context.res.send(resp[1])
    
    # resp[1] contains price data if no error
    price_data = resp[1]
    
    document_data = formatStockDocument(symbol=symbol, price_data=price_data)
    
    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        return context.res.json(price_data)
    # POST stock price data to database (create a document)
    elif context.req.method == "POST":
                
        client = (
            Client()
                .set_endpoint("https://cloud.appwrite.io/v1")
                .set_project(os.environ["PROJECT_ID"])
                #.set_key(os.environ["APPWRITE_API_KEY"])
        )
        
        databases = Databases(client)
        
        resp = databases.create_document(
            database_id=DATABASE_ID, 
            collection_id=COLLECTION_ID_PROFILE,
            document_id=ID.unique(),
            data=document_data
        )
        
        return context.res.send(resp)
        
        
        

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
