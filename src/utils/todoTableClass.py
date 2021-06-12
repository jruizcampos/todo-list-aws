import json
import logging
import os
import time
import uuid
import boto3

from utils import decimalencoder
traductor = boto3.client('translate')


class todoTableClass(object):

    #def __init__(self, table, dynamodb=None):
    def __init__(self, dynamodb=None):
        #self.tableName = table
        self.tableName = os.environ['DYNAMODB_TABLE']
        
        if not dynamodb:
            dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000') 
			#dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        self.dynamodb = dynamodb

    def create_todo_table(self):
        table = self.dynamodb.create_table(
            TableName=self.tableName,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        # Wait until the table exists.
        table.meta.client.get_waiter(
            'table_exists').wait(TableName=self.tableName)
        if (table.table_status != 'ACTIVE'):
            raise AssertionError()

        return table

    def delete_todo_table(self):
        table = self.dynamodb.Table(self.tableName)
        table.delete()

    #Obtiene un elemento de la tabla a partir de su id
    def get_todo(self, id):
        table = self.dynamodb.Table(self.tableName)
        
        try:
            result = table.get_item(
                Key={
                    'id': id
                }
            )
        except Exception as e:
            raise e
        else:
            return result

    #Obtiene la lista completa de elementos
    def scan_todo(self):
        table = self.dynamodb.Table(self.tableName)
        
        try:
            result = table.scan()
        except Exception as e:
            raise e
        else:
            return result
    
    #Actualiza un elemento de la tabla a partir de su id
    def update_todo(self, text, id, checked):
        timestamp = int(time.time() * 1000)
        table = self.dynamodb.Table(self.tableName)
        
        try:
            result = table.update_item(
                Key={
                    'id': id
                },
                ExpressionAttributeNames={
                  '#todo_text': 'text',
                },
                ExpressionAttributeValues={
                  ':text': text,
                  ':checked': checked,
                  ':updatedAt': timestamp,
                },
                UpdateExpression='SET #todo_text = :text, '
                                 'checked = :checked, '
                                 'updatedAt = :updatedAt',
                ReturnValues='ALL_NEW',
            )
        except Exception as e:
            raise e
        else:
            return result

    #Agrega un nuevo elemento a la lista
    def put_todo(self, text, id=None):
        if not id:
            id = str(uuid.uuid1())
        
        timestamp = str(time.time())
        table = self.dynamodb.Table(self.tableName)
        
        try:
            item = {
                'id': id,
                'text': text,
                'checked': False,
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }
            table.put_item(Item=item)
            
        except Exception as e:
            raise e
        else:
            return item

    #Elimina un elemento de la lista
    def delete_todo(self, id):
        table = self.dynamodb.Table(self.tableName)
        
        try:
            table.delete_item(
                Key={
                    'id': id
                }
            )
        except Exception as e:
            raise e
        else:
            return True
    
    #Traduce un elemento de la lista
    def translate_todo(self, id, source_language, target_language):
        table = self.dynamodb.Table(self.tableName)
        
        result = table.get_item(
            Key={
                'id': id
            }
        )
        
        try:
            result = traductor.translate_text(Text=result['Item'].get('text'), SourceLanguageCode=source_language, TargetLanguageCode=target_language)
        
        except Exception as e:
            raise e
        else:
            return result
