import os

from appwrite.client import Client
from appwrite.services.functions import Functions

# Environment variables
PROJECT_ID = os.environ['PROJECT_ID']
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
