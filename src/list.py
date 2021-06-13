import json
import os
import boto3

from utils import decimalencoder
from utils.todoTableClass import todoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


# Obtiene la lista completa de elementos
def list(event, context):
    mytable = todoTableClass(dynamodb)
    result = mytable.scan_todo()

    response = {
            "statusCode": 200,
            "body": json.dumps(result['Items'],
                               cls=decimalencoder.DecimalEncoder)
        }

    return response
