import json

print('Loading function')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    number = event['Details']['ContactData']['CustomerEndpoint']['Address']
    if number.startswith('+614'):
        result_map = {"Number":number}
    else:
        raise Exception('Not a mobile number')
    return result_map
