import json
# import time
import logging
import os
import boto3

from utils import decimalencoder
from utils.todoTableClass import todoTableClass

if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


# Actualiza un elemento de la tabla a partir de su id
def update(event, context):
    mytable = todoTableClass(dynamodb)

    data = json.loads(event['body'])

    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    result = mytable.update_todo(
        data['text'],
        event['pathParameters']['id'],
        data['checked'])

    response = {
            "statusCode": 200,
            "body": json.dumps(result['Attributes'],
                               cls=decimalencoder.DecimalEncoder)
        }

    return response
