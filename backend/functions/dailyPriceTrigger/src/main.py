from appwrite.client import Client
import os

from appwrite.services.functions import Functions
# Environment variables
FINNHUB_API_KEY = os.environ['FINNHUB_API_KEY']
PROJECT_ID = os.environ['PROJECT_ID']
DATABASE_ID = os.environ['DATABASE_ID']
COLLECTION_ID_PROFILE = os.environ['COLLECTION_ID_PROFILE']
APPWRITE_API_KEY = os.environ['APPWRITE_API_KEY']
FUNCTION_getTodaysPrice_ID = os.environ['FUNCTION_getTodaysPrice_ID']

client = (
    Client()    
    .set_endpoint('https://cloud.appwrite.io/v1')
    .set_project(PROJECT_ID)
    .set_key(APPWRITE_API_KEY)
)

functions = Functions(client)

result = functions.create_execution(FUNCTION_getTodaysPrice_ID, path="/stock?symbol=QQQ", method='POST')

print(result)

