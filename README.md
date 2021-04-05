# Connect Escalation


Notes:

`gsed` is used on MacOS (Installed via brew), because `sed` was on MacOS doesn't support `-i`.
Change to `sed` if on another platform

Setup:
```
export CONNECT_ARN=""
export OPSGENIE_KEY="abc123"
export STACK_NAME=esc
```


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

```
$(aws cloudformation describe-stacks --stack-name $STACK_NAME --output text --query 'Stacks[0].Outputs' | tr "\t" "=" | sed 's/^/export /')
```

```
for function in SendPageARN Check4DigitCodeARN SendSMSARN CheckCallerIDARN
do
  gsed -i "s/${function}/${!function}/" Escalation.json
  aws lambda update-function-code --function-name ${!function} --zip-file fileb://./escalation-deployment-package.zip
done
```

Create a new Contact flow and import `Escalation.json`.
