import boto3
from boto3.dynamodb.conditions import Attr
import os

DYNAMODB_TABLE = 'Brand'
dynamodb = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
table = dynamodb.Table('Brand')
auth_table = dynamodb.Table('Auth')
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

def store_phone_number(phone_number):
    print('storing phone number', phone_number)
    auth_table.put_item(
        Item={
            'phone_number': phone_number,
            'tries': 20
        }
    )
def get_tries(phone_number):
    try:
        response = auth_table.get_item(
            Key={
                'phone_number': phone_number
            }
        )
        item = response.get('Item')
        if item:
            return item.get('tries', 0)
        return 0
    except Exception as e:
        print(f"Error getting tries for phone number: {e}")
        return 0
