#!/usr/bin/env bash

aws cloudformation deploy --template-file ./cfn.yaml --stack-name $STACK_NAME \
--parameter-overrides ConnectInstanceARN=$CONNECT_ARN OpsGenieAPIKEY=$OPSGENIE_KEY \
--capabilities CAPABILITY_NAMED_IAM

mkdir package
pip3 install --target ./package opsgenie-sdk

cd package; zip -r ../escalation-deployment-package.zip .
cd ../
zip -g escalation-deployment-package.zip *.py

$(aws cloudformation describe-stacks --stack-name $STACK_NAME --output text --query 'Stacks[0].Outputs' | tr "\t" "=" | sed 's/^/export /')

for function in SendPageARN Check4DigitCodeARN SendSMSARN CheckCallerIDARN
do
  gsed -i "s/${function}/${!function}/" Escalation.json
  aws lambda update-function-code --function-name ${!function} --zip-file fileb://./escalation-deployment-package.zip
done
