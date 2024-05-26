import boto3
from boto3.dynamodb.conditions import Attr
import os

DYNAMODB_TABLE = 'Brand'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
table = dynamodb.Table('Brand')

def search_item_by_name(name):
    print('searching name', name)
    try:
        response = table.query(
            IndexName='name-index',  # Replace with your GSI name
            KeyConditionExpression=boto3.dynamodb.conditions.Key('name').eq(name)
        )

        print(response)
        items = response.get('Items', [])
        return items[0] if items else None
    except Exception as e:
        print(f"Error searching for item: {e}")
        return None