import os
import json
import requests

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

from .utils import getStockPriceToday
from .utils import formatStockDocument
from .utils import strtolist

# Environment variables
FINNHUB_API_KEY = os.environ['FINNHUB_API_KEY']
PROJECT_ID = os.environ['PROJECT_ID']
DATABASE_ID = os.environ['DATABASE_ID']
COLLECTION_ID_PROFILE = os.environ['COLLECTION_ID_PROFILE']

# Functionalize symbols collection
# Symbol can be passed through query param as a single string
# Symbol can also be passed into the body as an object of either
# one string or an array of symbols
def collect_symbols(query_req, body_req):
    symbols = []
    if "symbol" in query_req.keys():
        symbols.append(query_req["symbol"].upper())
    if "symbol" in body_req.keys():
        for symbol in strtolist(body_req["symbol"]):
            symbols.append(symbol.upper())
    if "symbols" in body_req.keys():
        for symbol in strtolist(body_req["symbols"]):
            symbols.append(symbol.upper())
            
    # Remove duplicates
    unique_symbols = set(symbols)
    
    return list(unique_symbols)

# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    
    # Get the symbol of interest
    query_params = context.req.query
    
    context.log(json.dumps(query_params)) ##
    context.log(context.req.query_string) ##
    context.log(json.dumps(context.req.body)) ##
    context.log(context.req.body_raw) ##
    
    # Verify body is an actual dict
    body_obj = context.req.body_raw
    if context.req.body_raw == "" or context.req.body == "" or context.req.body_raw == None or context.req.body == None:
        body_obj = {}
        context.log("creating empty braces for body_obj")
    elif not isinstance(context.req.body_raw, dict):
        context.log("context.req.body_raw is not an instance of a dict, calling json.loads")
        body_obj = json.loads(context.req.body_raw)
    
    # Collect symbols
    symbols = collect_symbols(query_req=context.req.query, body_req=body_obj)
    
    if len(symbols) <= 0:
        errmsg = "Error: no symbol provided!\nCollected symbols: {}\nMust include i.e. ?symbol=AAPL".format(symbols)
        context.error(errmsg)
        return context.res.send(errmsg)
    
    context.log(symbols) ##
    
    client = (
        Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(os.environ["PROJECT_ID"])
            #.set_key(os.environ["APPWRITE_API_KEY"])
    )

    databases = Databases(client)            
    
    responses = []
    for symbol in symbols:

        log = "\nsymbol == {}\n".format(symbol)
        
        context.log(log)
        
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
        
        context.log("~~ pre dump ~~") ##
        context.log(json.dumps(document_data)) ##
        context.log("~~ post dump ~~") ##
        
        # The `ctx.req` object contains the request data
        if context.req.method == "GET":
            #return context.res.json(document_data)
            responses.append(document_data)
        # POST stock price data to database (create a document)
        elif context.req.method == "POST":
            
            resp = databases.create_document(
                database_id=DATABASE_ID, 
                collection_id=COLLECTION_ID_PROFILE,
                document_id=ID.unique(),
                data=document_data
            )
            
            responses.append(resp)
            
    return context.res.json(responses)

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
