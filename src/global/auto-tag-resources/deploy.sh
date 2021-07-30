#!/bin/bash

TEMPLATE_FILE=$1
OUTPUT_FILE='output.yml'
STACK_NAME='stack3'
S3_BUCKET='1605151765-andy'
PROFILE=$2

if aws cloudformation package --template-file ${TEMPLATE_FILE} --output-template-file ${OUTPUT_FILE} --s3-bucket ${S3_BUCKET} --profile $2; then
    echo "Successfully created the package"
else
    echo "Failed creating Cloudformation package"
    exit 1
fi 

if aws cloudformation deploy --template-file ${OUTPUT_FILE} --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --region us-east-1 --profile $2; then
    echo "Successfully deploy package"
else
    echo "Failed deploying package"
    exit 1
fi