import json
import time
import string
import os
from random import choice
import boto3

print('Loading function')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    sns = boto3.client('sns')
    number = event['Details']['Parameters']['Number']
    if not number.startswith('+614'):
        number = event['Details']['ContactData']['Attributes']['TheNumber']

    if number.startswith('04'):
        number = '+61' + number[1:]

    print(number)

    contactid = event['Details']['ContactData']['ContactId']

    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))

    expiry = int(time.time()+120)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE'))

    table.put_item(
                Item={
                    'ContactId': contactid,
                    '4digitcode': random,
                    'TTL': expiry
                }
            )

    sns.publish(
        PhoneNumber=number,
        Message=random
    )
    return {}
