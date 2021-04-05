# Connect Escalation


## Notes

`gsed` is used on MacOS (Installed via brew), because `sed` was on MacOS doesn't support `-i`.
Change to `sed` if on another platform

I've designed this to work in Australia specifically. Lambda and Connect configuration and code will need to be changed for other countries.

## Requirements
* A working Connect Instance with a claimed number
* An integration Ops Genie API Key with alert create permissions

## TL;DR

Setup:
```
export CONNECT_ARN=""
export OPSGENIE_KEY="abc123"
export STACK_NAME=esc
```

Let's go:
```
./deploy.sh
```

## Details

Create CloudFormation Stack:
```
aws cloudformation deploy --template-file ./cfn.yaml --stack-name $STACK_NAME \
--parameter-overrides ConnectInstanceARN=$CONNECT_ARN OpsGenieAPIKEY=$OPSGENIE_KEY \
--capabilities CAPABILITY_NAMED_IAM
```

Validate CloudFormation:
```
cfn-lint ./cfn.yaml
```

Delete CloudFormation Stack:
```
aws cloudformation delete-stack --stack-name esc
```


Install 3rd party packages:
```
mkdir package
pip3 install --target ./package opsgenie-sdk
```

Create the Lambda Code Package:
```
cd package; zip -r ../escalation-deployment-package.zip .
cd ../
zip -g escalation-deployment-package.zip *.py
```

Get the Lambda function ARNs to use in the next step:
```
$(aws cloudformation describe-stacks --stack-name $STACK_NAME --output text --query 'Stacks[0].Outputs' | tr "\t" "=" | sed 's/^/export /')
```

Update the Connect configuration ready for import and deploy the _real_ code to the Lambda function:
```
for function in SendPageARN Check4DigitCodeARN SendSMSARN CheckCallerIDARN
do
  gsed -i "s/${function}/${!function}/" Escalation.json
  aws lambda update-function-code --function-name ${!function} --zip-file fileb://./escalation-deployment-package.zip
done
```

## Connect Instance
Create a new Contact flow and import `Escalation.json`.

Change the _contact flow/IVR_ on the phone number you want to use to `Escalation`.
