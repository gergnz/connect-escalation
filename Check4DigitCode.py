import json
import os
import boto3

print('Loading function')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    contactid = event['Details']['ContactData']['ContactId']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE'))

    item = table.get_item(
                Key={
                    'ContactId': contactid,
                }
            )
    storedcode = item['Item']['4digitcode']
    enteredcode = event['Details']['Parameters']['4DigitCode']
    if storedcode != enteredcode:
        raise Exception('Code does not match')
    table.delete_item(
                Key={
                    'ContactId': contactid,
                }
            )
    return {}
