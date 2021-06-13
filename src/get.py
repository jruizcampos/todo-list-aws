import os
import json
import boto3

from utils import decimalencoder
from utils.todoTableClass import todoTableClass


if os.environ["ENVIRONMENT"] == "LOCAL":
    dynamodb = None
else:
    dynamodb = boto3.resource("dynamodb")


# Obtiene un elemento de la tabla a partir de su id
def get(event, context):
    mytable = todoTableClass(dynamodb)
    result = mytable.get_todo(event['pathParameters']['id'])

    response = {
                "statusCode": 200,
                "body": json.dumps(result['Item'],
                                   cls=decimalencoder.DecimalEncoder)
            }

    return response
