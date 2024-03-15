import os
import requests
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

from .utils import getStockPriceToday

# Environment variables
FINNHUB_API_KEY = os.environ['FINNHUB_API_KEY']


# This is your Appwrite function
# It's executed each time we get a request
def main(context):
    
    # client = (
    #     Client()
    #         .set_endpoint("https://cloud.appwrite.io/v1")
    #         .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
    #         .set_key(os.environ["APPWRITE_API_KEY"])
    # )
    
    # databases = Databases(client)
    
    context.log(FINNHUB_API_KEY)
    
    ### Main goal for now is to print stock price data to screen
    resp = getStockPriceToday(symbol='AAPL', finnhub_key=FINNHUB_API_KEY)
    
    context.log(resp)
    
    if resp[0] == False:
        # If something goes wrong, log an error
        context.error(resp[1])

    # You can log messages to the console
    context.log("Hello, Logs!")

    
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
