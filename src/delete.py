import os
# import json
import boto3

# from utils import decimalencoder
from utils.todoTableClass import todoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


# Elimina un elemento de la lista
def delete(event, context):
    mytable = todoTableClass(dynamodb)
    mytable.delete_todo(event['pathParameters']['id'])

    response = {
            "statusCode": 200
        }

    return response
