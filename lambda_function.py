import json
import opsgenie_sdk

print('Loading function')

class OpsAlert():
    def __init__(self):
        self.conf = opsgenie_sdk.configuration.Configuration()
        self.conf.api_key['Authorization'] = 'd2ade71c-a8a8-40bc-9a27-1507e3cccad9'

        self.api_client = opsgenie_sdk.api_client.ApiClient(configuration=self.conf)
        self.alert_api = opsgenie_sdk.AlertApi(api_client=self.api_client)

    def send(self, message):
        body = opsgenie_sdk.CreateAlertPayload(
          message=message,
          priority='P2'
        )
        try:
            create_response = self.alert_api.create_alert(create_alert_payload=body)
            print(create_response)
            return create_response
        except opsgenie_sdk.ApiException as err:
            print("Exception when calling AlertApi->create_alert: %s\n" % err)

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    number = event['Details']['Parameters']['Number']
    if not number.startswith('+614'):
        number = event['Details']['ContactData']['Attributes']['TheNumber']

    if number.startswith('04'):
        number = '+61' + number[1:]

    print(number)

    alert = OpsAlert()
    alert.send('The following number requires emergency assistance:' + number)
    return {}
