#!/bin/bash

TEMPLATE_FILE='example.yml'
OUTPUT_FILE='output.yml'
STACK_NAME='my-stack'
S3_BUCKET='<bucket to store template file>'

if aws cloudformation package --template-file ${TEMPLATE_FILE} --output-template-file ${OUTPUT_FILE} --s3-bucket ${S3_BUCKET}; then
    echo "Successfully created the package"
else
    echo "Failed creating Cloudformation package"
    exit 1
fi 

if aws cloudformation deploy --template-file ${OUTPUT_FILE} --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --region ap-southeast-2; then
    echo "Successfully deploy package"
else
    echo "Failed deploying package"
    exit 1
fi