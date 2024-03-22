# Cron Job Trigger: 0 20 * * 1-5
# This function is triggered by a cron job to run every business day at 4pm (GMT-4)
# (Approximately when the NYSE closes)
# The function triggers getTodaysPrice function and passes the symbols to get price data for
import os

from appwrite.client import Client
from appwrite.services.functions import Functions

# Environment variables
PROJECT_ID = os.environ['PROJECT_ID']
APPWRITE_API_KEY = os.environ['APPWRITE_API_KEY']
FUNCTION_getTodaysPrice_ID = os.environ['FUNCTION_getTodaysPrice_ID']

def main(context):
    client = (
        Client()    
        .set_endpoint('https://cloud.appwrite.io/v1')
        .set_project(PROJECT_ID)
        .set_key(APPWRITE_API_KEY)
    )

    functions = Functions(client)

    result = functions.create_execution(FUNCTION_getTodaysPrice_ID, path="/stock?symbol=QQQ", method='POST')

    context.log(result)
    
    return context.res.send(result)
