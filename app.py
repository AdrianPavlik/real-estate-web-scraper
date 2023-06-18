__author__ = "Adrián Pavlik"
__license__ = "MIT"
__email__ = "pavlik.adrian1005@gmail.com"

import json
from dotenv import load_dotenv

keys = None
domDownloader = None

def handler(event, context):
    global keys, domDownloader
    keys = load_dotenv("./keys.env")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }