import os
import json
import requests
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

from .utils import getStockPriceToday

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
        
    log = "\nsymbol == {}\n".format(symbol)
    
    context.log(log)
    
    client = (
        Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(os.environ["PROJECT_ID"])
            #.set_key(os.environ["APPWRITE_API_KEY"])
    )
    
    databases = Databases(client)
    
    data = databases.list_documents(database_id=DATABASE_ID, collection_id=COLLECTION_ID_PROFILE)
    
    context.log(data)
    context.log(FINNHUB_API_KEY)
    
    resp = getStockPriceToday(symbol='AAPL', finnhub_key=FINNHUB_API_KEY)
    
    context.log(resp)
    
    if resp[0] == False:
        # If something goes wrong, log an error
        context.error(resp[1])

    # You can log messages to the console
    context.log("Hello, Logs!")
    
    ### TODO: save data for symbol to the database in an organized way to create a chart

    
    # The `ctx.req` object contains the request data
    if context.req.method == "GET" and resp[0] == True:
        return context.res.json(resp[1])
    elif context.req.method == "GET" and resp[0] == False:
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        return context.res.send(resp[1])

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
