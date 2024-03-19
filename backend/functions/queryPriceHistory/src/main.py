import os
from datetime import date, timedelta, datetime

# NOTE: appwrite==4.1.0 is required currently due to broken Queries in 5.0.1!!!
# Query syntax in 5.0.1 is modified for the new server changes but those changes
# have not taken effect yet...

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query

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
    
def get_date_list(offset_days, step_days, window_size):
  """
  Generates a list of datetime objects for a window based on offset and step.

  Args:
      offset_days (int): Number of days offset from today (0 for today).
      step_days (int): Step size between dates (e.g., 6 for every Monday).
      window_size (int): Number of dates to include in the window.

  Returns:
      list: List of datetime objects for the specified window.
  """

  # Get today's date
  today = date.today()

  # Calculate start date based on offset
  start_date = today - timedelta(days=offset_days)

  # List to store datetime objects
  date_list = []

  # Iterate for the window size
  for _ in range(window_size):

    # Skip weekends by shifting to the closest weekday
    while start_date.weekday() == 5:  # 5 and 6 represent Saturday and Sunday
        start_date -= timedelta(days=1)
    
    # Combine date with zero time
    date_list.append(start_date.strftime("%Y-%m-%d"))

    # Update start date for the next iteration
    start_date -= timedelta(days=step_days)

  return date_list
    
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