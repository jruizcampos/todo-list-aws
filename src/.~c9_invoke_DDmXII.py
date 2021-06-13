import json
import logging
import os
# import time
# import uuid
import boto3

# from utils import decimalencoder
from utils.todoTableClass import todoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


# Agrega un nuevo elemento a la lista
def create(event, context):
    data = json.loads(event['body'])

    if 'text' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")

    mytable = todoTableClass(dynamodb)
    item = mytable.put_todo(data['text'])

    response = {
                "statusCode": 200,
                "body": json.dumps(item)
            }
    return response
