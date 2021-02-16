#!/usr/bin/env bash
S3_BUCKET=$1
STACK_NAME=$2
EMAIL=$3
REGION=$4
aws cloudformation package --template-file template.yaml --s3-bucket ${S3_BUCKET} --output-template-file packaged-template.yaml
aws cloudformation create-stack --template-body file://$(pwd)/packaged-template.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --parameters ParameterKey=EmailToSend,ParameterValue=${EMAIL} --region ${REGION}

