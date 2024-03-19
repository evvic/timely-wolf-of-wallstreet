import os
from datetime import date, timedelta, datetime

# NOTE: appwrite==4.1.0 is required currently due to broken Queries in 5.0.1!!!
# Query syntax in 5.0.1 is modified for the new server changes but those changes
# have not taken effect yet...

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query

from .utils import get_date_list

PROJECT_ID = 'market-hunters-dev'
DATABASE_ID = 'pricecharts'
COLLECTION_ID_CRYPTO = 'crypto'
COLLECTION_ID_STOCK = 'stocks'
APPWRITE_API_KEY = "556869225850c7a5383ca0d7e333b08f7a01eb5e718ee31805831a54b0876c0747e736c8ca5fe0d1c8d390280a82639ef86fbac93b7512be58225ed5946dddc1f604c2b7af31efdb194424010137cf3b64a35df6628b71883466f074233bcafeef12bd8d08e5859fa95fbec00579bad6d32bb72a2ed7f3deb12e0afda75fd0c8"

# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    # Why not try the Appwrite SDK?
    #
    # client = (
    #     Client()
    #     .set_endpoint("https://cloud.appwrite.io/v1")
    #     .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #     .set_key(os.environ["APPWRITE_API_KEY"])
    # )

    # You can log messages to the console
    context.log("Hello, Logs!")

    # If something goes wrong, log an error
    context.error("Hello, Errors!")

    # The `ctx.req` object contains the request data
    if context.req.method == "GET":
        # Send a response with the res object helpers
        # `ctx.res.send()` dispatches a string back to the client
        return context.res.send("Hello, World!")

    # `ctx.res.json()` is a handy helper for sending JSON
    return context.res.json(
        {
            "motto": "Build like a team of hundreds_",
            "learn": "https://appwrite.io/docs",
            "connect": "https://appwrite.io/discord",
            "getInspired": "https://builtwith.appwrite.io",
        }
    )
   
    
def queryTimeSeries(market_type, symbol, timeseries="WEEKLY", window_offset=0, window_size=52):
    # Set a hard limit of 104 values from query
    window_size = min(window_size, 104)
    
    # Set collection ID to correct collection (either stock or crypto)
    COLLECTION_ID_PROFILE = COLLECTION_ID_CRYPTO if market_type == "crypto" else COLLECTION_ID_STOCK
    
    client = (
        Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(PROJECT_ID)
            #.set_key(os.environ["APPWRITE_API_KEY"])
    )
    
    client.set_self_signed(status=True)
    client.set_key(APPWRITE_API_KEY)
    
    databases = Databases(client)  
    
    if timeseries.upper() == "DAILY":
        step = 1
    elif timeseries.upper() == "WEEKLY":
        step = 6
    elif timeseries.upper() == "MONTHLY":
        step = 30
    else:
        print("Error not a good timeseries")
        return
    
    # Adjust window size based on step
    window_size *= step
    
    docs = []
    for i in range(window_offset, window_size+window_offset, step):
        # Make the query with limit 1 and offset
        doc = databases.list_documents(
            DATABASE_ID,
            COLLECTION_ID_PROFILE,
            queries=[
                Query.order_desc("date"),
                Query.equal("symbol", symbol),
                #Query.greater_than("price", 870),
                Query.limit(1),  # Limit to 1 document
                Query.offset(i),  # Specify offset
            ]
        )
        print(doc)

        # Check if any documents were retrieved
        if not doc:
            break
            
        docs.append(doc["documents"][0])
    
    return docs
    
def practiceQuery(market_type, symbol, timeseries="WEEKLY", window_offset=0, window_size=52):
    # Set a hard limit of 104 values from query
    window_size = min(window_size, 104)
    
    if timeseries.upper() == "DAILY":
        step = 1
    elif timeseries.upper() == "WEEKLY":
        step = 7
    elif timeseries.upper() == "MONTHLY":
        step = 30
    else:
        print("Error not a good timeseries")
        return
    
    # Set collection ID to correct collection (either stock or crypto)
    COLLECTION_ID_PROFILE = COLLECTION_ID_CRYPTO if market_type == "crypto" else COLLECTION_ID_STOCK
    
    dates = get_date_list(window_offset, step, window_size)
    print(dates)
    
    client = (
        Client()
            .set_endpoint("https://cloud.appwrite.io/v1")
            .set_project(PROJECT_ID)
            #.set_key(os.environ["APPWRITE_API_KEY"])
    )
    
    client.set_self_signed(status=True)
    client.set_key(APPWRITE_API_KEY)

    databases = Databases(client)   
    
    docs = databases.list_documents(
        DATABASE_ID, 
        COLLECTION_ID_PROFILE,
        queries=[
            Query.order_asc('date'),
            Query.equal('symbol', symbol),
            #Query.greater_than('price', 870),
            #Query.limit(window_size),
            Query.equal('date', dates)
        ] 
        )
    
    if docs['total'] <= 0:
        print("No docs matched query")
        return
    
    for doc in docs['documents']:
        print(doc)
        
    return docs
    


docs = practiceQuery(market_type='stocks', symbol="TSLA", timeseries="MONTHLY", window_offset=0, window_size=5)

import pdb
pdb.set_trace()

print(docs)


dates = get_date_list(0, 7, 5)
print(dates)